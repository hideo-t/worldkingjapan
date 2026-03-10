#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界王 OGP/Twitter Card 一括パッチ
- 全235話の詳細ページに og:title / og:description / og:image / twitter:card を注入
- index.html (トップ) のOGPも強化
使い方:
  python patch_ogp.py              # 全235ファイル + index.html
  python patch_ogp.py --dry-run    # 確認のみ
  python patch_ogp.py --pref 東京  # 1県だけ
  python patch_ogp.py --force      # 注入済みも強制上書き
"""

import argparse, re, sys
from pathlib import Path

try:
    from world_kings_data import PREFECTURES
except ImportError:
    print("❌ world_kings_data.py が見つかりません。worldkingjapan フォルダで実行してください。")
    sys.exit(1)

OUTPUT_BASE = Path("worldkings_output")
BASE_URL    = "https://hideo-t.github.io/worldkingjapan"
MARKER      = "<!-- ogp-injected -->"


def make_detail_ogp(pref_name: str, wl_key: str) -> str:
    """各詳細ページ用のOGPタグを生成"""
    pref     = PREFECTURES.get(pref_name, {})
    kingdom  = pref.get("kingdom", pref_name)
    question = pref.get("question", "")
    wl_value = pref.get("world_lines", {}).get(wl_key, wl_key)

    folder   = f"{pref_name}_{wl_key}"
    page_url = f"{BASE_URL}/worldkings_output/{folder}/index.html"
    # サムネイル: chapter_01.webp → なければ chapter_01.png
    img_url  = f"{BASE_URL}/worldkings_output/{folder}/thumbs/chapter_01.webp"

    title = f"{pref_name}〈{wl_key}〉{wl_value} ── 世界王"
    desc  = f"「{question}」{pref_name}を舞台にしたAIファンタジー小説。世界線：{wl_key}（{wl_value}）"

    # XSS対策
    def esc(s): return s.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

    return f"""{MARKER}
<meta property="og:type"        content="article">
<meta property="og:site_name"   content="世界王 World Kings">
<meta property="og:url"         content="{esc(page_url)}">
<meta property="og:title"       content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image"       content="{esc(img_url)}">
<meta property="og:locale"      content="ja_JP">
<meta name="twitter:card"       content="summary_large_image">
<meta name="twitter:title"      content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image"      content="{esc(img_url)}">
<meta name="description"        content="{esc(desc)}">"""


def make_index_ogp() -> str:
    """トップページ用OGPタグ"""
    title   = "世界王 World Kings ── Mysterious Japan"
    desc    = "47都道府県 × 5世界線 = 235話。AIが生成した日本ファンタジー小説コレクション。"
    img_url = f"{BASE_URL}/japan_map.png"
    page_url= f"{BASE_URL}/"

    return f"""{MARKER}
<meta property="og:type"        content="website">
<meta property="og:site_name"   content="世界王 World Kings">
<meta property="og:url"         content="{page_url}">
<meta property="og:title"       content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image"       content="{img_url}">
<meta property="og:locale"      content="ja_JP">
<meta name="twitter:card"       content="summary_large_image">
<meta name="twitter:title"      content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image"      content="{img_url}">"""


def patch_file(html_path: Path, new_ogp: str, dry_run: bool, force: bool) -> str:
    try:
        content = html_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"error（{e}）"

    if "<head>" not in content and "<head " not in content:
        return "skipped（<head>なし）"

    already = MARKER in content
    if already and not force:
        return "already"

    if already:
        # 既存OGPブロックを削除
        content = re.sub(
            re.escape(MARKER) + r'.*?(?=\n<meta(?! name="viewport")|\n</head>|\n<title)',
            '', content, flags=re.DOTALL
        )

    # <title> の直前に挿入
    if "<title>" in content:
        content = content.replace("<title>", new_ogp + "\n<title>", 1)
    else:
        content = re.sub(r'(<head[^>]*>)', r'\1\n' + new_ogp, content, count=1)

    if not dry_run:
        html_path.write_text(content, encoding="utf-8")

    return "updated" if already else "injected"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--pref",  default="")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--skip-index", action="store_true", help="index.htmlをスキップ")
    args = parser.parse_args()

    results = {}

    # ── トップページ ──
    if not args.pref and not args.skip_index:
        index_path = Path("index.html")
        if index_path.exists():
            res = patch_file(index_path, make_index_ogp(), args.dry_run, args.force)
            icon = {"injected":"✅","updated":"🔄","already":"⏭","skipped":"⚠","error":"❌"}.get(res.split("（")[0],"?")
            print(f"  {icon} index.html → {res}")
            results[res.split("（")[0]] = results.get(res.split("（")[0], 0) + 1
        else:
            print("  ⚠ index.html が見つかりません（スキップ）")

    # ── 詳細ページ235本 ──
    if not OUTPUT_BASE.exists():
        print(f"❌ {OUTPUT_BASE} が見つかりません。worldkingjapan フォルダで実行してください。")
        sys.exit(1)

    targets = []
    for folder in sorted(OUTPUT_BASE.iterdir()):
        if not folder.is_dir():
            continue
        parts = folder.name.rsplit("_", 1)
        if len(parts) != 2:
            continue
        pref_name, wl_key = parts
        if args.pref and pref_name != args.pref:
            continue
        html_path = folder / "index.html"
        if html_path.exists():
            targets.append((html_path, pref_name, wl_key))

    print(f"🔧 詳細ページ対象: {len(targets)} ファイル  dry-run={args.dry_run}  force={args.force}")

    for html_path, pref_name, wl_key in targets:
        ogp = make_detail_ogp(pref_name, wl_key)
        res = patch_file(html_path, ogp, args.dry_run, args.force)
        key = res.split("（")[0]
        results[key] = results.get(key, 0) + 1
        icon = {"injected":"✅","updated":"🔄","already":"⏭","skipped":"⚠","error":"❌"}.get(key,"?")
        print(f"  {icon} {pref_name}_{wl_key} → {res}")

    print(f"\n✅ 完了: {results}")


if __name__ == "__main__":
    main()
