#!/usr/bin/env python3
"""Shared Mify LLM client — avoids duplicating key loading and HTTP logic."""
import sys, os, json, urllib.request, time

sys.path.insert(0, os.path.expanduser("~/.codex/skills/mify-model-gateway/scripts"))
try:
    from _keyloader import load_mify_key
    _KEY = load_mify_key()
except SystemExit:
    _KEY = os.environ.get("MIFY_API_KEY", "")

MIFY_URL = "https://api.llm.mioffice.cn/v1/chat/completions"

def chat(model, messages, max_tokens=4000, temperature=0.1, timeout=60, retries=2):
    """Call Mify Gateway chat completions. Returns content string."""
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(MIFY_URL, data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {_KEY}"})
            resp = urllib.request.urlopen(req, timeout=timeout)
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            if attempt < retries:
                time.sleep(3)
                continue
            raise
