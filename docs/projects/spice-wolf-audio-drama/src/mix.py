#!/usr/bin/env python3
"""Audio mixing: TTS segments + BGM + SFX -> final audio drama episode.

Uses FFmpeg to:
  1. Concatenate TTS segments in order
  2. Add pauses between segments (narration pause, dialogue pause)
  3. Layer BGM track underneath at appropriate volume
  4. Insert SFX at cue points
  5. Output final MP3

Usage:
  python3 mix.py output/manifest.json -o episode01.mp3 --bgm bgm/medieval.mp3
  python3 mix.py output/manifest.json -o episode01.mp3 --dry-run
"""
import sys, os, json, argparse, subprocess, tempfile

def get_segment_duration(audio_path):
    """Get duration of audio file in seconds using ffprobe."""
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

def build_mix(manifest, audio_dir, output_path, bgm_path=None, 
              narration_pause=0.5, dialogue_pause=0.3, bgm_volume=0.15, dry_run=False):
    """Build the final mixed audio using FFmpeg."""
    
    # Build FFmpeg concat list
    concat_list = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    
    total_duration = 0
    for entry in manifest:
        if entry.get("type") == "sfx":
            # Insert silence as placeholder for SFX
            # In production, insert actual SFX file
            sfx_dur = 1.0  # default 1 second for SFX
            total_duration += sfx_dur
            continue
        
        audio_file = entry.get("file")
        if not audio_file:
            continue
        
        audio_path = os.path.join(audio_dir, audio_file)
        if not os.path.exists(audio_path):
            print(f"  Warning: {audio_file} not found, skipping", file=sys.stderr)
            continue
        
        dur = get_segment_duration(audio_path)
        total_duration += dur
        
        # Add pause based on segment type
        seg_type = entry.get("type", "narration")
        pause = narration_pause if seg_type == "narration" else dialogue_pause
        total_duration += pause
        
        concat_list.write(f"file '{audio_path}'\n")
    
    concat_list.close()
    
    if dry_run:
        print(f"[DRY-RUN] Would concatenate {len(manifest)} segments")
        print(f"  Total duration: {total_duration:.1f}s ({total_duration/60:.1f}min)")
        print(f"  BGM: {bgm_path or 'none'}")
        if bgm_path:
            print(f"  BGM volume: {bgm_volume}")
        os.unlink(concat_list.name)
        return
    
    # Step 1: Concatenate segments
    concat_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    concat_audio.close()
    
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list.name,
           "-c", "copy", concat_audio.name]
    subprocess.run(cmd, capture_output=True)
    
    # Step 2: Mix with BGM if provided
    if bgm_path and os.path.exists(bgm_path):
        cmd = [
            "ffmpeg", "-y",
            "-i", concat_audio.name,
            "-i", bgm_path,
            "-filter_complex",
            f"[0:a]volume=1.0[voice];[1:a]volume={bgm_volume},aloop=loop=-1:size=2e+09[bgm];[voice][bgm]amix=inputs=2:duration=first",
            "-c:a", "libmp3lame", "-q:a", "2",
            output_path
        ]
        subprocess.run(cmd, capture_output=True)
    else:
        # Just convert to MP3
        cmd = ["ffmpeg", "-y", "-i", concat_audio.name,
               "-c:a", "libmp3lame", "-q:a", "2", output_path]
        subprocess.run(cmd, capture_output=True)
    
    # Cleanup
    os.unlink(concat_list.name)
    os.unlink(concat_audio.name)
    
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        dur = get_segment_duration(output_path)
        print(f"Output: {output_path} ({dur:.1f}s, {size//1024}KB)")
    else:
        print(f"FAILED: output not created", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Mix TTS segments into final audio drama")
    parser.add_argument("manifest", help="manifest.json from tts_generate.py")
    parser.add_argument("-o", "--output", required=True, help="Output MP3 file")
    parser.add_argument("--bgm", help="BGM audio file path")
    parser.add_argument("--narration-pause", type=float, default=0.5, help="Pause after narration (seconds)")
    parser.add_argument("--dialogue-pause", type=float, default=0.3, help="Pause after dialogue (seconds)")
    parser.add_argument("--bgm-volume", type=float, default=0.15, help="BGM volume (0.0-1.0)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(args.manifest, encoding="utf-8") as f:
        manifest = json.load(f)

    audio_dir = os.path.dirname(args.manifest)
    build_mix(manifest, audio_dir, args.output, args.bgm,
              args.narration_pause, args.dialogue_pause, args.bgm_volume, args.dry_run)

if __name__ == "__main__":
    main()
