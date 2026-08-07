#!/usr/bin/env python3
"""TTS generation wrapper: annotated script -> audio files.

Supports multiple TTS backends:
  - cosyvoice: CosyVoice 3.0 (local GPU, recommended)
  - gptsovits: GPT-SoVITS (local GPU, alternative)
  - api: Remote API (Fish Audio etc, if configured)

Usage:
  python3 tts_generate.py script.json -o output/ --backend cosyvoice
  python3 tts_generate.py script.json -o output/ --backend cosyvoice --dry-run
"""
import sys, os, json, argparse, subprocess, time

# Add parent dir to path for voice_params
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voice_params import annotate_script, get_tts_params

def generate_cosyvoice(text, params, output_path, model_dir="pretrained_models/Fun-CosyVoice3-0.5B"):
    """Generate audio using CosyVoice 3.0.
    
    Requires CosyVoice installed on a GPU machine.
    This function constructs the Python call; actual execution needs the model.
    """
    ref_audio = params.get("ref_audio")
    instruct = params.get("instruct", "")
    speed = params.get("speed", 1.0)
    
    # CosyVoice instruct mode call
    code = f"""
import sys
sys.path.insert(0, 'CosyVoice')
from cosyvoice.cli.cosyvoice import CosyVoice2
from cosyvoice.cli.frontend import CosyVoiceFrontend

model = CosyVoice2('{model_dir}')
frontend = CosyVoiceFrontend('{model_dir}')

# Instruct mode for emotion control
instruct_text = "{instruct}"
ref_audio_path = "{ref_audio or ''}"

for chunk in model.inference_instruct2(
    text="{text}",
    instruct_text=instruct_text,
    prompt_speech_16k=ref_audio_path,
    speed={speed},
):
    # Save the last chunk
    pass

# Save audio
import torchaudio
# (chunk contains tensor in actual implementation)
"""
    # In dry-run mode, just show the command
    return code


def generate_gptsovits(text, params, output_path, api_url="http://localhost:9880"):
    """Generate audio using GPT-SoVITS API.
    
    GPT-SoVITS WebUI has an API mode at :9880.
    """
    ref_audio = params.get("ref_audio")
    if not ref_audio or not os.path.exists(ref_audio):
        raise FileNotFoundError(f"Reference audio not found: {ref_audio}")
    
    # GPT-SoVITS API call
    import urllib.request
    payload = json.dumps({
        "text": text,
        "text_lang": "zh",
        "ref_audio_path": ref_audio,
        "prompt_text": "",  # Could extract from ref audio
        "prompt_lang": "zh",
        "speed": params.get("speed", 1.0),
    }).encode()
    
    req = urllib.request.Request(
        f"{api_url}/tts",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    
    resp = urllib.request.urlopen(req, timeout=120)
    # Response is audio data
    with open(output_path, "wb") as f:
        f.write(resp.read())
    
    return output_path


def generate_segment(text, params, output_path, backend="cosyvoice", dry_run=False):
    """Generate one audio segment."""
    if dry_run:
        print(f"    [DRY-RUN] {text[:50]}...")
        print(f"    params: speed={params['speed']} emotion={params['emotion']} instruct={params.get('instruct','')[:30]}")
        # Create a placeholder file
        with open(output_path, "w") as f:
            f.write(f"DRY-RUN placeholder for: {text[:50]}")
        return output_path
    
    if backend == "gptsovits":
        return generate_gptsovits(text, params, output_path)
    elif backend == "cosyvoice":
        code = generate_cosyvoice(text, params, output_path)
        # Would execute on GPU machine
        print(f"    [CosyVoice code generated, needs GPU execution]")
        return code
    else:
        raise ValueError(f"Unknown backend: {backend}")


def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio from annotated script")
    parser.add_argument("script", help="Annotated script JSON file")
    parser.add_argument("-o", "--output", required=True, help="Output directory for audio files")
    parser.add_argument("--backend", default="cosyvoice", choices=["cosyvoice", "gptsovits", "api"])
    parser.add_argument("--dry-run", action="store_true", help="Show params without generating audio")
    parser.add_argument("--start", type=int, default=0, help="Start segment index")
    parser.add_argument("--end", type=int, default=None, help="End segment index (exclusive)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    with open(args.script, encoding="utf-8") as f:
        segments = json.load(f)

    # Add TTS params to segments
    segments = annotate_script(segments)

    start = args.start
    end = args.end or len(segments)
    segments = segments[start:end]

    print(f"Generating {len(segments)} segments ({args.backend}, dry_run={args.dry_run})")
    
    results = []
    for i, seg in enumerate(segments):
        text = seg["text"]
        params = seg["tts_params"]
        speaker = params["speaker"]
        emotion = params["emotion"]
        
        out_name = f"{start+i:04d}_{speaker}_{emotion}.wav"
        out_path = os.path.join(args.output, out_name)
        
        print(f"  [{i+1}/{len(segments)}] {speaker} ({emotion}): {text[:40]}...")
        
        try:
            if seg.get("type") == "sound_effect":
                # Skip TTS for sound effects, just log
                print(f"    [SFX] {seg.get('sfx_cue', 'unknown')}")
                results.append({"index": start+i, "file": None, "type": "sfx", "cue": seg.get("sfx_cue")})
                continue
            
            result = generate_segment(text, params, out_path, args.backend, args.dry_run)
            results.append({"index": start+i, "file": out_name, "type": seg.get("type"), "speaker": speaker, "emotion": emotion})
        except Exception as e:
            print(f"    FAILED: {e}", file=sys.stderr)
            results.append({"index": start+i, "file": None, "error": str(e)})

    # Save manifest
    manifest_path = os.path.join(args.output, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    success = sum(1 for r in results if r.get("file"))
    failed = sum(1 for r in results if r.get("error"))
    sfx = sum(1 for r in results if r.get("type") == "sfx")
    print(f"\nDone: {success} generated, {sfx} SFX, {failed} failed")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
