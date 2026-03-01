# -*- coding: utf-8 -*-
"""
詳細ページパッチ v3
- Google翻訳ウィジェット
- 戻るリンク
- ストーリーナビゲーション（前の物語 / ランダム / 次の物語）
既存パッチは自動で置き換え
"""
import re
import json
from pathlib import Path


def build_story_list(base: Path) -> list[str]:
    """全物語フォルダ名をスキャンしてソート済みリストを返す"""
    stories = []
    for d in sorted(base.iterdir()):
        if d.is_dir() and (d / "index.html").exists():
            stories.append(d.name)
    return stories


def make_inject_block(story_list_json: str) -> str:
    return f'''
<!-- i18n patch v3 -->
<style>
.back-link{{position:fixed;top:12px;left:12px;z-index:9999;color:#888;text-decoration:none;font-size:.85rem;padding:4px 10px;background:rgba(255,255,255,.06);border-radius:4px;border:1px solid rgba(255,255,255,.1);transition:.2s}}
.back-link:hover{{color:#fff;background:rgba(255,255,255,.12)}}
.translated-ltr .back-link,.translated-rtl .back-link{{top:50px}}
.gtranslate-wrap{{position:fixed;top:10px;right:12px;z-index:9999}}
.translated-ltr .gtranslate-wrap,.translated-rtl .gtranslate-wrap{{top:50px}}
.goog-te-gadget{{font-size:0!important}}
.goog-te-gadget .goog-te-combo{{
  background:rgba(20,20,30,.9)!important;
  border:1px solid rgba(255,255,255,.2)!important;
  color:#ccc!important;
  padding:5px 8px;border-radius:4px;font-size:.8rem;
  cursor:pointer;outline:none;
}}
.goog-te-gadget .goog-te-combo option{{background:#1a1a2e;color:#ccc}}
.goog-te-banner-frame{{display:none!important}}
body{{top:0!important;padding-bottom:60px}}
.story-nav{{position:fixed;bottom:0;left:0;right:0;z-index:9999;display:flex;justify-content:center;align-items:center;gap:8px;padding:10px 12px;background:rgba(10,10,20,.95);border-top:1px solid rgba(255,255,255,.08);backdrop-filter:blur(10px)}}
.story-nav a,.story-nav button{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);color:#aaa;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:.8rem;text-decoration:none;transition:.2s;white-space:nowrap}}
.story-nav a:hover,.story-nav button:hover{{background:rgba(201,168,76,.15);border-color:rgba(201,168,76,.3);color:#c9a84c}}
.story-nav .nav-label{{font-size:.65rem;color:#555;display:block;text-align:center;line-height:1}}
.story-nav .nav-name{{font-size:.75rem;color:#bbb;display:block;text-align:center;line-height:1.3;margin-top:2px;max-width:120px;overflow:hidden;text-overflow:ellipsis}}
.story-nav .nav-random{{background:rgba(201,168,76,.1);border-color:rgba(201,168,76,.2);color:#c9a84c;font-size:.9rem;padding:8px 20px}}
@media(max-width:600px){{
  .story-nav{{gap:4px;padding:8px 6px}}
  .story-nav a,.story-nav button{{padding:6px 10px;font-size:.7rem}}
  .story-nav .nav-name{{max-width:80px;font-size:.65rem}}
}}
</style>
<a class="back-link" href="../../index.html">← 戻る</a>
<div class="gtranslate-wrap">
<div id="google_translate_element"></div>
</div>
<div class="story-nav" id="storyNav"></div>
<script>
function googleTranslateElementInit(){{
  new google.translate.TranslateElement({{
    pageLanguage:'ja',
    includedLanguages:'ja,en,zh-CN,ko',
    layout:google.translate.TranslateElement.InlineLayout.SIMPLE,
    autoDisplay:false
  }},'google_translate_element');
}}
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
<script>
(function(){{
  // Auto-select language
  var p=new URLSearchParams(location.search);
  var lang=p.get('lang');
  if(lang&&lang!=='ja'){{
    var map={{en:'en',zh:'zh-CN',ko:'ko'}};
    var target=map[lang]||lang;
    var attempts=0;
    var iv=setInterval(function(){{
      attempts++;
      var sel=document.querySelector('.goog-te-combo');
      if(sel){{sel.value=target;sel.dispatchEvent(new Event('change'));clearInterval(iv);}}
      if(attempts>50)clearInterval(iv);
    }},200);
  }}

  // Story navigation
  var ALL_STORIES={story_list_json};
  var path=location.pathname;
  var match=path.match(/worldkings_output\\/([^\\/]+)\\//);
  if(!match)match=path.match(/worldkings_output%2F([^%\\/]+)/);
  var current=match?decodeURIComponent(match[1]):'';
  var idx=ALL_STORIES.indexOf(current);
  var nav=document.getElementById('storyNav');

  function storyUrl(name){{
    return encodeURI('../'+name+'/index.html')+(lang?'?lang='+lang:'');
  }}
  function displayName(name){{
    var parts=name.split('_');
    return parts[0]+'\\n'+parts.slice(1).join('_');
  }}

  if(idx>=0&&nav){{
    var prevIdx=(idx-1+ALL_STORIES.length)%ALL_STORIES.length;
    var nextIdx=(idx+1)%ALL_STORIES.length;
    var prevName=ALL_STORIES[prevIdx];
    var nextName=ALL_STORIES[nextIdx];

    nav.innerHTML=
      '<a href="'+storyUrl(prevName)+'" title="'+prevName+'">'+
        '<span class="nav-label">← 前</span>'+
        '<span class="nav-name">'+prevName.split('_')[0]+'</span>'+
      '</a>'+
      '<button class="nav-random" onclick="goRandom()" title="ランダム">🎲</button>'+
      '<a href="'+storyUrl(nextName)+'" title="'+nextName+'">'+
        '<span class="nav-label">次 →</span>'+
        '<span class="nav-name">'+nextName.split('_')[0]+'</span>'+
      '</a>';
  }}

  window.goRandom=function(){{
    var r=idx;
    while(r===idx&&ALL_STORIES.length>1)r=Math.floor(Math.random()*ALL_STORIES.length);
    location.href=storyUrl(ALL_STORIES[r]);
  }};
}})();
</script>
'''


def patch_file(filepath: Path, inject_block: str) -> bool:
    content = filepath.read_text(encoding='utf-8')

    # Remove any old patch
    if '<!-- i18n patch' in content:
        content = re.sub(
            r'\n*<!-- i18n patch[^>]*-->.*?</script>\s*(?=\n*</body>)',
            '', content, flags=re.DOTALL
        )
        print(f"  (old patch removed)")

    if '</body>' in content:
        content = content.replace('</body>', inject_block + '\n</body>')
        filepath.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    base = Path('worldkings_output')
    if not base.exists():
        print(f"Error: {base} not found. Run from the worldkingjapan directory.")
        return

    # Build story list
    stories = build_story_list(base)
    print(f"Found {len(stories)} stories")
    story_json = json.dumps(stories, ensure_ascii=False)
    inject_block = make_inject_block(story_json)

    patched = 0
    errors = 0

    for html_file in sorted(base.rglob('index.html')):
        # Only patch direct children (not subdirs)
        if html_file.parent.parent == base:
            try:
                if patch_file(html_file, inject_block):
                    patched += 1
                    print(f"✓ {html_file.parent.name}")
            except Exception as e:
                errors += 1
                print(f"✗ {html_file}: {e}")

    print(f"\n完了: {patched} patched, {errors} errors")


if __name__ == '__main__':
    main()
