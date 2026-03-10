#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""世界王 × ホテル予約ウィジェット v4 - 楽天+Booking.com+Agoda 横並び"""

import os, urllib.parse

RAKUTEN_APP_ID   = os.environ.get("RAKUTEN_APP_ID",   "")
RAKUTEN_AFFIL_ID = os.environ.get("RAKUTEN_AFFIL_ID", "")

PREF_TO_RAKUTEN_CODE = {
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

# 英語県名（Booking.com / Agoda 用）
PREF_TO_EN = {
    "北海道":"Hokkaido","青森":"Aomori","岩手":"Iwate","宮城":"Miyagi","秋田":"Akita",
    "山形":"Yamagata","福島":"Fukushima","茨城":"Ibaraki","栃木":"Tochigi","群馬":"Gunma",
    "埼玉":"Saitama","千葉":"Chiba","東京":"Tokyo","神奈川":"Kanagawa","新潟":"Niigata",
    "富山":"Toyama","石川":"Ishikawa","福井":"Fukui","山梨":"Yamanashi","長野":"Nagano",
    "岐阜":"Gifu","静岡":"Shizuoka","愛知":"Aichi","三重":"Mie","滋賀":"Shiga",
    "京都":"Kyoto","大阪":"Osaka","兵庫":"Hyogo","奈良":"Nara","和歌山":"Wakayama",
    "鳥取":"Tottori","島根":"Shimane","岡山":"Okayama","広島":"Hiroshima","山口":"Yamaguchi",
    "徳島":"Tokushima","香川":"Kagawa","愛媛":"Ehime","高知":"Kochi","福岡":"Fukuoka",
    "佐賀":"Saga","長崎":"Nagasaki","熊本":"Kumamoto","大分":"Oita","宮崎":"Miyazaki",
    "鹿児島":"Kagoshima","沖縄":"Okinawa",
}

# Booking.com キーワード補完（英語）


def get_hotel_section_html(pref_name, wl_key,
    accent_color="#7b2ff7", accent_light="#c084fc", bg_color="#1a0a2e",
    app_id="", affil_id=""):

    code   = PREF_TO_RAKUTEN_CODE.get(pref_name, "")
    pref_en = PREF_TO_EN.get(pref_name, pref_name)
    if not code:
        return ""

    affil   = affil_id or RAKUTEN_AFFIL_ID

    # Booking.com 検索URL（ss=県名+Japan）
    bk_query = urllib.parse.quote(f"{pref_en} Japan")
    booking_url = f"https://www.booking.com/search.html?ss={bk_query}&lang=en-us"

    # Agoda 検索URL
    agoda_query = urllib.parse.quote(f"{pref_en}, Japan")
    agoda_url = f"https://www.agoda.com/search?city={pref_en}&country=Japan&area=Japan&locale=en-us&ckuid=&prid=0&currency=USD&correlationId=&tag=&device=desktop&networkType=&travellerType=&checkIn=&los=1&rooms=1&adults=2&children=0&searchrequestid=&travelPurpose=leisure&q={agoda_query}"

    return f"""
<!-- rakuten-hotel-widget: {pref_name}_{wl_key} -->
<section id="hotel-search" class="hotel-widget">
  <div class="hotel-widget__inner">
    <h2 class="hotel-widget__title"><span>🏯</span> この地の宿を探す</h2>
    <p class="hotel-widget__desc">{pref_name}の王国を旅した余韻を胸に、実際にこの地に泊まってみませんか。</p>

    <div class="hotel-widget__form">
      <div class="hotel-widget__btns">
        <button class="ht-btn ht-btn--rakuten" onclick="htSearch_{code}('rakuten')">
          <img src="https://www.rakuten.co.jp/favicon.ico" onerror="this.style.display='none'" width="14" height="14"> 楽天トラベル
        </button>
        <button class="ht-btn ht-btn--booking" onclick="htSearch_{code}('booking')">
          <span style="font-weight:700;letter-spacing:-.5px">b.</span> Booking.com
        </button>
        <button class="ht-btn ht-btn--agoda" onclick="htSearch_{code}('agoda')">
          ✦ Agoda
        </button>
      </div>
    </div>
  </div>
</section>

<style>
.hotel-widget{{background:linear-gradient(to bottom,{bg_color}00,{bg_color}cc);border-top:1px solid {accent_color}44;padding:4rem 1.5rem;margin-top:3rem}}
.hotel-widget__inner{{max-width:720px;margin:0 auto}}
.hotel-widget__title{{font-size:1.3rem;color:{accent_light};margin-bottom:.5rem;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}}
.hotel-widget__desc{{color:#888;font-size:.9rem;margin-bottom:1.5rem}}
.hotel-widget__form{{display:flex;flex-direction:column;gap:1.2rem}}
.hotel-widget__row{{display:flex;gap:1rem;flex-wrap:wrap;align-items:flex-end}}
.hotel-widget__row label{{display:flex;flex-direction:column;gap:.3rem;font-size:.78rem;color:#aaa}}
.hotel-widget__row input,.hotel-widget__row select{{background:#ffffff11;border:1px solid {accent_color}55;color:#e0e0e0;border-radius:6px;padding:.4rem .6rem;font-size:.88rem;min-width:0}}
.hotel-widget__btns{{display:flex;gap:.7rem;flex-wrap:wrap}}
.ht-btn{{display:inline-flex;align-items:center;gap:.4rem;border:none;border-radius:8px;padding:.65rem 1.4rem;font-size:.9rem;cursor:pointer;font-family:inherit;transition:opacity .2s,transform .15s;white-space:nowrap}}
.ht-btn:hover{{opacity:.85;transform:translateY(-1px)}}
.ht-btn--rakuten{{background:#bf0000;color:#fff}}
.ht-btn--booking{{background:#003580;color:#fff}}
.ht-btn--agoda{{background:#e43 ;color:#fff}}
</style>

<script>
(function(){{
  var fmt=function(d){{return d.toISOString().split('T')[0];}};
  var t=new Date(),t2=new Date(t);t2.setDate(t.getDate()+1);
  var ci=document.getElementById('ht-ci-{code}');
  var co=document.getElementById('ht-co-{code}');
  ci.value=fmt(t);ci.min=fmt(t);
  co.value=fmt(t2);co.min=fmt(t2);
  ci.addEventListener('change',function(){{
    var d=new Date(this.value),nd=new Date(d);nd.setDate(d.getDate()+1);
    co.min=fmt(nd);if(new Date(co.value)<=d)co.value=fmt(nd);
  }});
}})();

function htSearch_{code}(site){{
  var url='';
  if(site==='rakuten'){{
    url='https://travel.rakuten.co.jp/yado/{code}/';
  }} else if(site==='booking'){{
    url='https://www.booking.com/search.html'
      +'?ss='+encodeURIComponent('{pref_en} Japan')
      +'&checkin='+ci[0]+'-'+ci[1]+'-'+ci[2]
      +'&checkout='+co[0]+'-'+co[1]+'-'+co[2]
      +'&group_adults='+ad
      +'&no_rooms=1&lang=en-us';
  }} else if(site==='agoda'){{
    url='https://www.agoda.com/search?city='+encodeURIComponent('{pref_en}')
      +'&country=Japan'
      +'&checkIn='+ci[0]+'-'+ci[1]+'-'+ci[2]
      +'&los=1'
      +'&rooms=1&adults='+ad
      +'&children=0&locale=en-us';
  }}
  window.open(url,'_blank','noopener');
}}
</script>
<!-- /rakuten-hotel-widget -->
"""


if __name__ == "__main__":
    html = get_hotel_section_html("京都", "封印線")
    print(f"✅ 生成HTML: {len(html):,} 文字")
    print(html[:400])
