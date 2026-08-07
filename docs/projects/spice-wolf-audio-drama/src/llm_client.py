#!/usr/bin/env python3
"""Shared LLM client — DeepSeek API (migrated from Mify Gateway)."""
import os, json, urllib.request, time, ssl

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
_KEY = "sk-6b1c933160de49f5bfcc6e1a173adc5f"
_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE

# Model mapping: old Mify owner/id → DeepSeek model
_MODEL_MAP = {
    "zhipuai/glm-4.5": "deepseek-chat",
    "deepseek-chat": "deepseek-chat",
}

def chat(model, messages, max_tokens=4000, temperature=0.1, timeout=60, retries=2):
    """Call DeepSeek chat completions. Returns content string."""
    ds_model = _MODEL_MAP.get(model, "deepseek-chat")
    payload = {"model": ds_model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(DEEPSEEK_URL, data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {_KEY}"})
            resp = urllib.request.urlopen(req, timeout=timeout, context=_CTX)
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            if attempt < retries:
                time.sleep(3)
                continue
            raise
