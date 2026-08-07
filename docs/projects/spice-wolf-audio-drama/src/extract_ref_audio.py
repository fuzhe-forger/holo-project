#!/usr/bin/env python3
"""Extract clean reference audio clips from anime/BD sources.

Uses faster-whisper for transcription alignment, then ffmpeg to cut
clean single-speaker segments at precise timestamps.

Usage:
  python3 extract_ref_audio.py input_video.mp4 --character 赫萝 --output data/ref-voices/
  python3 extract_ref_audio.py input_video.mp4 --batch config.json
"""
import sys, os, json, argparse, subprocess, re

def extract_audio_segment(input_path, start, duration, output_path, sr=16000):
    """Extract a segment from input video/audio file."""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ss", str(start),
        "-t", str(duration),
        "-vn", "-ac", "1", "-ar", str(sr),
        "-af", "afftdn=nf=-25",  # denoise
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    return output_path

def transcribe_with_whisper(audio_path, language="ja"):
    """Transcribe audio with faster-whisper, return segments with timestamps."""
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("small", device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_path, language=language, 
                                           vad_filter=True,
                                           beam_size=5)
        results = []
        for seg in segments:
            results.append({
                "start": seg.start,
                "end": seg.end,
                "text": seg.text.strip(),
            })
        return results
    except ImportError:
        print("faster-whisper not installed. Install: pip install faster-whisper", file=sys.stderr)
        sys.exit(1)

def find_character_segments(transcript, character_keywords):
    """Find segments that likely belong to a specific character.
    
    Uses keyword matching on surrounding context. For Japanese anime,
    this is a heuristic — manual review recommended.
    """
    matches = []
    for i, seg in enumerate(transcript):
        text = seg["text"]
        # Check for character-specific speech patterns
        for kw in character_keywords:
            if kw in text:
                matches.append({**seg, "keyword": kw, "index": i})
                break
    return matches

# Character speech pattern keywords (Japanese)
CHARACTER_KEYWORDS = {
    "赫萝": ["咱", "汝", "ちん", "わっち", "ぬし", "フロウレンス"],  # Holo's archaic speech
    "罗伦斯": ["ロレンス", "さん", "です", "ます", "商売"],  # Lawrence's merchant speech
    "诺拉": ["ノラ", "えっと", "その"],
    "阿玛蒂": ["アマーティ", "君", "僕"],
}

def auto_extract(input_path, character, output_dir, min_dur=3, max_dur=30):
    """Auto-extract reference audio for a character."""
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Transcribing {input_path} with faster-whisper...")
    # First extract full audio
    full_audio = os.path.join(output_dir, "_temp_full.wav")
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-vn", "-ac", "1", "-ar", "16000", full_audio
    ], capture_output=True, check=True)
    
    transcript = transcribe_with_whisper(full_audio)
    print(f"Transcribed: {len(transcript)} segments")
    
    keywords = CHARACTER_KEYWORDS.get(character, [character])
    matches = find_character_segments(transcript, keywords)
    print(f"Found {len(matches)} potential {character} segments")
    
    # Extract clean clips
    extracted = []
    for i, match in enumerate(matches[:10]):  # max 10 clips
        dur = match["end"] - match["start"]
        if dur < min_dur or dur > max_dur:
            continue
        
        out_name = f"{character}_{i:02d}_{match['start']:.1f}s.wav"
        out_path = os.path.join(output_dir, out_name)
        
        try:
            extract_audio_segment(input_path, match["start"], dur, out_path)
            extracted.append({
                "file": out_name,
                "start": match["start"],
                "duration": dur,
                "text": match["text"],
                "keyword": match["keyword"],
            })
            print(f"  [{i+1}] {out_name} ({dur:.1f}s) <- {match['text'][:30]}")
        except subprocess.CalledProcessError:
            print(f"  [{i+1}] FAILED: {out_name}", file=sys.stderr)
    
    # Cleanup temp
    if os.path.exists(full_audio):
        os.unlink(full_audio)
    
    # Save manifest
    manifest_path = os.path.join(output_dir, f"{character}_ref_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(extracted, f, ensure_ascii=False, indent=2)
    
    print(f"\nExtracted {len(extracted)} clips for {character}")
    print(f"Manifest: {manifest_path}")
    print(f"\nNext step: listen to each clip and pick the best ones.")
    print(f"Rename good clips to: {character}_calm.wav, {character}_playful.wav, etc.")
    return extracted

def batch_extract(config_path, output_dir):
    """Batch extract from multiple sources for multiple characters."""
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
    
    for entry in config.get("sources", []):
        input_path = entry["file"]
        for character in entry.get("characters", []):
            print(f"\n{'='*60}")
            print(f"  Extracting: {character} from {input_path}")
            print(f"{'='*60}")
            auto_extract(input_path, character, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Extract reference audio for voice cloning")
    parser.add_argument("input", help="Input video/audio file, or batch config JSON with --batch")
    parser.add_argument("--character", help="Character name to extract")
    parser.add_argument("--output", default="data/ref-voices/", help="Output directory")
    parser.add_argument("--batch", action="store_true", help="Input is a batch config JSON")
    args = parser.parse_args()

    if args.batch:
        batch_extract(args.input, args.output)
    else:
        if not args.character:
            print("Error: --character required for single file mode", file=sys.stderr)
            sys.exit(1)
        auto_extract(args.input, args.character, args.output)

if __name__ == "__main__":
    main()
