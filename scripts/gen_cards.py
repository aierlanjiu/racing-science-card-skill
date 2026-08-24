#!/usr/bin/env python3
"""Safely export racing-card prompts from JSON to text files.

This helper is intentionally offline. It never reads credentials and never
calls a model or an image service.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-.")
    return slug or "prompt"


def load_prompts(path: Path) -> dict[str, str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not payload:
        raise ValueError("prompts.json must be a non-empty object")
    prompts: dict[str, str] = {}
    for key, value in payload.items():
        if not isinstance(key, str) or not isinstance(value, str) or not value.strip():
            raise ValueError("every prompt entry must map a string name to non-empty text")
        prompts[key] = value.strip() + "\n"
    return prompts


def export_prompts(prompts: dict[str, str], output_dir: Path) -> list[dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, object]] = []
    used: set[str] = set()

    for index, (name, prompt) in enumerate(prompts.items(), start=1):
        base = safe_slug(name)
        filename = f"{index:02d}-{base}.txt"
        if filename in used:
            digest = hashlib.sha256(name.encode("utf-8")).hexdigest()[:8]
            filename = f"{index:02d}-{base}-{digest}.txt"
        used.add(filename)

        destination = output_dir / filename
        destination.write_text(prompt, encoding="utf-8")
        manifest.append(
            {
                "name": name,
                "file": filename,
                "characters": len(prompt.rstrip("\n")),
                "sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            }
        )

    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Export racing-card prompts without network access")
    parser.add_argument("prompts_json", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    prompts = load_prompts(args.prompts_json)
    manifest = export_prompts(prompts, args.output_dir)
    print(f"Exported {len(manifest)} prompt files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
