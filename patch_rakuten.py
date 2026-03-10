#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  世界王 楽天トラベル 一括パッチスクリプト                           ║
║  patch_rakuten.py                                                ║
║                                                                  ║
║  既存の worldkings_output/ 以下の全 index.html に                 ║
║  楽天トラベル空室検索ウィジェットを注入する。                         ║
║                                                                  ║
║  使い方:                                                          ║
║    python patch_rakuten.py                        # 全235ファイル ║
║    python patch_rakuten.py --dry-run              # 確認のみ      ║
║    python patch_rakuten.py --pref 沖縄            # 1県だけ       ║
║    python patch_rakuten.py --pref 沖縄 --wl 封印線 # 1ファイルだけ║
║                                                                  ║
║  環境変数:                                                        ║
║    RAKUTEN_APP_ID   = 楽天アプリID（必須）                         ║
║    RAKUTEN_AFFIL_ID = 楽天アフィリエイトID（任意）                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import argparse
import os
import sys
from pathlib import Path

# ─── rakuten_travel.py を同じフォルダから import ─────────────────────
try:
    from rakuten_travel import (
        get_hotel_section_html,
        PREF_TO_RAKUTEN_CODE,
        RAKUTEN_APP_ID,
        RAKUTEN_AFFIL_ID,
    )
except ImportError:
    print("❌ rakuten_travel.py が見つかりません。同じフォルダに置いてください。")
    sys.exit(1)

# ─── 定数 ──────────────────────────────────────────────────────────
OUTPUT_BASE   = Path("worldkings_output")      # 出力フォルダのルート
MARKER_COMMENT = "<!-- rakuten-widget-injected -->"  # 注入済みマーカー

# 世界線キー → アクセントカラー（worldkings_novel.py と同じ配色）
COLOR_MAP = {
    "封印線": ("#1a0a2e", "#7b2ff7", "#c084fc"),
    "商都線": ("#2a1a0a", "#f7a02f", "#fcd084"),
    "静律線": ("#0a1a2e", "#2f7bf7", "#84c0fc"),
    "変革線": ("#2e0a0a", "#f72f2f", "#fc8484"),
    "境界線": ("#0a2e1a", "#2ff77b", "#84fcc0"),
}


def inject_widget(html_path: Path, pref_name: str, wl_key: str, dry_run: bool) -> str:
    """
    index.html にウィジェットを注入する。
    戻り値: "injected" / "already" / "skipped" / "error"
    """
    try:
        content = html_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"error: {e}"

    # 注入済みチェック
    if MARKER_COMMENT in content:
        return "already"

    # </body> がなければスキップ
    if "</body>" not in content:
        return "skipped"

    bg, accent, accent_light = COLOR_MAP.get(wl_key, ("#1a1a2e", "#7b7bf7", "#c0c0fc"))

    widget_html = get_hotel_section_html(
        pref_name=pref_name,
        wl_key=wl_key,
        accent_color=accent,
        accent_light=accent_light,
        bg_color=bg,
    )

    if not widget_html.strip():
        return "skipped"  # アプリID未設定 or 未対応県

    # </body> の直前に注入
    injected = content.replace(
        "</body>",
        f"\n{MARKER_COMMENT}\n{widget_html}\n</body>",
        1,  # 最初の1件だけ置換
    )

    if not dry_run:
        html_path.write_text(injected, encoding="utf-8")

    return "injected"


def main():
    parser = argparse.ArgumentParser(description="楽天トラベルウィジェット一括注入")
    parser.add_argument("--dry-run", action="store_true", help="書き込まずに確認だけ")
    parser.add_argument("--pref",    type=str, default="", help="特定の県だけ（例: 沖縄）")
    parser.add_argument("--wl",      type=str, default="", help="特定の世界線だけ（例: 封印線）")
    parser.add_argument("--output",  type=str, default="worldkings_output", help="出力フォルダのパス")
    args = parser.parse_args()

    output_base = Path(args.output)

    # ── 事前チェック ───────────────────────────────────────────────
    print("=" * 60)
    print("  楽天トラベル 一括パッチ")
    print("=" * 60)

    if not RAKUTEN_APP_ID:
        print("❌ RAKUTEN_APP_ID が未設定です。")
        print("   PowerShell: $env:RAKUTEN_APP_ID = 'your-app-id'")
        sys.exit(1)

    print(f"  APP_ID   : {RAKUTEN_APP_ID[:8]}...")
    print(f"  AFFIL_ID : {RAKUTEN_AFFIL_ID[:8]}..." if RAKUTEN_AFFIL_ID else "  AFFIL_ID : （未設定）")
    print(f"  対象フォルダ: {output_base.resolve()}")
    if args.dry_run:
        print("  ⚠ DRY-RUN モード（実際には書き込みません）")
    print()

    if not output_base.exists():
        print(f"❌ フォルダが見つかりません: {output_base}")
        sys.exit(1)

    # ── 対象フォルダを収集 ─────────────────────────────────────────
    targets = []
    for folder in sorted(output_base.iterdir()):
        if not folder.is_dir():
            continue

        # フォルダ名を「県名_世界線」に分割
        parts = folder.name.split("_", 1)
        if len(parts) != 2:
            continue

        pref_name, wl_key = parts[0], parts[1]

        # フィルター
        if args.pref and pref_name != args.pref:
            continue
        if args.wl and wl_key != args.wl:
            continue

        html_path = folder / "index.html"
        if not html_path.exists():
            continue

        targets.append((html_path, pref_name, wl_key))

    print(f"  対象ファイル数: {len(targets)}")
    print()

    # ── 一括注入 ───────────────────────────────────────────────────
    counts = {"injected": 0, "already": 0, "skipped": 0, "error": 0}

    for html_path, pref_name, wl_key in targets:
        result = inject_widget(html_path, pref_name, wl_key, dry_run=args.dry_run)
        counts[result.split(":")[0]] += 1

        icon = {
            "injected": "✅",
            "already":  "⏭",
            "skipped":  "⚠",
            "error":    "❌",
        }.get(result.split(":")[0], "?")

        print(f"  {icon} {pref_name}_{wl_key}  → {result}")

    # ── サマリー ───────────────────────────────────────────────────
    print()
    print("=" * 60)
    print(f"  ✅ 注入完了 : {counts['injected']} ファイル")
    print(f"  ⏭ 注入済み : {counts['already']} ファイル")
    print(f"  ⚠ スキップ : {counts['skipped']} ファイル")
    if counts['error']:
        print(f"  ❌ エラー   : {counts['error']} ファイル")
    print("=" * 60)

    if args.dry_run:
        print()
        print("  DRY-RUNのため書き込みは行いませんでした。")
        print("  実際に注入するには --dry-run を外して実行してください。")
    elif counts['injected'] > 0:
        print()
        print("  次のステップ: git add -A && git push")


if __name__ == "__main__":
    main()
