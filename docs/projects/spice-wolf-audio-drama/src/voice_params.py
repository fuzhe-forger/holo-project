#!/usr/bin/env python3
"""Voice guardrails -> TTS parameters converter.

Maps Holo's persona voice descriptions to structured TTS instruction parameters.
This is the first inter-dimension interface: text (voice guardrails) -> voice (TTS params).

Each character's voice description (from voice guardrails / profile) gets converted
to a parameter dict that CosyVoice/GPT-SoVITS/IndexTTS2 can consume.

Usage:
  from voice_params import get_tts_params
  params = get_tts_params("赫萝", "mischievous", 3)
  # -> {"emotion": "playful", "speed": 1.1, "volume": 0, "instruct": "..."}
"""
import json
import os

# ── Character voice profiles ──
# These are derived from Holo's voice guardrails and character traits.
# In production, these would be loaded from the Holo persona engine.

CHARACTER_VOICES = {
    "赫萝": {
        "voice_description": "成熟女性，略带沙哑，慵懒中带着狡黠，偶尔威严",
        "base_speed": 1.0,
        "base_volume": 0,
        "ref_audio": "ref-voices/holo_calm.wav",
        # Emotion-specific reference audio
        "emotion_refs": {
            "calm": "ref-voices/holo_calm.wav",
            "mischievous": "ref-voices/holo_playful.wav",
            "angry": "ref-voices/holo_angry.wav",
            "sad": "ref-voices/holo_sad.wav",
            "proud": "ref-voices/holo_proud.wav",
        },
    },
    "罗伦斯": {
        "voice_description": "成年男性，温和稳重，商人气质，偶尔慌张",
        "base_speed": 0.95,
        "base_volume": 0,
        "ref_audio": "ref-voices/lawrence_calm.wav",
        "emotion_refs": {
            "calm": "ref-voices/lawrence_calm.wav",
            "surprised": "ref-voices/lawrence_flustered.wav",
            "serious": "ref-voices/lawrence_serious.wav",
        },
    },
    "旁白": {
        "voice_description": "中性沉稳，说书人风格，语速偏慢",
        "base_speed": 0.85,
        "base_volume": 0,
        "ref_audio": "ref-voices/narrator.wav",
        "emotion_refs": {
            "calm": "ref-voices/narrator.wav",
        },
    },
}

# ── Emotion -> TTS parameter mapping ──
# This is the core translation: voice guardrail emotion words -> TTS instruct params.
# CosyVoice 3 supports: language, emotion, speed, volume instructions.
# IndexTTS2 supports: emotion disentanglement via style prompt.

EMOTION_PARAMS = {
    "calm":        {"tts_emotion": "neutral",   "speed_mod": 1.0,  "volume_mod": 0,  "instruct_prefix": ""},
    "happy":       {"tts_emotion": "happy",     "speed_mod": 1.1,  "volume_mod": 2,  "instruct_prefix": "语气轻快愉悦"},
    "angry":       {"tts_emotion": "angry",     "speed_mod": 1.15, "volume_mod": 5,  "instruct_prefix": "语气严厉愤怒"},
    "sad":         {"tts_emotion": "sad",       "speed_mod": 0.85, "volume_mod": -3, "instruct_prefix": "语气低落悲伤"},
    "surprised":   {"tts_emotion": "surprised", "speed_mod": 1.2,  "volume_mod": 3,  "instruct_prefix": "语气惊讶"},
    "fearful":     {"tts_emotion": "fearful",   "speed_mod": 0.9,  "volume_mod": -2, "instruct_prefix": "语气紧张恐惧"},
    "mischievous": {"tts_emotion": "playful",   "speed_mod": 1.1,  "volume_mod": 1,  "instruct_prefix": "语气狡黠俏皮，带着捉弄的意味"},
    "serious":     {"tts_emotion": "serious",   "speed_mod": 0.9,  "volume_mod": 1,  "instruct_prefix": "语气严肃认真"},
    "tender":      {"tts_emotion": "warm",      "speed_mod": 0.95, "volume_mod": -1, "instruct_prefix": "语气温柔亲昵"},
    "mocking":     {"tts_emotion": "playful",   "speed_mod": 1.05, "volume_mod": 1,  "instruct_prefix": "语气嘲讽戏谑"},
    "proud":       {"tts_emotion": "proud",     "speed_mod": 0.95, "volume_mod": 2,  "instruct_prefix": "语气高傲自信，带着威严"},
}

DEFAULT_VOICE = {
    "voice_description": "中性声音",
    "base_speed": 1.0,
    "base_volume": 0,
    "ref_audio": None,
    "emotion_refs": {},
}


def get_tts_params(speaker, emotion, intensity=3, scene=None):
    """Convert voice guardrail descriptors to TTS-executable parameters.
    
    This is the inter-dimension interface: text persona -> voice params.
    
    Returns dict with:
      - ref_audio: path to reference audio for this speaker+emotion
      - speed: float (0.5-2.0)
      - volume: int (-10 to 10, dB adjustment)
      - emotion: TTS emotion label
      - instruct: full instruction string for CosyVoice instruct mode
      - voice_description: human-readable voice description
    """
    voice = CHARACTER_VOICES.get(speaker, DEFAULT_VOICE)
    emo = EMOTION_PARAMS.get(emotion, EMOTION_PARAMS["calm"])
    
    # Intensity scales speed and volume deviation
    intensity_factor = intensity / 3.0  # 1-5 -> 0.33-1.67
    
    speed = voice["base_speed"] * emo["speed_mod"]
    # Clamp speed
    speed = max(0.5, min(2.0, speed))
    
    volume = voice["base_volume"] + int(emo["volume_mod"] * intensity_factor)
    
    # Pick reference audio: emotion-specific if available, else base
    ref_audio = voice["emotion_refs"].get(emotion) or voice.get("ref_audio")
    
    # Build instruction string for CosyVoice instruct mode
    instruct_parts = []
    if emo["instruct_prefix"]:
        instruct_parts.append(emo["instruct_prefix"])
    if voice["voice_description"]:
        instruct_parts.append(voice["voice_description"])
    instruct = "，".join(instruct_parts) if instruct_parts else None
    
    return {
        "ref_audio": ref_audio,
        "speed": round(speed, 2),
        "volume": volume,
        "emotion": emo["tts_emotion"],
        "instruct": instruct,
        "voice_description": voice["voice_description"],
        "speaker": speaker,
        "emotion_input": emotion,
        "intensity": intensity,
        "scene": scene,
    }


def annotate_script(segments):
    """Take annotated segments from annotate.py, add TTS params to each."""
    for seg in segments:
        speaker = seg.get("speaker") or "旁白"
        emotion = seg.get("emotion", "calm")
        intensity = seg.get("emotion_intensity", 3)
        scene = seg.get("scene")
        
        seg["tts_params"] = get_tts_params(speaker, emotion, intensity, scene)
    
    return segments


if __name__ == "__main__":
    # Demo: show parameter conversion for all character-emotion combos
    print("=== Voice Guardrails -> TTS Params Conversion Demo ===\n")
    
    test_cases = [
        ("赫萝", "mischievous", 3),
        ("赫萝", "proud", 4),
        ("赫萝", "calm", 2),
        ("赫萝", "angry", 5),
        ("罗伦斯", "calm", 3),
        ("罗伦斯", "surprised", 4),
        ("旁白", "calm", 2),
    ]
    
    for speaker, emotion, intensity in test_cases:
        params = get_tts_params(speaker, emotion, intensity)
        print(f"[{speaker}] emotion={emotion} intensity={intensity}")
        print(f"  speed={params['speed']} volume={params['volume']} tts_emotion={params['emotion']}")
        print(f"  instruct: {params['instruct']}")
        print(f"  ref_audio: {params['ref_audio']}")
        print()
