#!/usr/bin/env python3
"""楽天トラベル 都道府県コード検証スクリプト"""
import urllib.request, urllib.parse, json, time

APP_ID = "48183afe-d7a2-47ee-92a6-da11db5a18ee"

# 現在のコード一覧（怪しいものを検証）
CODES = {
    "北海道":"hokkaido","青森":"aomori","岩手":"iwate","宮城":"miyagi","秋田":"akita",
    "山形":"yamagata","福島":"hukushima","茨城":"ibaragi","栃木":"tochigi","群馬":"gunma",
    "埼玉":"saitama","千葉":"chiba","東京":"tokyo","神奈川":"kanagawa","新潟":"niigata",
    "富山":"toyama","石川":"ishikawa","福井":"fukui","山梨":"yamanashi","長野":"nagano",
    "岐阜":"gifu","静岡":"shizuoka","愛知":"aichi","三重":"mie","滋賀":"shiga",
    "京都":"kyoto","大阪":"osaka","兵庫":"hyogo","奈良":"nara","和歌山":"wakayama",
    "鳥取":"tottori","島根":"shimane","岡山":"okayama","広島":"hiroshima","山口":"yamaguchi",
    "徳島":"tokushima","香川":"kagawa","愛媛":"ehime","高知":"kochi","福岡":"fukuoka",
    "佐賀":"saga","長崎":"nagasaki","熊本":"kumamoto","大分":"oita","宮崎":"miyazaki",
    "鹿児島":"kagoshima","沖縄":"okinawa",
}

def check_code(pref, code):
    """コードが有効か検証（searchVacantで県単位検索）"""
    url = (
        "https://search.travel.rakuten.co.jp/ds/vacant/searchVacant"
        f"?f_dai=japan&f_chu={code}"
        "&f_nen1=2026&f_tuki1=4&f_hi1=1"
        "&f_nen2=2026&f_tuki2=4&f_hi2=2"
        "&f_otona_su=2&f_heya_su=1&f_hyoji=1"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req, timeout=5)
        body = res.read().decode("utf-8", errors="ignore")
        # 404ページかどうか判定
        if "指定されたページが見つかりません" in body or "404" in body[:200]:
            return "❌ 404"
        elif "件" in body or "ホテル" in body or "旅館" in body:
            return "✅ OK"
        else:
            return "⚠ 不明"
    except Exception as e:
        return f"⚠ {str(e)[:30]}"

print("=" * 50)
print("楽天トラベル コード検証中...")
print("=" * 50)

for pref, code in CODES.items():
    result = check_code(pref, code)
    print(f"  {pref:5s} {code:15s} {result}")
    time.sleep(0.3)  # レート制限対策

print("=" * 50)
print("完了")
