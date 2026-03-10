#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界王 ホテルウィジェット 一括パッチ v2
- 古いウィジェット（v1/v2/v3）を自動削除して最新版を再注入
使い方:
  python patch_rakuten.py              # 全235ファイル
  python patch_rakuten.py --dry-run    # 確認のみ
  python patch_rakuten.py --pref 沖縄  # 1県だけ
  python patch_rakuten.py --force      # 注入済みも強制上書き
"""

import argparse, os, re, sys
from pathlib import Path

try:
    from rakuten_travel import get_hotel_section_html, PREF_TO_RAKUTEN_CODE, RAKUTEN_APP_ID, RAKUTEN_AFFIL_ID
except ImportError:
    print("❌ rakuten_travel.py が見つかりません。同じフォルダに置いてください。")
    sys.exit(1)

OUTPUT_BASE    = Path("worldkings_output")
MARKER_START   = "<!-- rakuten-widget-injected -->"   # 新マーカー
MARKER_END     = "<!-- /rakuten-hotel-widget -->"     # 新終端

# 古いバージョンで使われていたマーカー（これがあれば古いと判断）
OLD_MARKERS = [
    "<!-- rakuten-widget-injected -->",
    "<!-- rakuten-hotel-widget:",
    "id=\"hotel-search\"",
    "class=\"hotel-widget\"",
]

COLOR_MAP = {
    "封印線": ("#1a0a2e", "#7b2ff7", "#c084fc"),
    "商都線": ("#2a1a0a", "#f7a02f", "#fcd084"),
    "静律線": ("#0a1a2e", "#2f7bf7", "#84c0fc"),
    "変革線": ("#2e0a0a", "#f72f2f", "#fc8484"),
    "境界線": ("#0a2e1a", "#2ff77b", "#84fcc0"),
}


def remove_old_widget(content: str) -> str:
    """古いウィジェットブロックを丸ごと削除する"""

    # パターン1: <!-- rakuten-widget-injected --> ～ <!-- /rakuten-hotel-widget --> 
    content = re.sub(
        r'\n<!-- rakuten-widget-injected -->.*?<!-- /rakuten-hotel-widget -->',
        '', content, flags=re.DOTALL
    )

    # パターン2: <!-- rakuten-hotel-widget: で始まるブロック（マーカーなし版）
    content = re.sub(
        r'\n<!-- rakuten-hotel-widget:.*?<!-- /rakuten-hotel-widget -->',
        '', content, flags=re.DOTALL
    )

    # パターン3: <section id="hotel-search" ～ </section> （上記で残った場合）
    content = re.sub(
        r'\n<section id="hotel-search".*?</section>',
        '', content, flags=re.DOTALL
    )

    # パターン4: <style>.hotel-widget{ ～ </style> （孤立したスタイル）
    content = re.sub(
        r'\n<style>\s*\.hotel-widget\{.*?</style>',
        '', content, flags=re.DOTALL
    )

    # パターン5: <script>...htSearch_ ～ </script> （孤立したスクリプト）
    content = re.sub(
        r'\n<script>\s*\(function\(\)\{[^<]*ht-ci-.*?</script>',
        '', content, flags=re.DOTALL
    )

    return content


def has_old_widget(content: str) -> bool:
    return any(m in content for m in OLD_MARKERS)


def inject_widget(html_path: Path, pref_name: str, wl_key: str, dry_run: bool, force: bool) -> str:
    try:
        content = html_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"error: {e}"

    already = has_old_widget(content)

    if already and not force:
        return "already（--force で上書き可）"

    if "</body>" not in content:
        return "skipped（</body>なし）"

    # 古いウィジェットを削除
    if already:
        content = remove_old_widget(content)

    bg, accent, accent_light = COLOR_MAP.get(wl_key, ("#1a1a2e", "#7b7bf7", "#c0c0fc"))

    widget_html = get_hotel_section_html(
        pref_name=pref_name, wl_key=wl_key,
        accent_color=accent, accent_light=accent_light, bg_color=bg,
    )

    if not widget_html.strip():
        return "skipped（ウィジェット生成失敗）"

    injected = content.replace(
        "</body>",
        f"\n{MARKER_START}\n{widget_html}\n</body>",
        1,
    )

    if not dry_run:
        html_path.write_text(injected, encoding="utf-8")

    return "updated" if already else "injected"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force",   action="store_true", help="注入済みファイルも強制上書き")
    parser.add_argument("--pref",    type=str, default="")
    parser.add_argument("--wl",      type=str, default="")
    parser.add_argument("--output",  type=str, default="worldkings_output")
    args = parser.parse_args()

    output_base = Path(args.output)

    print("=" * 60)
    print("  ホテルウィジェット 一括パッチ v2")
    print("=" * 60)
    if not RAKUTEN_APP_ID:
        print("❌ RAKUTEN_APP_ID 未設定")
        sys.exit(1)

    print(f"  APP_ID   : {RAKUTEN_APP_ID[:8]}...")
    print(f"  AFFIL_ID : {RAKUTEN_AFFIL_ID[:8]}..." if RAKUTEN_AFFIL_ID else "  AFFIL_ID : （未設定）")
    print(f"  モード   : {'DRY-RUN' if args.dry_run else ('FORCE更新' if args.force else '通常')}")
    print()

    if not output_base.exists():
        print(f"❌ フォルダが見つかりません: {output_base}")
        sys.exit(1)

    targets = []
    for folder in sorted(output_base.iterdir()):
        if not folder.is_dir(): continue
        parts = folder.name.split("_", 1)
        if len(parts) != 2: continue
        pref_name, wl_key = parts
        if args.pref and pref_name != args.pref: continue
        if args.wl   and wl_key   != args.wl:   continue
        html_path = folder / "index.html"
        if not html_path.exists(): continue
        targets.append((html_path, pref_name, wl_key))

    print(f"  対象: {len(targets)} ファイル\n")

    counts = {}
    for html_path, pref_name, wl_key in targets:
        result = inject_widget(html_path, pref_name, wl_key, args.dry_run, args.force)
        key = result.split("（")[0]
        counts[key] = counts.get(key, 0) + 1
        icon = {"injected":"✅","updated":"🔄","skipped":"⚠","error":"❌"}.get(key, "⏭")
        print(f"  {icon} {pref_name}_{wl_key} → {result}")

    print()
    print("=" * 60)
    for k, v in counts.items():
        icon = {"injected":"✅","updated":"🔄","skipped":"⚠","error":"❌","already":"⏭"}.get(k,"?")
        print(f"  {icon} {k}: {v}")
    print("=" * 60)
    if not args.dry_run and counts.get("injected", 0) + counts.get("updated", 0) > 0:
        print("\n  次: git add -A && git push origin main --force")

if __name__ == "__main__":
    main()
