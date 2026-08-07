#!/usr/bin/env python3
"""End-to-end MVP pipeline: text -> annotate -> TTS params -> generate -> mix.

Usage:
  python3 run_pipeline.py input.txt -o output/ --dry-run
  python3 run_pipeline.py input.txt -o output/ --backend cosyvoice
"""
import sys, os, json, argparse, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

def run(cmd, desc):
    print(f"\n{'='*60}")
    print(f"  {desc}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"FAILED: {desc}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="End-to-end audio drama pipeline")
    parser.add_argument("input", help="Input novel text file")
    parser.add_argument("-o", "--output", default="output", help="Output directory")
    parser.add_argument("--backend", default="cosyvoice", choices=["cosyvoice", "gptsovits"])
    parser.add_argument("--dry-run", action="store_true", help="Skip actual TTS and mixing")
    parser.add_argument("--model", default="zhipuai/glm-4.5", help="LLM model for annotation")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    
    script_path = os.path.join(args.output, "script.json")
    audio_dir = os.path.join(args.output, "audio")
    episode_path = os.path.join(args.output, "episode.mp3")

    # Step 1: Annotate
    run([
        sys.executable, os.path.join(HERE, "annotate.py"),
        args.input, "-o", script_path, "--model", args.model
    ], "Step 1: Text annotation (LLM)")

    # Step 2: Generate TTS
    run([
        sys.executable, os.path.join(HERE, "tts_generate.py"),
        script_path, "-o", audio_dir,
        "--backend", args.backend
    ] + (["--dry-run"] if args.dry_run else []), "Step 2: TTS generation")

    # Step 3: Mix
    manifest_path = os.path.join(audio_dir, "manifest.json")
    if os.path.exists(manifest_path):
        run([
            sys.executable, os.path.join(HERE, "mix.py"),
            manifest_path, "-o", episode_path
        ] + (["--dry-run"] if args.dry_run else []), "Step 3: Audio mixing")

    print(f"\n{'='*60}")
    print(f"  Pipeline complete!")
    print(f"  Script: {script_path}")
    print(f"  Audio:  {audio_dir}/")
    print(f"  Episode: {episode_path}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
