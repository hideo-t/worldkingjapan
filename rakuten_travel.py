#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""世界王 × 楽天トラベル v3 - リダイレクト方式（CORS問題回避）"""

import os, urllib.parse

RAKUTEN_APP_ID   = os.environ.get("RAKUTEN_APP_ID",   "")
RAKUTEN_AFFIL_ID = os.environ.get("RAKUTEN_AFFIL_ID", "")

PREF_TO_RAKUTEN_CODE = {
    "北海道":"hokkaido","青森":"aomori","岩手":"iwate","宮城":"miyagi","秋田":"akita",
    "山形":"yamagata","福島":"fukushima","茨城":"ibaraki","栃木":"tochigi","群馬":"gunma",
    "埼玉":"saitama","千葉":"chiba","東京":"tokyo","神奈川":"kanagawa","新潟":"niigata",
    "富山":"toyama","石川":"ishikawa","福井":"fukui","山梨":"yamanashi","長野":"nagano",
    "岐阜":"gifu","静岡":"shizuoka","愛知":"aichi","三重":"mie","滋賀":"shiga",
    "京都":"kyoto","大阪":"osaka","兵庫":"hyogo","奈良":"nara","和歌山":"wakayama",
    "鳥取":"tottori","島根":"shimane","岡山":"okayama","広島":"hiroshima","山口":"yamaguchi",
    "徳島":"tokushima","香川":"kagawa","愛媛":"ehime","高知":"kochi","福岡":"fukuoka",
    "佐賀":"saga","長崎":"nagasaki","熊本":"kumamoto","大分":"oita","宮崎":"miyazaki",
    "鹿児島":"kagoshima","沖縄":"okinawa",
}

WORLD_LINE_KEYWORD = {
    "封印線":"温泉", "商都線":"", "静律線":"朝食付き", "変革線":"WiFi", "境界線":"大浴場",
}
WORLD_LINE_LABEL = {
    "封印線":"♨ 温泉宿", "商都線":"🏨 全タイプ", "静律線":"🍳 朝食付き",
    "変革線":"📶 Wi-Fi完備", "境界線":"🛁 大浴場あり",
}


def get_hotel_section_html(pref_name, wl_key,
    accent_color="#7b2ff7", accent_light="#c084fc", bg_color="#1a0a2e",
    app_id="", affil_id=""):

    code = PREF_TO_RAKUTEN_CODE.get(pref_name, "")
    if not code:
        return ""

    affil   = affil_id or RAKUTEN_AFFIL_ID
    keyword = WORLD_LINE_KEYWORD.get(wl_key, "")
    label   = WORLD_LINE_LABEL.get(wl_key, "🏨 全タイプ")
    kw_js   = f"+'&f_nen='+encodeURIComponent('{keyword}')" if keyword else ""

    return f"""
<!-- rakuten-hotel-widget: {pref_name}_{wl_key} -->
<section id="hotel-search" class="hotel-widget">
  <div class="hotel-widget__inner">
    <h2 class="hotel-widget__title">
      <span>🏯</span> この地の宿を探す
      <span class="hotel-widget__badge">{label}</span>
    </h2>
    <p class="hotel-widget__desc">{pref_name}の王国を旅した余韻を胸に、実際にこの地に泊まってみませんか。</p>
    <div class="hotel-widget__form">
      <div class="hotel-widget__row">
        <label>チェックイン<input type="date" id="ht-ci-{code}"/></label>
        <label>チェックアウト<input type="date" id="ht-co-{code}"/></label>
        <label>大人
          <select id="ht-ad-{code}">
            <option value="1">1名</option><option value="2" selected>2名</option>
            <option value="3">3名</option><option value="4">4名</option>
          </select>
        </label>
      </div>
      <button onclick="htSearch_{code}()">🔍 空室を検索する（楽天トラベル）</button>
    </div>
  </div>
</section>

<style>
.hotel-widget{{background:linear-gradient(to bottom,{bg_color}00,{bg_color}cc);border-top:1px solid {accent_color}44;padding:4rem 1.5rem;margin-top:3rem}}
.hotel-widget__inner{{max-width:720px;margin:0 auto}}
.hotel-widget__title{{font-size:1.4rem;color:{accent_light};margin-bottom:.5rem;display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}}
.hotel-widget__badge{{font-size:.75rem;background:{accent_color}44;border:1px solid {accent_color};color:{accent_light};padding:.15rem .6rem;border-radius:99px;font-weight:normal}}
.hotel-widget__desc{{color:#888;font-size:.9rem;margin-bottom:1.5rem}}
.hotel-widget__form{{display:flex;flex-direction:column;gap:1rem}}
.hotel-widget__row{{display:flex;gap:1rem;flex-wrap:wrap;align-items:flex-end}}
.hotel-widget__row label{{display:flex;flex-direction:column;gap:.3rem;font-size:.8rem;color:#aaa}}
.hotel-widget__row input,.hotel-widget__row select{{background:#ffffff11;border:1px solid {accent_color}66;color:#e0e0e0;border-radius:6px;padding:.4rem .6rem;font-size:.9rem}}
.hotel-widget button{{background:{accent_color};color:#fff;border:none;border-radius:8px;padding:.7rem 2rem;font-size:1rem;cursor:pointer;transition:opacity .2s;font-family:inherit}}
.hotel-widget button:hover{{opacity:.85}}
</style>

<script>
(function(){{
  var fmt=function(d){{return d.toISOString().split('T')[0];}};
  var t=new Date(), t2=new Date(t); t2.setDate(t.getDate()+1);
  var ci=document.getElementById('ht-ci-{code}');
  var co=document.getElementById('ht-co-{code}');
  ci.value=fmt(t); ci.min=fmt(t);
  co.value=fmt(t2); co.min=fmt(t2);
  ci.addEventListener('change',function(){{
    var d=new Date(this.value),nd=new Date(d); nd.setDate(d.getDate()+1);
    co.min=fmt(nd); if(new Date(co.value)<=d) co.value=fmt(nd);
  }});
}})();

function htSearch_{code}(){{
  var ci=document.getElementById('ht-ci-{code}').value.split('-');
  var co=document.getElementById('ht-co-{code}').value.split('-');
  var ad=document.getElementById('ht-ad-{code}').value;
  var url='https://travel.rakuten.co.jp/HOTEL/search/search.php'
    +'?f_area={code}'
    +'&f_otona_su='+ad
    +'&f_s1='+ci[0]+'&f_m1='+ci[1]+'&f_d1='+ci[2]
    +'&f_s2='+co[0]+'&f_m2='+co[1]+'&f_d2='+co[2]
    {kw_js};
  var affil='{affil}';
  if(affil){{
    url='https://hb.afl.rakuten.co.jp/hgc/'+affil+'/?pc='+encodeURIComponent(url)+'&m='+encodeURIComponent(url);
  }}
  window.open(url,'_blank','noopener');
}}
</script>
<!-- /rakuten-hotel-widget -->
"""


if __name__ == "__main__":
    html = get_hotel_section_html("京都", "封印線")
    print(f"✅ 生成HTML: {len(html):,} 文字")
    print(html[:300])
