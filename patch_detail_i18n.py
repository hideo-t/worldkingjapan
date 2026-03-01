# -*- coding: utf-8 -*-
"""
詳細ページ多言語パッチ
既存の worldkings_output/*/index.html に多言語UIを注入する
"""
import os
from pathlib import Path

# 注入するCSS + JS
I18N_INJECT = '''
<!-- i18n patch -->
<style>
.lang-bar{position:fixed;top:12px;right:12px;z-index:999;display:flex;gap:4px}
.lang-btn{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);color:#aaa;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:.75rem;transition:.2s}
.lang-btn:hover{background:rgba(255,255,255,.15)}
.lang-btn.active{background:rgba(201,168,76,.2);border-color:rgba(201,168,76,.4);color:#c9a84c}
.back-link{position:fixed;top:12px;left:12px;z-index:999;color:#888;text-decoration:none;font-size:.85rem;padding:4px 10px;background:rgba(255,255,255,.06);border-radius:4px;border:1px solid rgba(255,255,255,.1)}
.back-link:hover{color:#fff;background:rgba(255,255,255,.12)}
</style>
<a class="back-link" href="../../index.html" id="backLink">← 戻る</a>
<div class="lang-bar">
<button class="lang-btn active" onclick="setDetailLang('ja')">日本語</button>
<button class="lang-btn" onclick="setDetailLang('en')">EN</button>
<button class="lang-btn" onclick="setDetailLang('zh')">中文</button>
<button class="lang-btn" onclick="setDetailLang('ko')">한국</button>
</div>
<script>
const DI18N={
ja:{title:"世界王",tagline:"この国は、見えない王たちに守られている。",footer:"あなたの町にも、王がいる。",crest:"紋章",color:"色",symbol:"象徴",back:"← 戻る",
wl:{封印線:"封印線",商都線:"商都線",静律線:"静律線",変革線:"変革線",境界線:"境界線"}},
en:{title:"World Kings",tagline:"This land is guarded by invisible kings.",footer:"There is a king in your town, too.",crest:"Crest",color:"Colors",symbol:"Symbol",back:"← Back",
wl:{封印線:"Seal Line",商都線:"Trade Line",静律線:"Zen Line",変革線:"Revolution Line",境界線:"Border Line"}},
zh:{title:"世界王",tagline:"这个国家，被看不见的王守护着。",footer:"你的城市里，也有一位王。",crest:"纹章",color:"颜色",symbol:"象征",back:"← 返回",
wl:{封印線:"封印线",商都線:"商都线",静律線:"静律线",変革線:"变革线",境界線:"境界线"}},
ko:{title:"세계왕",tagline:"이 나라는 보이지 않는 왕들에 의해 지켜지고 있다.",footer:"당신의 마을에도 왕이 있다.",crest:"문장",color:"색",symbol:"상징",back:"← 뒤로",
wl:{封印線:"봉인선",商都線:"상도선",静律線:"정률선",変革線:"변혁선",境界線:"경계선"}}
};
let curLang='ja';
function setDetailLang(l){
curLang=l;
document.querySelectorAll('.lang-btn').forEach(b=>b.classList.remove('active'));
document.querySelector('.lang-btn[onclick="setDetailLang(\\''+l+'\\')"]').classList.add('active');
const t=DI18N[l];
// Title
const h1=document.querySelector('.hero h1');
if(h1){const orig=h1.getAttribute('data-orig');if(!orig)h1.setAttribute('data-orig',h1.textContent);
const parts=(orig||h1.textContent).split('──');
if(l==='ja')h1.textContent=orig||h1.textContent;
else h1.textContent=t.title+' ── '+parts[1].trim();}
// Subtitle world line name
const sub=document.querySelector('.hero .subtitle');
if(sub){const origS=sub.getAttribute('data-orig');if(!origS)sub.setAttribute('data-orig',sub.textContent);
if(l==='ja'){sub.textContent=origS||sub.textContent;}
else{let txt=origS||sub.textContent;for(const[jk,ev] of Object.entries(t.wl)){txt=txt.replace(new RegExp(jk.replace('線','線?'),'g'),ev);}sub.textContent=txt;}}
// Tagline
const tl=document.querySelector('.hero .tagline');
if(tl)tl.textContent=t.tagline;
// Footer
const ft=document.querySelector('.footer');
if(ft)ft.textContent=t.footer;
// Emblem info
const ei=document.querySelector('.emblem-info');
if(ei){const origE=ei.getAttribute('data-orig');if(!origE)ei.setAttribute('data-orig',ei.textContent);
if(l==='ja'){ei.textContent=origE||ei.textContent;}
else{let etxt=origE||ei.textContent;etxt=etxt.replace('紋章',t.crest).replace(/色：/g,t.color+'：').replace('象徴',t.symbol);
for(const[jk,ev] of Object.entries(t.wl)){etxt=etxt.replace(jk,ev);}ei.textContent=etxt;}}
// Back link
const bl=document.getElementById('backLink');
if(bl){bl.textContent=t.back;bl.href='../../index.html'+(l!=='ja'?'#lang='+l:'');}
}
// Auto-detect lang from URL or browser
(function(){
const p=new URLSearchParams(location.search);
const ul=p.get('lang');
if(ul&&DI18N[ul])setDetailLang(ul);
else{const bl=(navigator.language||'').substring(0,2);if(['en','zh','ko'].includes(bl))setDetailLang(bl);}
})();
</script>
'''

def patch_file(filepath: Path):
    """Patch a single detail index.html"""
    content = filepath.read_text(encoding='utf-8')
    
    # Skip if already patched
    if 'i18n patch' in content:
        return False
    
    # Inject before </body>
    if '</body>' in content:
        content = content.replace('</body>', I18N_INJECT + '\n</body>')
        filepath.write_text(content, encoding='utf-8')
        return True
    return False

def main():
    base = Path('worldkings_output')
    if not base.exists():
        print(f"Error: {base} not found. Run from the worldkingjapan directory.")
        return
    
    patched = 0
    skipped = 0
    errors = 0
    
    for html_file in sorted(base.rglob('index.html')):
        try:
            if patch_file(html_file):
                patched += 1
                print(f"✓ {html_file}")
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"✗ {html_file}: {e}")
    
    print(f"\n完了: {patched} patched, {skipped} skipped, {errors} errors")

if __name__ == '__main__':
    main()
