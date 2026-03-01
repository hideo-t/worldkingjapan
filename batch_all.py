#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界王 全県一括バッチ生成スクリプト
=====================================
47都道府県 × 5世界線 = 235話を一括生成

使い方:
  python batch_all.py                    # 全県 DeepSeek
  python batch_all.py --llm claude       # 全県 Claude
  python batch_all.py --email            # 各話ごとにGmail送信
  python batch_all.py --start 京都       # 京都から再開
  python batch_all.py --only 京都 福島 沖縄  # 指定県のみ

環境変数:
  DEEPSEEK_API_KEY   = sk-...
  ANTHROPIC_API_KEY   = sk-ant-... (claude使用時)
  GMAIL_ADDRESS       = your@gmail.com (--email時)
  GMAIL_APP_PASSWORD  = xxxx xxxx xxxx xxxx (--email時)
"""

import argparse
import os
import sys
import time
from datetime import datetime, timedelta

# ── Import pipeline ──
try:
    from worldkings_novel import run_pipeline, LLMConfig, SDConfig, check_sd, console, HAS_RICH
    from world_kings_data import PREFECTURES
except ImportError:
    print("ERROR: worldkings_novel.py と world_kings_data.py が同じフォルダに必要")
    sys.exit(1)

# 47都道府県の順番
ALL_PREFS = list(PREFECTURES.keys())


def estimate_time(total: int, per_story_sec: float = 150) -> str:
    """推定所要時間を計算"""
    total_sec = total * per_story_sec
    h = int(total_sec // 3600)
    m = int((total_sec % 3600) // 60)
    return f"{h}時間{m}分"


def main():
    parser = argparse.ArgumentParser(description="世界王 全県一括バッチ生成")
    parser.add_argument("--llm", default="deepseek", choices=["claude", "deepseek"],
                        help="LLMプロバイダ (default: deepseek)")
    parser.add_argument("--email", action="store_true",
                        help="各世界線ごとにGmail送信")
    parser.add_argument("--skip-images", action="store_true",
                        help="画像生成をスキップ（テキストのみ）")
    parser.add_argument("--start", default=None,
                        help="指定県から再開（例: --start 京都）")
    parser.add_argument("--only", nargs="+", default=None,
                        help="指定県のみ生成（例: --only 京都 福島 沖縄）")
    parser.add_argument("--dry-run", action="store_true",
                        help="実行せず計画だけ表示")
    parser.add_argument("--sd-url", default=None,
                        help="SD WebUI URL")
    args = parser.parse_args()

    # ── 対象県リスト ──
    if args.only:
        prefs = [p for p in args.only if p in PREFECTURES]
        invalid = [p for p in args.only if p not in PREFECTURES]
        if invalid:
            console.print(f"[red]❌ 未登録: {', '.join(invalid)}[/]")
    elif args.start:
        if args.start not in PREFECTURES:
            console.print(f"[red]❌ '{args.start}' は未登録[/]")
            return
        idx = ALL_PREFS.index(args.start)
        prefs = ALL_PREFS[idx:]
    else:
        prefs = ALL_PREFS

    # ── 世界線リスト ──
    total_stories = 0
    plan = []
    for pref_name in prefs:
        wl_keys = list(PREFECTURES[pref_name]["world_lines"].keys())
        for wl_key in wl_keys:
            plan.append((pref_name, wl_key))
            total_stories += 1

    # ── 事前チェック ──
    llm_config = LLMConfig(provider=args.llm)
    sd_config = SDConfig()
    if args.sd_url:
        sd_config.url = args.sd_url

    sd_available = check_sd(sd_config) and not args.skip_images

    # ── 計画表示 ──
    console.print()
    console.print(f"[bold cyan]{'='*60}[/]")
    console.print(f"[bold cyan]  世界王 全県一括バッチ生成[/]")
    console.print(f"[bold cyan]{'='*60}[/]")
    console.print()
    console.print(f"  対象県数:   {len(prefs)}県")
    console.print(f"  総生成数:   {total_stories}話（各5章 + 挿絵5枚）")
    console.print(f"  LLM:        {args.llm.upper()}")
    console.print(f"  SD画像:     {'ON' if sd_available else 'OFF（テキストのみ）'}")
    console.print(f"  Gmail送信:  {'ON' if args.email else 'OFF'}")

    # 時間・コスト推定
    if sd_available:
        per_story = 150  # 2.5分（テキスト+画像）
    else:
        per_story = 60   # 1分（テキストのみ）

    est_time = estimate_time(total_stories, per_story)
    if args.llm == "deepseek":
        est_cost = f"~${total_stories * 0.009:.1f}（約{int(total_stories * 0.009 * 150)}円）"
    else:
        est_cost = f"~${total_stories * 0.105:.1f}（約{int(total_stories * 0.105 * 150)}円）"

    console.print(f"  推定時間:   {est_time}")
    console.print(f"  推定API費:  {est_cost}")
    console.print()

    # 最初と最後を表示
    if len(plan) > 6:
        for pref, wl in plan[:3]:
            console.print(f"    {pref} × {wl}")
        console.print(f"    ... ({len(plan) - 6}話省略)")
        for pref, wl in plan[-3:]:
            console.print(f"    {pref} × {wl}")
    else:
        for pref, wl in plan:
            console.print(f"    {pref} × {wl}")

    console.print()

    if args.dry_run:
        console.print("[yellow]  --dry-run: 計画表示のみ。実行するには --dry-run を外す[/]")
        return

    # ── 確認 ──
    console.print("[bold yellow]  開始しますか？ (y/n): [/]", end="")
    confirm = input().strip().lower()
    if confirm not in ("y", "yes", ""):
        console.print("[yellow]  キャンセル[/]")
        return

    # ── 実行 ──
    start_time = time.time()
    completed = 0
    failed = []
    log_file = f"batch_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    for i, (pref_name, wl_key) in enumerate(plan):
        wl_value = PREFECTURES[pref_name]["world_lines"][wl_key]
        progress_str = f"[{i+1}/{total_stories}]"

        console.print()
        console.print(f"[bold cyan]{'='*60}[/]")
        console.print(f"[bold]  {progress_str} {pref_name} × {wl_key}（{wl_value}）[/]")

        # 残り時間推定
        if completed > 0:
            elapsed = time.time() - start_time
            avg = elapsed / completed
            remaining = avg * (total_stories - completed)
            eta = timedelta(seconds=int(remaining))
            console.print(f"  残り推定: {eta}")

        console.print(f"[bold cyan]{'='*60}[/]")

        try:
            run_pipeline(
                pref_name=pref_name,
                world_line_option=wl_key,
                llm_config=llm_config,
                sd_config=sd_config,
                skip_images=args.skip_images or not sd_available,
                skip_push=True,  # バッチ中はpushしない
                send_email=args.email,
            )
            completed += 1

            # ログ書き出し
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"OK  {pref_name} {wl_key} {datetime.now().isoformat()}\n")

        except Exception as e:
            console.print(f"[red]  ❌ 失敗: {e}[/]")
            failed.append((pref_name, wl_key, str(e)))

            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"ERR {pref_name} {wl_key} {e}\n")

            # API制限エラーなら少し待つ
            if "rate" in str(e).lower() or "429" in str(e):
                console.print("[yellow]  ⏳ レート制限検知、60秒待機...[/]")
                time.sleep(60)
            else:
                time.sleep(5)  # 通常エラーは5秒待って次へ

            continue

        # API負荷軽減（DeepSeekは2秒、Claudeは3秒）
        wait = 3 if args.llm == "claude" else 2
        time.sleep(wait)

    # ── 最終レポート ──
    total_time = time.time() - start_time
    hours = int(total_time // 3600)
    mins = int((total_time % 3600) // 60)

    console.print()
    console.print(f"[bold green]{'='*60}[/]")
    console.print(f"[bold green]  バッチ完了！[/]")
    console.print(f"[bold green]{'='*60}[/]")
    console.print(f"  成功: {completed}/{total_stories}")
    console.print(f"  失敗: {len(failed)}")
    console.print(f"  所要: {hours}時間{mins}分")
    console.print(f"  ログ: {log_file}")

    if failed:
        console.print()
        console.print("[red]  失敗リスト:[/]")
        for pref, wl, err in failed:
            console.print(f"    {pref} × {wl}: {err[:60]}")

        # リトライコマンド生成
        retry_prefs = list(set(p for p, w, e in failed))
        console.print()
        console.print("[yellow]  リトライ:[/]")
        for p in retry_prefs:
            console.print(f"    python worldkings_novel.py {p} --all --llm {args.llm} --skip-push")

    console.print()
    console.print(f"[bold]  次のステップ: git pushでまとめてデプロイ[/]")
    console.print(f"    git add worldkings_output/")
    console.print(f"    git commit -m \"batch {len(prefs)} prefectures\"")
    console.print(f"    git push")


if __name__ == "__main__":
    main()
