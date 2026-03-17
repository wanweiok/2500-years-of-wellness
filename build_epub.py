"""Build KDP-ready EPUB for the English edition.

Uses Pandoc directly — SVG diagrams are embedded as-is (KDP handles conversion).
"""
import os, re, subprocess, shutil
from pathlib import Path

ROOT = Path(__file__).parent
IMG_DIR = ROOT / "images"
KINDLE_DIR = ROOT / "kindle"

CHAPTERS_EN = [
    "ch00-preface-en.md",
    "ch01-oldest-conversation-en.md",
    "ch02-living-in-rhythm-en.md",
    "ch03-food-as-medicine-en.md",
    "ch04-emotional-body-en.md",
    "ch05-moving-like-water-en.md",
    "ch06-art-of-prevention-en.md",
    "ch07-yin-yang-balance-en.md",
    "ch08-sleep-healer-en.md",
    "ch09-invisible-network-en.md",
    "ch10-breath-and-posture-en.md",
    "ch11-ai-meets-tcm-en.md",
]


def prepare_chapters():
    """Copy and fix image paths in each chapter markdown."""
    KINDLE_DIR.mkdir(parents=True, exist_ok=True)
    img_dest = KINDLE_DIR / "images"
    img_dest.mkdir(exist_ok=True)

    for svg in IMG_DIR.glob("*-en.svg"):
        shutil.copy2(svg, img_dest / svg.name)
    for svg in IMG_DIR.glob("*-en.png"):
        shutil.copy2(svg, img_dest / svg.name)

    cover_src = IMG_DIR / "kdp-cover-en.png"
    if not cover_src.exists():
        cover_src = IMG_DIR / "book-cover-final.png"
    if cover_src.exists():
        shutil.copy2(cover_src, KINDLE_DIR / "cover.png")
        print(f"  Cover: {cover_src.name} -> cover.png")

    chapters = []
    for fname in CHAPTERS_EN:
        src = ROOT / fname
        if not src.exists():
            print(f"  SKIP: {fname} not found")
            continue

        text = src.read_text(encoding="utf-8")
        text = text.replace("./images/", "images/")

        out = KINDLE_DIR / fname
        out.write_text(text, encoding="utf-8")
        chapters.append(str(out))
        print(f"  Prepared: {fname}")

    return chapters


def write_metadata():
    """Write Pandoc EPUB metadata YAML."""
    path = KINDLE_DIR / "metadata.yaml"
    path.write_text("""---
title: "2,500 Years of Wellness"
subtitle: "The Yellow Emperor's Guide to Living Well"
author: "Wan Wei"
lang: en-US
description: >
  A modern wellness guide based on the Huangdi Neijing,
  the world's oldest surviving medical text. Bridges ancient
  Chinese medicine with contemporary science across 11 chapters
  covering circadian rhythm, nutrition, emotions, movement,
  prevention, sleep, meridians, breath, and AI-powered wellness.
subject: "Health & Wellness / Traditional Chinese Medicine"
rights: "Copyright 2026 Wan Wei. All rights reserved."
cover-image: cover.png
toc-title: "Table of Contents"
---
""", encoding="utf-8")
    print(f"  Metadata: {path.name}")
    return path


def build_epub(chapter_files, meta_path):
    """Run Pandoc to produce EPUB."""
    epub_path = KINDLE_DIR / "2500-Years-of-Wellness.epub"

    cmd = [
        "pandoc",
        *chapter_files,
        "--metadata-file", str(meta_path),
        "-o", str(epub_path),
        "--toc",
        "--toc-depth=2",
        "--epub-chapter-level=1",
        "--wrap=none",
    ]

    cover = KINDLE_DIR / "cover.png"
    if cover.exists():
        cmd.extend(["--epub-cover-image", str(cover)])

    print(f"  Pandoc: {len(chapter_files)} files -> {epub_path.name}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(KINDLE_DIR))

    if result.stderr:
        for line in result.stderr.strip().split("\n")[:10]:
            print(f"  WARN: {line}")

    if result.returncode != 0:
        raise RuntimeError(f"Pandoc failed (exit {result.returncode})")

    size_kb = epub_path.stat().st_size / 1024
    print(f"  Built: {epub_path.name} ({size_kb:.0f} KB)")
    return epub_path


if __name__ == "__main__":
    print("=" * 50)
    print("Building KDP EPUB — English Edition")
    print("=" * 50)

    print("\n[1/3] Preparing chapters and images...")
    chapters = prepare_chapters()

    print("\n[2/3] Writing metadata...")
    meta = write_metadata()

    print("\n[3/3] Building EPUB with Pandoc...")
    epub = build_epub(chapters, meta)

    print("\n" + "=" * 50)
    print(f"EPUB ready: {epub}")
    print(f"Upload to: https://kdp.amazon.com")
    print("=" * 50)
