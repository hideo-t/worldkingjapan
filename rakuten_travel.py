#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  世界王 × 楽天トラベル空室検索 統合モジュール v2                    ║
║  rakuten_travel.py                                               ║
║                                                                  ║
║  環境変数（PowerShellで設定）:                                     ║
║    $env:RAKUTEN_APP_ID   = "48183afe-xxxx-..."                   ║
║    $env:RAKUTEN_AFFIL_ID = "51be1a0f.xxxx...."（任意）            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os

# ─── 環境変数からAPIキーを読み込む ────────────────────────────────────
RAKUTEN_APP_ID   = os.environ.get("RAKUTEN_APP_ID",   "")
RAKUTEN_AFFIL_ID = os.environ.get("RAKUTEN_AFFIL_ID", "")

# ─── 47都道府県 → 楽天トラベル middleClassCode マッピング ─────────────
PREF_TO_RAKUTEN_CODE: dict[str, str] = {
    "北海道": "hokkaido", "青森": "aomori",   "岩手": "iwate",
    "宮城":   "miyagi",   "秋田": "akita",    "山形": "yamagata",
    "福島":   "fukushima","茨城": "ibaraki",  "栃木": "tochigi",
    "群馬":   "gunma",    "埼玉": "saitama",  "千葉": "chiba",
    "東京":   "tokyo",    "神奈川":"kanagawa", "新潟": "niigata",
    "富山":   "toyama",   "石川": "ishikawa", "福井": "fukui",
    "山梨":   "yamanashi","長野": "nagano",   "岐阜": "gifu",
    "静岡":   "shizuoka", "愛知": "aichi",    "三重": "mie",
    "滋賀":   "shiga",    "京都": "kyoto",    "大阪": "osaka",
    "兵庫":   "hyogo",    "奈良": "nara",     "和歌山":"wakayama",
    "鳥取":   "tottori",  "島根": "shimane",  "岡山": "okayama",
    "広島":   "hiroshima","山口": "yamaguchi","徳島": "tokushima",
    "香川":   "kagawa",   "愛媛": "ehime",    "高知": "kochi",
    "福岡":   "fukuoka",  "佐賀": "saga",     "長崎": "nagasaki",
    "熊本":   "kumamoto", "大分": "oita",     "宮崎": "miyazaki",
    "鹿児島": "kagoshima","沖縄": "okinawa",
}

# ─── 世界線ごとの宿フィルター ─────────────────────────────────────────
WORLD_LINE_SQUEEZE: dict[str, str] = {
    "封印線": "onsen",      # 温泉（神秘・静寂）
    "商都線": "",           # フィルターなし（都市ホテル）
    "静律線": "breakfast",  # 朝食付き（禅の朝）
    "変革線": "internet",   # Wi-Fi完備（革命の情報戦）
    "境界線": "daiyoku",    # 大浴場（境界の湯）
}

SQUEEZE_LABELS = {
    "onsen":     "♨ 温泉宿",
    "breakfast": "🍳 朝食付き",
    "internet":  "📶 Wi-Fi完備",
    "daiyoku":   "🛁 大浴場あり",
    "kinen":     "🚭 禁煙ルーム",
    "":          "🏨 全タイプ",
}


def get_hotel_section_html(
    pref_name: str,
    wl_key: str,
    accent_color: str = "#7b2ff7",
    accent_light: str = "#c084fc",
    bg_color: str = "#1a0a2e",
    app_id: str = "",
    affil_id: str = "",
) -> str:
    """
    楽天トラベル空室検索ウィジェットHTMLを返す。
    APIキーは 引数 > 環境変数 の優先順位で解決。
    """
    middle_code = PREF_TO_RAKUTEN_CODE.get(pref_name, "")
    if not middle_code:
        return ""

    resolved_app_id   = app_id   or RAKUTEN_APP_ID
    resolved_affil_id = affil_id or RAKUTEN_AFFIL_ID

    if not resolved_app_id:
        return (
            f"\n<!-- ⚠ rakuten_travel: RAKUTEN_APP_ID 未設定。"
            f"$env:RAKUTEN_APP_ID を設定してください -->\n"
        )

    squeeze       = WORLD_LINE_SQUEEZE.get(wl_key, "")
    squeeze_label = SQUEEZE_LABELS.get(squeeze, "🏨 全タイプ")

    return f"""
<!-- ══════════════════════════════════════════════════════════
     楽天トラベル 空室検索ウィジェット
     県: {pref_name} | コード: {middle_code} | 世界線: {wl_key}
     ══════════════════════════════════════════════════════════ -->
<section id="hotel-search" class="hotel-widget">
  <div class="hotel-widget__inner">
    <h2 class="hotel-widget__title">
      <span class="hotel-widget__icon">🏯</span>
      この地の宿を探す
      <span class="hotel-widget__badge">{squeeze_label}</span>
    </h2>
    <p class="hotel-widget__desc">
      {pref_name}の王国を旅した余韻を胸に、実際にこの地に泊まってみませんか。
    </p>
    <div class="hotel-widget__form">
      <div class="hotel-widget__row">
        <label>チェックイン<input type="date" id="ht-checkin"/></label>
        <label>チェックアウト<input type="date" id="ht-checkout"/></label>
        <label>大人
          <select id="ht-adult">
            <option value="1">1名</option>
            <option value="2" selected>2名</option>
            <option value="3">3名</option>
            <option value="4">4名</option>
          </select>
        </label>
      </div>
      <button id="ht-search-btn" onclick="searchHotels()">空室を検索する</button>
    </div>
    <div id="ht-results" class="hotel-widget__results" style="display:none">
      <div id="ht-loading" class="hotel-widget__loading">🔮 王国の宿を探しています...</div>
      <div id="ht-list"    class="hotel-widget__list"></div>
      <div id="ht-more"    class="hotel-widget__more" style="display:none">
        <button onclick="loadMoreHotels()">さらに表示する</button>
      </div>
    </div>
  </div>
</section>

<style>
.hotel-widget{{background:linear-gradient(to bottom,{bg_color}00,{bg_color}cc);border-top:1px solid {accent_color}44;padding:4rem 1.5rem;margin-top:3rem}}
.hotel-widget__inner{{max-width:720px;margin:0 auto}}
.hotel-widget__title{{font-size:1.4rem;color:{accent_light};margin-bottom:.5rem;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}}
.hotel-widget__icon{{font-size:1.6rem}}
.hotel-widget__badge{{font-size:.75rem;background:{accent_color}44;border:1px solid {accent_color};color:{accent_light};padding:.15rem .6rem;border-radius:99px;font-weight:normal}}
.hotel-widget__desc{{color:#888;font-size:.9rem;margin-bottom:1.5rem}}
.hotel-widget__form{{display:flex;flex-direction:column;gap:1rem}}
.hotel-widget__row{{display:flex;gap:1rem;flex-wrap:wrap}}
.hotel-widget__row label{{display:flex;flex-direction:column;gap:.3rem;font-size:.8rem;color:#aaa}}
.hotel-widget__row input,.hotel-widget__row select{{background:#ffffff11;border:1px solid {accent_color}66;color:#e0e0e0;border-radius:6px;padding:.4rem .6rem;font-size:.9rem}}
#ht-search-btn{{background:{accent_color};color:#fff;border:none;border-radius:8px;padding:.7rem 2rem;font-size:1rem;cursor:pointer;width:fit-content;transition:opacity .2s;font-family:inherit}}
#ht-search-btn:hover{{opacity:.85}}
#ht-search-btn:disabled{{opacity:.4;cursor:not-allowed}}
.hotel-widget__results{{margin-top:2rem}}
.hotel-widget__loading{{text-align:center;color:{accent_color};padding:2rem;animation:ht-pulse 1.5s infinite}}
@keyframes ht-pulse{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.hotel-widget__list{{display:flex;flex-direction:column;gap:1rem}}
.hotel-card{{display:flex;gap:1rem;background:#ffffff08;border:1px solid {accent_color}33;border-radius:10px;padding:1rem;text-decoration:none;color:inherit;transition:border-color .2s,background .2s}}
.hotel-card:hover{{border-color:{accent_color};background:#ffffff12}}
.hotel-card__thumb{{width:100px;min-width:100px;height:70px;object-fit:cover;border-radius:6px}}
.hotel-card__thumb-placeholder{{width:100px;min-width:100px;height:70px;border-radius:6px;background:{accent_color}22;display:flex;align-items:center;justify-content:center;font-size:1.5rem}}
.hotel-card__body{{flex:1;min-width:0}}
.hotel-card__name{{font-size:.95rem;color:{accent_light};margin-bottom:.3rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.hotel-card__meta{{font-size:.78rem;color:#888;margin-bottom:.4rem}}
.hotel-card__price{{font-size:.9rem;color:#f7c948}}
.hotel-card__review{{font-size:.75rem;color:#aaa;margin-top:.2rem}}
.hotel-widget__more{{text-align:center;margin-top:1.5rem}}
.hotel-widget__more button{{background:transparent;border:1px solid {accent_color};color:{accent_light};border-radius:8px;padding:.5rem 1.5rem;cursor:pointer;font-family:inherit;font-size:.9rem;transition:background .2s}}
.hotel-widget__more button:hover{{background:{accent_color}33}}
.hotel-widget__error{{text-align:center;color:#f87;padding:1.5rem}}
.hotel-widget__empty{{text-align:center;color:#666;padding:1.5rem}}
</style>

<script>
// ── APIキー（環境変数から生成時に埋め込み済み）────────────────────────
const HT_APP_ID    = "{resolved_app_id}";
const HT_AFFIL_ID  = "{resolved_affil_id}";
const MIDDLE_CODE  = "{middle_code}";
const LARGE_CODE   = "japan";
const SQUEEZE_COND = "{squeeze}";

// ── 日付デフォルト ────────────────────────────────────────────────────
(function(){{
  const today=new Date(), tomorrow=new Date(today);
  tomorrow.setDate(today.getDate()+1);
  const fmt=d=>d.toISOString().split('T')[0];
  document.getElementById('ht-checkin').value  = fmt(today);
  document.getElementById('ht-checkout').value = fmt(tomorrow);
  document.getElementById('ht-checkin').min    = fmt(today);
  document.getElementById('ht-checkout').min   = fmt(tomorrow);
  document.getElementById('ht-checkin').addEventListener('change',function(){{
    const cin=new Date(this.value), cout=new Date(cin);
    cout.setDate(cin.getDate()+1);
    const el=document.getElementById('ht-checkout');
    el.min=fmt(cout);
    if(new Date(el.value)<=cin) el.value=fmt(cout);
  }});
}})();

let _htPage=1, _htLastParams=null;

async function searchHotels(){{
  _htPage=1;
  _htLastParams={{
    checkin:  document.getElementById('ht-checkin').value,
    checkout: document.getElementById('ht-checkout').value,
    adult:    document.getElementById('ht-adult').value,
  }};
  document.getElementById('ht-list').innerHTML='';
  document.getElementById('ht-more').style.display='none';
  document.getElementById('ht-results').style.display='block';
  document.getElementById('ht-loading').style.display='block';
  document.getElementById('ht-search-btn').disabled=true;
  await fetchHotels(1);
  document.getElementById('ht-search-btn').disabled=false;
}}

async function loadMoreHotels(){{
  _htPage++;
  document.getElementById('ht-more').style.display='none';
  document.getElementById('ht-loading').style.display='block';
  await fetchHotels(_htPage);
}}

async function fetchHotels(page){{
  const p=_htLastParams;
  const params=new URLSearchParams({{
    applicationId:   HT_APP_ID,
    largeClassCode:  LARGE_CODE,
    middleClassCode: MIDDLE_CODE,
    checkinDate:     p.checkin,
    checkoutDate:    p.checkout,
    adultNum:        p.adult,
    hits:            '6',
    page:            String(page),
    formatVersion:   '2',
    responseType:    'middle',
    sort:            'standard',
    ...(HT_AFFIL_ID  ? {{affiliateId:HT_AFFIL_ID}}  : {{}}),
    ...(SQUEEZE_COND ? {{squeezeCondition:SQUEEZE_COND}} : {{}}),
  }});
  try{{
    const res=await fetch(`https://app.rakuten.co.jp/services/api/Travel/VacantHotelSearch/20170426?${{params}}`);
    const data=await res.json();
    if(data.error){{ showError('APIエラー: '+(data.error_description||data.error)); return; }}
    const hotels=data.hotels||[];
    document.getElementById('ht-loading').style.display='none';
    if(hotels.length===0&&page===1){{
      document.getElementById('ht-list').innerHTML='<div class="hotel-widget__empty">空室が見つかりませんでした。<br>日程や条件を変えてお試しください。</div>';
      return;
    }}
    const listEl=document.getElementById('ht-list');
    hotels.forEach(h=>{{
      const info=h.hotelBasicInfo||h;
      const charge=h.roomInfo?.[0]?.dailyCharge||{{}};
      const name=info.hotelName||'（名称不明）';
      const url=info.planListUrl||info.hotelInformationUrl||'#';
      const thumb=info.hotelThumbnailUrl||'';
      const station=info.nearestStation?`🚉 ${{info.nearestStation}}`:'';
      const review=info.reviewAverage?`${{'\u2605'.repeat(Math.round(info.reviewAverage))}} ${{info.reviewAverage}} (${{info.reviewCount}}件)`:'';
      const price=info.hotelMinCharge?`¥${{Number(info.hotelMinCharge).toLocaleString()}}〜/泊`:(charge.rakutenCharge?`¥${{Number(charge.rakutenCharge).toLocaleString()}}〜/泊`:'');
      const thumbEl=thumb?`<img class="hotel-card__thumb" src="${{thumb}}" alt="${{name}}" loading="lazy">`:`<div class="hotel-card__thumb-placeholder">🏯</div>`;
      listEl.insertAdjacentHTML('beforeend',`
        <a class="hotel-card" href="${{url}}" target="_blank" rel="noopener">
          ${{thumbEl}}
          <div class="hotel-card__body">
            <div class="hotel-card__name">${{name}}</div>
            <div class="hotel-card__meta">${{station}}</div>
            ${{price  ?`<div class="hotel-card__price">${{price}}</div>`  :''}}
            ${{review ?`<div class="hotel-card__review">${{review}}</div>`:''}}
          </div>
        </a>`);
    }});
    const totalPages=data.pagingInfo?.pageCount||1;
    if(page<totalPages&&page<5) document.getElementById('ht-more').style.display='block';
  }}catch(e){{ showError('通信エラー: '+e.message); }}
}}

function showError(msg){{
  document.getElementById('ht-loading').style.display='none';
  document.getElementById('ht-list').innerHTML=`<div class="hotel-widget__error">⚠ ${{msg}}</div>`;
}}
</script>
<!-- ══════════════════════════════════════════════════════════ -->
"""


# ─── worldkings_novel.py への組み込み方法 ─────────────────────────────
INTEGRATION_PATCH = '''
# ════════════════════════════════════════════════════════
#  rakuten_travel.py の組み込み方（worldkings_novel.py）
# ════════════════════════════════════════════════════════
#
# 【Step 1】 ファイル先頭に1行追加
#   from rakuten_travel import get_hotel_section_html
#
# 【Step 2】 build_html_reader() 内、i18n_block 挿入の直前に追加
#
#   hotel_section = get_hotel_section_html(
#       pref_name=pref_name,
#       wl_key=wl_key,
#       accent_color=accent,
#       accent_light=accent_light,
#       bg_color=bg,
#   )
#   html = html.replace("\\n</body>", f"\\n{hotel_section}\\n</body>")
#
# 【確認コマンド】
#   python -c "from rakuten_travel import RAKUTEN_APP_ID; print(RAKUTEN_APP_ID[:8])"
#   # → 48183afe と表示されればOK
# ════════════════════════════════════════════════════════
'''


if __name__ == "__main__":
    print("=" * 55)
    print("  rakuten_travel.py v2 動作確認")
    print("=" * 55)
    print(f"  RAKUTEN_APP_ID   : {RAKUTEN_APP_ID[:8]}..." if RAKUTEN_APP_ID   else "  RAKUTEN_APP_ID   : ⚠ 未設定")
    print(f"  RAKUTEN_AFFIL_ID : {RAKUTEN_AFFIL_ID[:8]}..." if RAKUTEN_AFFIL_ID else "  RAKUTEN_AFFIL_ID : （未設定・任意）")
    print(f"  対応県数         : {len(PREF_TO_RAKUTEN_CODE)}")

    html = get_hotel_section_html("京都", "封印線", "#7b2ff7", "#c084fc", "#1a0a2e")
    print(f"  生成HTML         : {len(html):,} 文字")
    if RAKUTEN_APP_ID and RAKUTEN_APP_ID in html:
        print("  ✅ アプリIDがHTMLに埋め込まれました")
    elif not RAKUTEN_APP_ID:
        print("  ⚠ 環境変数未設定のためウィジェット非生成")
    print()
    print(INTEGRATION_PATCH)
