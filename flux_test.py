#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  世界王 × FLUX1.1 [pro] テスト生成スクリプト                       ║
║  flux_test.py                                                    ║
║                                                                  ║
║  使い方:                                                          ║
║    python flux_test.py                  # 沖縄・封印線・第1章      ║
║    python flux_test.py --pref 京都 --wl 封印線 --ch 2            ║
║                                                                  ║
║  環境変数:                                                        ║
║    $env:BFL_API_KEY = "your-key"                                 ║
╚══════════════════════════════════════════════════════════════════╝
"""

import argparse
import os
import sys
import time
import requests
from pathlib import Path

# ─── APIキー ──────────────────────────────────────────────────────
BFL_API_KEY = os.environ.get("BFL_API_KEY", "")
API_ENDPOINT = "https://api.bfl.ai/v1/flux-pro-1.1"

# ─── 世界線 → 画風キーワード ──────────────────────────────────────
WL_STYLE = {
    "封印線": "mystical sealed ancient, deep purple and gold, ethereal barrier glowing, sacred geometry",
    "商都線": "vibrant merchant city, warm amber light, bustling market, golden prosperity",
    "静律線": "zen tranquility, soft blue mist, meditation, silent shrine, spiritual calm",
    "変革線": "revolution uprising, crimson energy, dramatic storm, transformation power",
    "境界線": "boundary between worlds, emerald mist, ocean meets mountain, cultural crossroads",
}

# ─── 章ごとの雰囲気 ───────────────────────────────────────────────
CH_MOOD = {
    1: "peaceful dawn, gentle awakening, soft light",
    2: "fairy magic, ethereal glow, whimsical fantasy, cute fairy character",
    3: "storm approaching, dramatic tension, dark clouds gathering",
    4: "sacred holy, divine light rays, spiritual climax",
    5: "epic grand finale, vast panorama, legendary scale",
}

# ─── 47都道府県の景観キーワード（簡易版） ────────────────────────────
PREF_LANDSCAPE = {
    "北海道": "vast snowy plains, lavender fields, volcanic mountains, pioneer farmland",
    "青森": "apple orchards, Aomori nebuta lanterns, Tsugaru strait, misty mountains",
    "岩手": "Iwate mountain, Hiraizumi golden temple ruins, deep forests, ancient ruins",
    "宮城": "Matsushima pine islands, Date samurai castle, coastal fishing village",
    "秋田": "Akita cedar forest, Lake Tazawa deep blue, rice paddies, Namahage demon masks",
    "山形": "Yamadera mountain temple cliffs, cherry blossoms, snow monsters on Zao",
    "福島": "Aizu samurai town, Bandai mountain volcanic lake, persimmon orchards",
    "茨城": "Kashima shrine ancient forest, Ibaraki plum grove, Pacific coast cliffs",
    "栃木": "Nikko ornate shrine gold and red, cedar avenue, Kegon waterfall",
    "群馬": "Kusatsu onsen steam, Haruna lake, silk weaving town, mountain valleys",
    "埼玉": "Chichibu mountain shrine, Kawagoe old merchant town, Musashi plains",
    "千葉": "Chiba coastal cliffs, Naritasan temple, Tokyo bay shore, flower fields",
    "東京": "modern neon cityscape, ancient Senso-ji among skyscrapers, Shinjuku lights",
    "神奈川": "Kamakura great Buddha coastal, Yokohama harbor red brick, Mt Fuji silhouette",
    "新潟": "Niigata rice terraces, Sea of Japan winter waves, snow country landscape",
    "富山": "Tateyama alpine snow corridor, traditional gassho farmhouses, clear mountain streams",
    "石川": "Kenroku-en elegant garden, Wajima lacquerware, Noto peninsula rugged coast",
    "福井": "Eiheiji moss-covered zen temple, Tojinbo sea cliffs, dinosaur fossil coast",
    "山梨": "Mt Fuji reflected in Kawaguchi lake, wine vineyards, Shosenkyo gorge",
    "長野": "Japanese Alps jagged peaks, Matsumoto castle crow castle, Zenko-ji pilgrimage",
    "岐阜": "Shirakawa-go thatched roof village, Hida folk village, Nagaragawa cormorant fishing",
    "静岡": "Mt Fuji tea plantations, Izu Peninsula ocean cliffs, Miho pine grove",
    "愛知": "Nagoya golden castle shachihoko, Toyota industrial, Inuyama castle river",
    "三重": "Ise Grand Shrine sacred forest, Toba pearl diving, Kumano ancient pilgrimage",
    "滋賀": "Lake Biwa vast blue water, Hikone castle reflection, reeds and herons",
    "京都": "ancient Kyoto imperial palace, vermillion torii gates, stone zen garden, geisha district",
    "大阪": "Osaka castle cherry blossoms, Dotonbori neon canal, takoyaki street food",
    "兵庫": "Himeji white heron castle, Arima onsen village, Awaji island shore",
    "奈良": "giant Buddha ancient hall, sacred deer in misty forest, Kasuga lanterns",
    "和歌山": "Koyasan mountain monastery fog, Kumano Nachi waterfall sacred, mandarin orange groves",
    "鳥取": "Tottori sand dunes dramatic, Daisen volcanic mountain, Uradome crystal coast",
    "島根": "Izumo Taisha grand shrine of gods, Matsue castle black, Oki island remote",
    "岡山": "Korakuen garden seasonal, Okayama black crow castle, Seto Inland Sea islands",
    "広島": "Itsukushima floating torii gate sea, atomic dome ruins, Seto sea sunset",
    "山口": "Kintai Bridge arching river, Akiyoshidai karst plateau, Motonosumi torii tunnel",
    "徳島": "Awa Odori dance lanterns, Naruto whirlpool, Yoshino indigo river",
    "香川": "Kotohira shrine mountain steps, Seto Inland Sea olive islands, udon wheat fields",
    "愛媛": "Matsuyama castle hilltop, Dogo onsen ancient bath, Shikoku 88 temple pilgrimage",
    "高知": "Kochi Shimanto clear river, Cape Muroto dramatic cliffs, bonito fishing port",
    "福岡": "Dazaifu shrine plum blossoms, Hakata traditional festival, Fukuoka modern waterfront",
    "佐賀": "Yoshinogari ancient ruins, Imari porcelain ceramics, balloon festival sky",
    "長崎": "Nagasaki harbor European buildings, Glover garden colonial, lantern festival",
    "熊本": "Aso volcanic caldera steam, Kumamoto castle black stone, green grasslands",
    "大分": "Beppu hell hot springs steam, Yufuin valley misty morning, Usa shrine ancient",
    "宮崎": "Takachiho gorge mythological waterfall, Nichinan subtropical coast, Miyazaki Phoenix",
    "鹿児島": "Sakurajima erupting volcano harbor, Yakushima ancient cedar forest, Amami tropical",
    "沖縄": "Okinawa turquoise coral reef, Shuri castle red lacquer, subtropical jungle, Ryukyu culture",
}


def generate_image(prompt: str, width: int = 1024, height: int = 768) -> str | None:
    """
    FLUX1.1 [pro] APIで画像を生成し、画像URLを返す。
    非同期API（submit → poll）方式。
    """
    if not BFL_API_KEY:
        print("❌ BFL_API_KEY が未設定です。")
        print("   PowerShell: $env:BFL_API_KEY = 'your-key'")
        return None

    headers = {
        "accept": "application/json",
        "x-key": BFL_API_KEY,
        "Content-Type": "application/json",
    }

    # ── Step 1: リクエスト送信 ──────────────────────────────────────
    print(f"  📤 リクエスト送信中...")
    res = requests.post(
        API_ENDPOINT,
        headers=headers,
        json={
            "prompt": prompt,
            "width": width,
            "height": height,
        },
        timeout=30,
    )

    if res.status_code != 200:
        print(f"  ❌ APIエラー: {res.status_code} {res.text}")
        return None

    data = res.json()
    # 新エンドポイント(api.bfl.ai)はpolling_urlを返す
    polling_url = data.get("polling_url") or f"https://api.bfl.ai/v1/get_result?id={data.get('id')}"
    print(f"  ✅ リクエスト受付: {data.get('id', '?')}")

    # ── Step 2: ポーリング（完了待ち） ────────────────────────────
    print(f"  ⏳ 生成中 ", end="", flush=True)
    for _ in range(120):  # 最大60秒
        time.sleep(0.5)
        poll = requests.get(
            polling_url,
            headers=headers,
            timeout=10,
        ).json()

        status = poll.get("status", "")
        if status == "Ready":
            print(" ✨ 完了！")
            return poll["result"]["sample"]
        elif status in ("Error", "Failed"):
            print(f"\n  ❌ 生成失敗: {poll}")
            return None
        else:
            print(".", end="", flush=True)

    print("\n  ⏱ タイムアウト")
    return None


def download_image(url: str, save_path: Path) -> bool:
    """画像URLをダウンロードして保存"""
    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        save_path.write_bytes(res.content)
        return True
    except Exception as e:
        print(f"  ❌ ダウンロード失敗: {e}")
        return False


def build_prompt(pref: str, wl_key: str, chapter: int) -> str:
    """世界王スタイルのFLUXプロンプトを生成"""
    landscape = PREF_LANDSCAPE.get(pref, "mystical Japanese landscape")
    style     = WL_STYLE.get(wl_key, "mystical ethereal")
    mood      = CH_MOOD.get(chapter, "dramatic atmospheric")

    return (
        f"Masterpiece illustration, {landscape}, "
        f"{style}, {mood}, "
        f"invisible guardian king watching over the land, "
        f"ancient Japanese mythology meets fantasy, "
        f"cinematic lighting, highly detailed, 8K quality, "
        f"no text, no watermark, painterly style"
    )


def main():
    parser = argparse.ArgumentParser(description="FLUX1.1 [pro] テスト生成")
    parser.add_argument("--pref", default="沖縄",  help="都道府県名")
    parser.add_argument("--wl",   default="封印線", help="世界線")
    parser.add_argument("--ch",   type=int, default=1, help="章番号(1-5)")
    parser.add_argument("--out",  default="flux_test_output", help="出力フォルダ")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(exist_ok=True)

    print("=" * 55)
    print(f"  FLUX1.1 [pro] テスト生成")
    print("=" * 55)
    print(f"  県     : {args.pref}")
    print(f"  世界線 : {args.wl}")
    print(f"  章     : 第{args.ch}章")
    print()

    prompt = build_prompt(args.pref, args.wl, args.ch)
    print(f"  プロンプト:\n  {prompt[:100]}...")
    print()

    # 生成
    image_url = generate_image(prompt, width=1024, height=768)
    if not image_url:
        sys.exit(1)

    # ダウンロード
    save_path = out_dir / f"{args.pref}_{args.wl}_ch{args.ch}.jpg"
    print(f"  💾 保存中: {save_path}")
    if download_image(image_url, save_path):
        print(f"  ✅ 完了！ → {save_path.resolve()}")
        print()
        print(f"  💰 消費クレジット: 4 credits（$0.04）")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
