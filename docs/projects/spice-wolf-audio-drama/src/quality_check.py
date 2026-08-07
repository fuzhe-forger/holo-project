#!/usr/bin/env python3
"""Audio quality check: reverse-transcribe generated audio and compare with original text.

Uses faster-whisper to transcribe generated WAV files, then compares the
transcription with the original text from the script JSON. Flags:
  - Missing words / extra words
  - Wrong characters (homophone errors)
  - Empty / silent audio
  - Duration anomalies (too short = truncated, too long = repetition)

Usage:
  python3 quality_check.py output/audio/manifest.json data/text/sample_script.json
  python3 quality_check.py output/audio/manifest.json data/text/sample_script.json --threshold 0.7
"""
import sys, os, json, argparse, subprocess, re, difflib

def get_audio_duration(audio_path):
    """Get duration in seconds via ffprobe."""
    if not os.path.exists(audio_path):
        return 0
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
        capture_output=True, text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0

def transcribe_audio(audio_path, language="zh"):
    """Transcribe generated audio with faster-whisper."""
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("small", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_path, language=language, vad_filter=True)
        return " ".join(seg.text.strip() for seg in segments)
    except ImportError:
        print("faster-whisper not installed. Install: pip install faster-whisper", file=sys.stderr)
        sys.exit(1)

def normalize_text(text):
    """Normalize Chinese text for comparison: remove punctuation, whitespace."""
    # Remove punctuation (Chinese and English)
    text = re.sub(r'[，。！？、；：""''「」（）()\[\]{},.!?;:\s]', '', text)
    return text.lower()

def calculate_similarity(text1, text2):
    """Calculate character-level similarity ratio."""
    n1, n2 = normalize_text(text1), normalize_text(text2)
    if not n1 or not n2:
        return 0.0
    return difflib.SequenceMatcher(None, n1, n2).ratio()

def find_errors(original, transcribed):
    """Find specific error types between original and transcribed text."""
    n_orig = normalize_text(original)
    n_trans = normalize_text(transcribed)
    
    if not n_trans:
        return {"type": "empty", "message": "Audio produced no transcription (silent/failed)"}
    
    # Check for truncation (transcribed much shorter than original)
    if len(n_trans) < len(n_orig) * 0.5:
        return {"type": "truncated", "message": f"Audio likely truncated: {len(n_trans)} vs {len(n_orig)} chars"}
    
    # Check for repetition (transcribed much longer)
    if len(n_trans) > len(n_orig) * 2:
        return {"type": "repetition", "message": f"Audio may contain repetition: {len(n_trans)} vs {len(n_orig)} chars"}
    
    # Find character-level diffs
    diff = difflib.SequenceMatcher(None, n_orig, n_trans)
    errors = []
    for tag, i1, i2, j1, j2 in diff.get_opcodes():
        if tag == 'replace':
            errors.append(f"substitution: '{n_orig[i1:i2]}' -> '{n_trans[j1:j2]}'")
        elif tag == 'delete':
            errors.append(f"missing in audio: '{n_orig[i1:i2]}'")
        elif tag == 'insert':
            errors.append(f"extra in audio: '{n_trans[j1:j2]}'")
    
    if errors:
        return {"type": "char_errors", "errors": errors[:5], "total": len(errors)}
    
    return None

def check_segment(original_text, audio_path, duration, similarity_threshold=0.7):
    """Run all quality checks on one segment."""
    issues = []
    
    # Check 1: file exists and has content
    if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 100:
        issues.append({"check": "file", "severity": "critical", 
                       "message": "Audio file missing or empty"})
        return issues
    
    # Check 2: duration sanity
    if duration < 0.5:
        issues.append({"check": "duration", "severity": "critical",
                       "message": f"Audio too short: {duration:.1f}s"})
    elif duration > 300:
        issues.append({"check": "duration", "severity": "warning",
                       "message": f"Audio very long: {duration:.1f}s, check for repetition"})
    
    # Check 3: reverse transcription similarity
    transcribed = transcribe_audio(audio_path)
    similarity = calculate_similarity(original_text, transcribed)
    
    if similarity < similarity_threshold:
        error_detail = find_errors(original_text, transcribed)
        issues.append({
            "check": "transcription_similarity",
            "severity": "critical" if similarity < 0.5 else "warning",
            "similarity": round(similarity, 3),
            "transcribed": transcribed[:100],
            "error_detail": error_detail,
        })
    
    # Check 4: estimated speech rate (chars per second)
    char_count = len(normalize_text(original_text))
    if duration > 0:
        rate = char_count / duration
        if rate > 8:  # too fast
            issues.append({"check": "speech_rate", "severity": "warning",
                           "message": f"Speech too fast: {rate:.1f} chars/s"})
        elif rate < 2 and char_count > 10:  # too slow
            issues.append({"check": "speech_rate", "severity": "warning",
                           "message": f"Speech too slow: {rate:.1f} chars/s"})
    
    return issues

def main():
    parser = argparse.ArgumentParser(description="Quality check generated audio")
    parser.add_argument("manifest", help="manifest.json from tts_generate.py")
    parser.add_argument("script", help="Original script JSON")
    parser.add_argument("--audio-dir", default=None, help="Audio directory (default: manifest dir)")
    parser.add_argument("--threshold", type=float, default=0.7, help="Similarity threshold")
    parser.add_argument("--output", default=None, help="Output report JSON")
    args = parser.parse_args()

    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)
    with open(args.script, encoding="utf-8") as f:
        script = json.load(f)
    
    audio_dir = args.audio_dir or os.path.dirname(args.manifest)
    
    # Build index: script index -> text
    script_texts = {i: seg["text"] for i, seg in enumerate(script)}
    
    report = {
        "total": len(manifest),
        "checked": 0,
        "passed": 0,
        "warning": 0,
        "critical": 0,
        "skipped": 0,
        "segments": [],
    }
    
    print(f"Checking {len(manifest)} segments (threshold={args.threshold})\n")
    
    for entry in manifest:
        idx = entry.get("index", 0)
        audio_file = entry.get("file")
        
        if not audio_file or entry.get("type") == "sfx":
            report["skipped"] += 1
            continue
        
        audio_path = os.path.join(audio_dir, audio_file)
        original_text = script_texts.get(idx, "")
        
        if not original_text:
            print(f"  [{idx}] No original text found, skipping")
            report["skipped"] += 1
            continue
        
        dur = get_audio_duration(audio_path)
        print(f"  [{idx}] {audio_file} ({dur:.1f}s) ", end="", flush=True)
        
        issues = check_segment(original_text, audio_path, dur, args.threshold)
        
        if not issues:
            print("PASS")
            report["passed"] += 1
        else:
            severities = [i["severity"] for i in issues]
            if "critical" in severities:
                print("CRITICAL")
                report["critical"] += 1
            else:
                print("WARNING")
                report["warning"] += 1
            
            for issue in issues:
                print(f"       {issue['check']}: {issue.get('message', issue)}")
        
        report["checked"] += 1
        report["segments"].append({
            "index": idx,
            "file": audio_file,
            "duration": round(dur, 2),
            "issues": issues,
        })
    
    print(f"\n{'='*60}")
    print(f"  Checked: {report['checked']} | PASS: {report['passed']} | "
          f"WARNING: {report['warning']} | CRITICAL: {report['critical']} | "
          f"SKIP: {report['skipped']}")
    print(f"{'='*60}")
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Report: {args.output}")
    else:
        # Save next to manifest
        report_path = os.path.join(audio_dir, "quality_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Report: {report_path}")

if __name__ == "__main__":
    main()
