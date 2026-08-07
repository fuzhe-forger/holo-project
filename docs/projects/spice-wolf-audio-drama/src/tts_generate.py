#!/usr/bin/env python3
"""TTS generation: annotated script -> audio files.

Supports:
  - gptsovits: GPT-SoVITS API (local Mac, port 9880)
  - cosyvoice: CosyVoice API (local, port 50000)
  - dry-run: params only, no audio generation

Usage:
  python3 tts_generate.py script.json -o output/audio --backend gptsovits
  python3 tts_generate.py script.json -o output/audio --dry-run
"""
import sys, os, json, argparse, time, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voice_params import annotate_script

def generate_gptsovits(text, params, output_path, api_url="http://127.0.0.1:9880"):
    """Generate audio via GPT-SoVITS API v2.
    
    Requires GPT-SoVITS running in API mode:
      python3 api_v2.py --host 127.0.0.1 --port 9880
    """
    ref_audio = params.get("ref_audio")
    
    # Resolve ref audio path relative to project
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ref_audio and not os.path.isabs(ref_audio):
        ref_audio = os.path.join(project_root, "data", ref_audio)
    
    if not ref_audio or not os.path.exists(ref_audio):
        raise FileNotFoundError(
            f"Reference audio not found: {ref_audio}\n"
            f"Put reference audio in data/ref-voices/ and update voice_params.py"
        )
    
    # GPT-SoVITS API v2 payload
    payload = json.dumps({
        "text": text,
        "text_lang": "zh",
        "ref_audio_path": ref_audio,
        "prompt_text": "",
        "prompt_lang": "zh",
        "speed": params.get("speed", 1.0),
        "media_type": "wav",
        "streaming_mode": False,
    }).encode()
    
    req = urllib.request.Request(
        f"{api_url}/tts",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        audio_data = resp.read()
        with open(output_path, "wb") as f:
            f.write(audio_data)
        return output_path
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200] if e.read else ""
        raise RuntimeError(f"GPT-SoVITS API error {e.code}: {body}")
    except urllib.error.URLError as e:
        raise ConnectionError(
            f"Cannot reach GPT-SoVITS API at {api_url}. "
            f"Start it with: python3 api_v2.py --host 127.0.0.1 --port 9880"
        )

def generate_cosyvoice(text, params, output_path, api_url="http://127.0.0.1:50000"):
    """Generate audio via CosyVoice API.
    
    Requires CosyVoice webui running with API enabled.
    Uses instruct mode for emotion control.
    """
    ref_audio = params.get("ref_audio")
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ref_audio and not os.path.isabs(ref_audio):
        ref_audio = os.path.join(project_root, "data", ref_audio)
    
    instruct = params.get("instruct", "")
    speed = params.get("speed", 1.0)
    
    # CosyVoice API call (POST to /api/inference)
    payload = json.dumps({
        "text": text,
        "ref_audio_path": ref_audio or "",
        "instruct": instruct,
        "speed": speed,
        "mode": "instruct" if instruct else "zero_shot",
    }).encode()
    
    req = urllib.request.Request(
        f"{api_url}/api/inference",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        audio_data = resp.read()
        with open(output_path, "wb") as f:
            f.write(audio_data)
        return output_path
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"CosyVoice API error {e.code}")
    except urllib.error.URLError:
        raise ConnectionError(
            f"Cannot reach CosyVoice at {api_url}. "
            f"Start: python3 webui.py --port 50000"
        )

def generate_segment(text, params, output_path, backend="gptsovits", dry_run=False):
    """Generate one audio segment."""
    if dry_run:
        print(f"    [DRY-RUN] {text[:50]}...")
        print(f"    speed={params['speed']} emotion={params['emotion']} instruct={params.get('instruct','')[:40]}")
        with open(output_path, "w") as f:
            f.write(f"DRY-RUN: {text[:50]}")
        return output_path
    
    if backend == "gptsovits":
        return generate_gptsovits(text, params, output_path)
    elif backend == "cosyvoice":
        return generate_cosyvoice(text, params, output_path)
    else:
        raise ValueError(f"Unknown backend: {backend}")

def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio from annotated script")
    parser.add_argument("script", help="Annotated script JSON")
    parser.add_argument("-o", "--output", required=True, help="Output directory")
    parser.add_argument("--backend", default="gptsovits", choices=["gptsovits", "cosyvoice"])
    parser.add_argument("--api-url", default=None, help="Override API URL")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=None)
    parser.add_argument("--retry", type=int, default=2, help="Retry count for failed segments")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    with open(args.script, encoding="utf-8") as f:
        segments = json.load(f)

    segments = annotate_script(segments)
    segments = segments[args.start:(args.end or len(segments))]

    # Default API URLs
    api_urls = {
        "gptsovits": args.api_url or "http://127.0.0.1:9880",
        "cosyvoice": args.api_url or "http://127.0.0.1:50000",
    }

    print(f"Generating {len(segments)} segments ({args.backend}, dry_run={args.dry_run})")
    
    results = []
    for i, seg in enumerate(segments):
        text = seg["text"]
        params = seg["tts_params"]
        speaker = params["speaker"]
        emotion = params["emotion"]
        
        out_name = f"{args.start+i:04d}_{speaker}_{emotion}.wav"
        out_path = os.path.join(args.output, out_name)
        
        print(f"  [{i+1}/{len(segments)}] {speaker} ({emotion}): {text[:40]}...", end="", flush=True)
        
        if seg.get("type") == "sound_effect":
            print(f" [SFX: {seg.get('sfx_cue', '?')}]")
            results.append({"index": args.start+i, "file": None, "type": "sfx", "cue": seg.get("sfx_cue")})
            continue
        
        success = False
        for attempt in range(args.retry + 1):
            try:
                generate_segment(text, params, out_path, args.backend, args.dry_run)
                print(" OK")
                results.append({"index": args.start+i, "file": out_name, "type": seg.get("type"),
                                "speaker": speaker, "emotion": emotion})
                success = True
                break
            except Exception as e:
                if attempt < args.retry:
                    print(f" retry{attempt+1}", end="", flush=True)
                    time.sleep(3)
                else:
                    print(f" FAILED: {e}")
                    results.append({"index": args.start+i, "file": None, "error": str(e)})
        
        # Rate limit: be nice to local TTS
        if not args.dry_run and success:
            time.sleep(1)

    manifest_path = os.path.join(args.output, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    success_count = sum(1 for r in results if r.get("file"))
    failed_count = sum(1 for r in results if r.get("error"))
    sfx_count = sum(1 for r in results if r.get("type") == "sfx")
    print(f"\nDone: {success_count} generated, {sfx_count} SFX, {failed_count} failed")
    print(f"Manifest: {manifest_path}")

if __name__ == "__main__":
    main()
