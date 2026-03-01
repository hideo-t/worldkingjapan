# -*- coding: utf-8 -*-
"""
画像最適化スクリプト
1. PNG → WebP変換（品質85、サイズ大幅削減）
2. サムネイル生成（index.html用、幅400px）
3. HTML内の参照パスを更新

使い方:
  pip install Pillow
  cd worldkingjapan
  python optimize_images.py
"""
from pathlib import Path
from PIL import Image
import os
import re
import sys

WEBP_QUALITY = 85
THUMB_WIDTH = 400
BASE = Path("worldkings_output")


def convert_to_webp(png_path: Path) -> tuple[Path, int, int]:
    """PNG → WebP変換。元サイズと新サイズを返す"""
    webp_path = png_path.with_suffix(".webp")
    orig_size = png_path.stat().st_size

    img = Image.open(png_path)
    if img.mode == "RGBA":
        # WebPはRGBAも対応だが、背景付きの方が軽い場合がある
        pass
    img.save(webp_path, "WEBP", quality=WEBP_QUALITY, method=4)
    new_size = webp_path.stat().st_size

    return webp_path, orig_size, new_size


def make_thumbnail(png_path: Path, thumb_dir: Path) -> Path:
    """サムネイル生成（幅400px）"""
    thumb_dir.mkdir(exist_ok=True)
    thumb_path = thumb_dir / png_path.with_suffix(".webp").name

    img = Image.open(png_path)
    ratio = THUMB_WIDTH / img.width
    new_h = int(img.height * ratio)
    img = img.resize((THUMB_WIDTH, new_h), Image.LANCZOS)
    img.save(thumb_path, "WEBP", quality=80, method=4)
    return thumb_path


def update_detail_html(html_path: Path):
    """詳細ページHTML内の .png → .webp 参照を更新"""
    content = html_path.read_text(encoding="utf-8")
    new_content = content.replace('.png"', '.webp"').replace(".png'", ".webp'")
    if new_content != content:
        html_path.write_text(new_content, encoding="utf-8")
        return True
    return False


def update_index_html():
    """トップページのサムネ参照を thumb/ + .webp に変更"""
    index = Path("index.html")
    if not index.exists():
        return False

    content = index.read_text(encoding="utf-8")

    # imgPath関数を更新: images/chapter_XX.png → thumbs/chapter_XX.webp
    old_func = re.search(r"function imgPath\(.*?\)\{.*?\}", content)
    if old_func:
        new_func = "function imgPath(pref,wl,ch){return encodeURI(`worldkings_output/${pref}_${wl}/thumbs/chapter_${String(ch).padStart(2,'0')}.webp`)}"
        content = content[:old_func.start()] + new_func + content[old_func.end():]
        index.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    if not BASE.exists():
        print(f"Error: {BASE} not found. Run from worldkingjapan directory.")
        sys.exit(1)

    total_orig = 0
    total_new = 0
    converted = 0
    thumbs = 0

    png_files = sorted(BASE.rglob("images/chapter_*.png"))
    total = len(png_files)
    print(f"Found {total} PNG images to optimize\n")

    for i, png in enumerate(png_files, 1):
        try:
            # WebP変換
            webp_path, orig, new = convert_to_webp(png)
            total_orig += orig
            total_new += new
            converted += 1

            # サムネイル生成
            thumb_dir = png.parent.parent / "thumbs"
            make_thumbnail(png, thumb_dir)
            thumbs += 1

            # 進捗表示
            pct = (1 - new / orig) * 100 if orig > 0 else 0
            if i % 50 == 0 or i == total:
                print(f"  [{i}/{total}] {pct:.0f}% smaller: {png.parent.parent.name}")

        except Exception as e:
            print(f"  ✗ {png}: {e}")

    # 詳細ページHTMLを更新
    html_updated = 0
    for html_file in sorted(BASE.rglob("index.html")):
        if update_detail_html(html_file):
            html_updated += 1

    # トップページ更新
    idx_updated = update_index_html()

    # サマリー
    orig_mb = total_orig / 1024 / 1024
    new_mb = total_new / 1024 / 1024
    saved_mb = orig_mb - new_mb
    pct = (1 - total_new / total_orig) * 100 if total_orig > 0 else 0

    print(f"\n{'='*50}")
    print(f"完了!")
    print(f"  PNG → WebP: {converted} files")
    print(f"  サムネイル: {thumbs} files")
    print(f"  HTML更新:   {html_updated} detail + {'1 index' if idx_updated else '0 index'}")
    print(f"  元サイズ:   {orig_mb:.1f} MB")
    print(f"  新サイズ:   {new_mb:.1f} MB")
    print(f"  削減:       {saved_mb:.1f} MB ({pct:.0f}% smaller)")
    print(f"{'='*50}")
    print(f"\n※ 確認後、元のPNGを削除するには:")
    print(f'  python -c "from pathlib import Path; [f.unlink() for f in Path(\'worldkings_output\').rglob(\'images/chapter_*.png\')]"')
    print(f"\n  git add . && git commit -m \"画像WebP最適化\" && git push origin main")


if __name__ == "__main__":
    main()
