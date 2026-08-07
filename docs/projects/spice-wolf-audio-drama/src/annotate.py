#!/usr/bin/env python3
"""Text annotation pipeline: novel text -> structured script JSON.

Uses LLM (Mify Gateway) to identify speakers, emotions, scenes, and SFX cues.
Splits narration from dialogue — narration is speaker=null, type="narration".

Usage:
  python3 annotate.py input.txt -o output.json
  python3 annotate.py input.txt -o output.json --model zhipuai/glm-4.5
"""
import sys, os, json, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_client import chat

DEFAULT_MODEL = "zhipuai/glm-4.5"

PROMPT_SYSTEM = """You are a script supervisor for an audio drama production. Given a passage of Chinese novel text, break it into segments and annotate each one.

CRITICAL RULE — Narration vs Dialogue separation:
- Narration (description, action, environment, internal thought attributed to narrator) MUST be type="narration", speaker=null.
- Only text that is ACTUALLY SPOKEN ALOUD by a character is type="dialogue" or "monologue".
- A paragraph that mixes narration and dialogue MUST be split into separate segments.
- Example: '罗伦斯叹了口气。"又怎么了？"他说。' -> TWO segments:
  1. {"text": "罗伦斯叹了口气。", "type": "narration", "speaker": null, ...}
  2. {"text": "又怎么了？", "type": "dialogue", "speaker": "罗伦斯", ...}
  3. {"text": "他说。", "type": "narration", "speaker": null, ...}
- Dialogue markers: quotes (""), 「」, or obvious spoken text. Everything else is narration.

Output format: a JSON array. Each element:
{
  "text": "original text (verbatim, no modifications)",
  "type": "narration" | "dialogue" | "monologue" | "sound_effect",
  "speaker": "character name or null for narration",
  "emotion": "calm" | "happy" | "angry" | "sad" | "surprised" | "fearful" | "mischievous" | "serious" | "tender" | "mocking" | "proud",
  "emotion_intensity": 1-5,
  "scene": "brief scene description for BGM selection",
  "sfx_cue": "sound effect cue or null"
}

Rules:
- Keep text verbatim. Do NOT rewrite, translate, or summarize.
- Split at natural boundaries: speaker changes, narration to dialogue, scene shifts.
- Each segment should be 20-500 characters.
- Identify the speaker from context. If unclear, use "unknown".
- Sound effects in text (e.g. "*snap*") become type="sound_effect".
- Emotion for narration reflects the mood of the scene, not a character's emotion.
- Scene: "market", "forest_night", "tavern", "travel_road", etc.
- Output ONLY the JSON array, no explanation, no markdown fences.
"""

def annotate_chunk(text, model=DEFAULT_MODEL):
    content = chat(model, [
        {"role": "system", "content": PROMPT_SYSTEM},
        {"role": "user", "content": f"Annotate this passage:\n\n{text}"},
    ], max_tokens=8000, temperature=0.1)
    
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1] if "\n" in content else content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    segments = json.loads(content)
    return segments if isinstance(segments, list) else [segments]

def split_text(text, max_chars=2000):
    paragraphs = text.split("\n\n")
    chunks, current = [], ""
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if len(current) + len(p) + 2 > max_chars and current:
            chunks.append(current.strip())
            current = p
        else:
            current = (current + "\n\n" + p) if current else p
    if current.strip():
        chunks.append(current.strip())
    return chunks

def main():
    parser = argparse.ArgumentParser(description="Annotate novel text for audio drama")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("-o", "--output", required=True, help="Output JSON file")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        text = f.read()

    chunks = split_text(text)
    print(f"Input: {len(text)} chars, {len(chunks)} chunks")

    all_segments = []
    for i, chunk in enumerate(chunks):
        print(f"  [{i+1}/{len(chunks)}] ({len(chunk)} chars)...", end="", flush=True)
        segments = annotate_chunk(chunk, args.model)
        print(f" {len(segments)} segments")
        all_segments.extend(segments)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(all_segments, f, ensure_ascii=False, indent=2)

    speakers, emotions, types = {}, {}, {}
    for seg in all_segments:
        sp = seg.get("speaker") or "narrator"
        speakers[sp] = speakers.get(sp, 0) + 1
        em = seg.get("emotion", "unknown")
        emotions[em] = emotions.get(em, 0) + 1
        ty = seg.get("type", "unknown")
        types[ty] = types.get(ty, 0) + 1

    print(f"\nTotal: {len(all_segments)} segments")
    print(f"Types: {dict(sorted(types.items(), key=lambda x: -x[1]))}")
    print(f"Speakers: {dict(sorted(speakers.items(), key=lambda x: -x[1]))}")
    print(f"Emotions: {dict(sorted(emotions.items(), key=lambda x: -x[1]))}")

if __name__ == "__main__":
    main()
