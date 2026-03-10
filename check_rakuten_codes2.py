#!/usr/bin/env python3
"""訓令式コードで再検証"""
import urllib.request, time

def check(code):
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
        if "指定されたページが見つかりません" in body or "404" in body[:200]:
            return "❌"
        elif "件" in body or "ホテル" in body or "旅館" in body:
            return "✅"
        else:
            return "⚠"
    except Exception as e:
        return f"ERR:{str(e)[:20]}"

# 訓令式が疑われる県を両方チェック
suspects = [
    ("千葉",   "chiba",    "tiba"),
    ("静岡",   "shizuoka", "sizuoka"),
    ("広島",   "hiroshima","hirosima"),
    ("鹿児島", "kagoshima","kagosima"),
    ("徳島",   "tokushima","tokusima"),
    ("愛知",   "aichi",    "aiti"),
    ("高知",   "kochi",    "koti"),
    ("栃木",   "tochigi",  "totigi"),
    ("長崎",   "nagasaki", "nagasaki"),  # 変わらない
]

print(f"{'県名':6s}  {'ヘボン式':15s}  {'訓令式':15s}")
print("-" * 45)
for pref, hepburn, kunrei in suspects:
    r1 = check(hepburn); time.sleep(0.3)
    r2 = check(kunrei);  time.sleep(0.3)
    mark = "← 正解" if r2 == "✅" and r1 != "✅" else ("← 正解" if r1 == "✅" else "")
    print(f"{pref:6s}  {hepburn:15s}{r1}  {kunrei:15s}{r2}  {mark}")

print("\n完了")
