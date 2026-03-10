#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界王 マイページ FAB ボタン 一括パッチ
- 全235話の詳細ページに ♡（お気に入り）と 📖（マイページへ）ボタンを注入
使い方:
  python patch_mypage_fab.py              # 全235ファイル
  python patch_mypage_fab.py --dry-run    # 確認のみ
  python patch_mypage_fab.py --pref 東京  # 1県だけ
  python patch_mypage_fab.py --force      # 注入済みも強制上書き
"""

import argparse, os, sys
from pathlib import Path

OUTPUT_BASE  = Path("worldkings_output")
MARKER_START = "<!-- mypage-fab-injected -->"
MARKER_END   = "<!-- /mypage-fab -->"


def make_fab_html(pref_name: str, wl_key: str) -> str:
    """♡ + 📖 フローティングボタン HTML + CSS + JS を生成"""
    # ポータルへの相対パス（2階層上）
    portal_url = "../../index.html"

    return f"""{MARKER_START}
<style>
.wk-fab-wrap{{
  position:fixed;right:.9rem;bottom:5rem;z-index:500;
  display:flex;flex-direction:column;gap:.5rem;
}}
.wk-fab{{
  width:50px;height:50px;border-radius:50%;
  border:1px solid rgba(201,168,76,.3);
  background:rgba(6,6,14,.92);
  backdrop-filter:blur(10px);
  display:flex;align-items:center;justify-content:center;
  font-size:1.3rem;cursor:pointer;
  transition:.25s;
  box-shadow:0 2px 14px rgba(0,0,0,.45);
  text-decoration:none;
  -webkit-tap-highlight-color:transparent;
}}
.wk-fab:hover{{
  border-color:rgba(201,168,76,.6);
  background:rgba(201,168,76,.12);
  transform:scale(1.1);
}}
.wk-fab-fav.fav-on{{
  background:rgba(247,80,100,.18);
  border-color:rgba(247,80,100,.5);
}}
.wk-fab-tip{{
  position:absolute;right:58px;
  background:rgba(6,6,14,.95);
  border:1px solid rgba(255,255,255,.08);
  border-radius:6px;padding:.3rem .6rem;
  font-size:.65rem;color:#c8c8d4;
  white-space:nowrap;font-family:inherit;
  pointer-events:none;opacity:0;transition:.2s;
}}
.wk-fab:hover .wk-fab-tip{{opacity:1}}
</style>

<div class="wk-fab-wrap">
  <!-- マイページへ -->
  <a class="wk-fab" href="{portal_url}#mypage"
     onclick="sessionStorage.setItem('wk_open_mypage','1')"
     title="マイページ">
    📖<span class="wk-fab-tip">マイページ</span>
  </a>
  <!-- お気に入り（♡） -->
  <button class="wk-fab wk-fab-fav" id="wkFavBtn"
     onclick="wkToggleFav()" title="お気に入り">
    <span id="wkFavIcon">♡</span>
    <span class="wk-fab-tip" id="wkFavTip">お気に入りに追加</span>
  </button>
</div>

<script>
(function(){{
  var PREF = '{pref_name}';
  var KEY  = 'wk_my_prefavs';
  function getFavs(){{ try{{ return JSON.parse(localStorage.getItem(KEY)||'[]'); }}catch(e){{return[];}} }}
  function saveFavs(f){{ localStorage.setItem(KEY, JSON.stringify(f)); }}
  function isFav(){{ return getFavs().indexOf(PREF) >= 0; }}
  function update(){{
    var on = isFav();
    document.getElementById('wkFavIcon').textContent = on ? '♥' : '♡';
    document.getElementById('wkFavTip').textContent  = on ? 'お気に入り済み' : 'お気に入りに追加';
    document.getElementById('wkFavBtn').classList.toggle('fav-on', on);
  }}
  window.wkToggleFav = function(){{
    var f = getFavs();
    var i = f.indexOf(PREF);
    if(i >= 0) f.splice(i, 1); else f.unshift(PREF);
    saveFavs(f);
    update();
  }};
  update();
}})();
</script>
{MARKER_END}"""


def inject(html_path: Path, pref_name: str, wl_key: str, dry_run: bool, force: bool) -> str:
    try:
        content = html_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"error（{e}）"

    if "</body>" not in content:
        return "skipped（</body>なし）"

    already = MARKER_START in content
    if already and not force:
        return "already"

    if already:
        # 既存を削除
        import re
        content = re.sub(
            r'\n?' + re.escape(MARKER_START) + r'.*?' + re.escape(MARKER_END),
            '', content, flags=re.DOTALL
        )

    fab_html = make_fab_html(pref_name, wl_key)
    injected = content.replace("</body>", f"\n{fab_html}\n</body>")

    if not dry_run:
        html_path.write_text(injected, encoding="utf-8")

    return "updated" if already else "injected"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--pref", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

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

    print(f"🔧 対象: {len(targets)} ファイル  dry-run={args.dry_run}  force={args.force}")

    counts = {"injected": 0, "updated": 0, "already": 0, "skipped": 0, "error": 0}
    for html_path, pref_name, wl_key in targets:
        result = inject(html_path, pref_name, wl_key, args.dry_run, args.force)
        key = result.split("（")[0]
        counts[key] = counts.get(key, 0) + 1
        icon = {"injected":"✅","updated":"🔄","already":"⏭","skipped":"⚠","error":"❌"}.get(key,"?")
        print(f"  {icon} {pref_name}_{wl_key} → {result}")

    print(f"\n完了: {counts}")


if __name__ == "__main__":
    main()
