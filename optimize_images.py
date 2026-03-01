# -*- coding: utf-8 -*-
"""
画像最適化スクリプト v2
1. PNG → WebP変換（品質85）
2. サムネイル生成（幅400px）
3. 詳細ページHTMLの .png → .webp 参照更新
※ index.htmlはフォールバック対応済みなので変更しない

使い方:
  pip install Pillow
  cd worldkingjapan
  python optimize_images.py
"""
from pathlib import Path
from PIL import Image
import sys

WEBP_QUALITY = 85
THUMB_WIDTH = 400
BASE = Path("worldkings_output")


def convert_to_webp(png_path):
    webp_path = png_path.with_suffix(".webp")
    orig_size = png_path.stat().st_size
    img = Image.open(png_path)
    img.save(webp_path, "WEBP", quality=WEBP_QUALITY, method=4)
    new_size = webp_path.stat().st_size
    return webp_path, orig_size, new_size


def make_thumbnail(png_path, thumb_dir):
    thumb_dir.mkdir(exist_ok=True)
    thumb_path = thumb_dir / png_path.with_suffix(".webp").name
    img = Image.open(png_path)
    ratio = THUMB_WIDTH / img.width
    new_h = int(img.height * ratio)
    img = img.resize((THUMB_WIDTH, new_h), Image.LANCZOS)
    img.save(thumb_path, "WEBP", quality=80, method=4)
    return thumb_path


def update_detail_html(html_path):
    content = html_path.read_text(encoding="utf-8")
    new_content = content.replace('.png"', '.webp"').replace(".png'", ".webp'")
    if new_content != content:
        html_path.write_text(new_content, encoding="utf-8")
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
            _, orig, new = convert_to_webp(png)
            total_orig += orig
            total_new += new
            converted += 1

            thumb_dir = png.parent.parent / "thumbs"
            make_thumbnail(png, thumb_dir)
            thumbs += 1

            if i % 50 == 0 or i == total:
                print(f"  [{i}/{total}] {png.parent.parent.name}")
        except Exception as e:
            print(f"  x {png}: {e}")

    html_updated = 0
    for html_file in sorted(BASE.rglob("index.html")):
        if update_detail_html(html_file):
            html_updated += 1

    orig_mb = total_orig / 1024 / 1024
    new_mb = total_new / 1024 / 1024
    saved_mb = orig_mb - new_mb
    pct = (1 - total_new / total_orig) * 100 if total_orig > 0 else 0

    print(f"\n{'='*50}")
    print(f"Done!")
    print(f"  PNG to WebP: {converted} files")
    print(f"  Thumbnails:  {thumbs} files")
    print(f"  HTML updated: {html_updated} detail pages")
    print(f"  Original:    {orig_mb:.1f} MB")
    print(f"  Optimized:   {new_mb:.1f} MB")
    print(f"  Saved:       {saved_mb:.1f} MB ({pct:.0f}% smaller)")
    print(f"{'='*50}")
    print(f"\nTo delete original PNGs:")
    print(f'  python -c "from pathlib import Path; [f.unlink() for f in Path(\'worldkings_output\').rglob(\'images/chapter_*.png\')]"')


if __name__ == "__main__":
    main()
