#!/usr/bin/env python3
"""
赛车科普卡片批量生成 — Codex gpt-image-2 pipeline
依赖: Hermes Agent (Codex OAuth token 读取)
用法: python3 gen_cards.py <prompts.json路径> <输出目录>
"""

import json, sys, os, base64

# === 配置：根据你的 Hermes 安装路径修改 ===
HERMES_AGENT_PATH = os.path.expanduser("~/.hermes/hermes-agent")
# =============================================

sys.path.insert(0, HERMES_AGENT_PATH)
os.chdir(HERMES_AGENT_PATH)

from agent.auxiliary_client import _read_codex_access_token, _codex_cloudflare_headers
import openai

QUALITY = "high"
API_MODEL = "gpt-image-2"
CHAT_MODEL = "gpt-5.4"
BASE_URL = "https://chatgpt.com/backend-api/codex"
INSTRUCTIONS = (
    "You are an assistant that must fulfill image generation requests "
    "by using the image_generation tool when provided."
)


def gen_card(prompt: str, output_path: str) -> bool:
    """生成单张卡片，返回是否成功"""
    token = _read_codex_access_token()
    if not token:
        print("No Codex token — is Codex.app running and logged in?")
        return False

    client = openai.OpenAI(
        api_key=token,
        base_url=BASE_URL,
        default_headers=_codex_cloudflare_headers(token),
    )

    image_b64 = None
    try:
        with client.responses.stream(
            model=CHAT_MODEL,
            store=False,
            instructions=INSTRUCTIONS,
            input=[{
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": prompt}],
            }],
            tools=[{
                "type": "image_generation",
                "model": API_MODEL,
                "size": "1024x1536",
                "quality": QUALITY,
                "output_format": "png",
                "background": "opaque",
                "partial_images": 1,
            }],
            tool_choice={
                "type": "allowed_tools",
                "mode": "required",
                "tools": [{"type": "image_generation"}],
            },
        ) as stream:
            for event in stream:
                et = getattr(event, "type", "")
                if et == "response.output_item.done":
                    item = getattr(event, "item", None)
                    if getattr(item, "type", None) == "image_generation_call":
                        result = getattr(item, "result", None)
                        if isinstance(result, str) and result:
                            image_b64 = result
                elif et == "response.image_generation_call.partial_image":
                    partial = getattr(event, "partial_image_b64", None)
                    if isinstance(partial, str) and partial:
                        image_b64 = partial
            final = stream.get_final_response()

        for item in getattr(final, "output", None) or []:
            if getattr(item, "type", None) == "image_generation_call":
                result = getattr(item, "result", None)
                if isinstance(result, str) and result:
                    image_b64 = result

        if not image_b64:
            print(f"   No image in response")
            return False

        img_bytes = base64.b64decode(image_b64)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(img_bytes)
        print(f"   Saved: {os.path.basename(output_path)} ({len(img_bytes)/1024:.0f} KB)")
        return True

    except Exception as e:
        print(f"   Failed: {e}")
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 gen_cards.py <prompts.json> <output_dir>")
        print()
        print("prompts.json format:")
        print('  {"filename.png": "prompt text", ...}')
        sys.exit(1)

    prompts_file = sys.argv[1]
    out_dir = sys.argv[2]

    with open(prompts_file) as f:
        prompts = json.load(f)

    ok = 0
    for filename, prompt in prompts.items():
        print(f"\n{'='*60}")
        print(f"Generating: {filename} ({len(prompt)} chars)")
        if gen_card(prompt, os.path.join(out_dir, filename)):
            ok += 1

    print(f"\nDone: {ok}/{len(prompts)} generated → {out_dir}/")


if __name__ == "__main__":
    main()
