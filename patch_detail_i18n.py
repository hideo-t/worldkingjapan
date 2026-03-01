# -*- coding: utf-8 -*-
"""
詳細ページ多言語パッチ v2
Google翻訳ウィジェット + 戻るリンクを注入
既存の worldkings_output/*/index.html に適用
v1パッチがある場合は自動で置き換え
"""
import re
from pathlib import Path

I18N_INJECT_V2 = '''
<!-- i18n patch v2 -->
<style>
.back-link{position:fixed;top:12px;left:12px;z-index:9999;color:#888;text-decoration:none;font-size:.85rem;padding:4px 10px;background:rgba(255,255,255,.06);border-radius:4px;border:1px solid rgba(255,255,255,.1);transition:.2s}
.back-link:hover{color:#fff;background:rgba(255,255,255,.12)}
.gtranslate-wrap{position:fixed;top:10px;right:12px;z-index:9999}
.goog-te-gadget{font-size:0!important}
.goog-te-gadget .goog-te-combo{
  background:rgba(20,20,30,.9)!important;
  border:1px solid rgba(255,255,255,.2)!important;
  color:#ccc!important;
  padding:5px 8px;border-radius:4px;font-size:.8rem;
  cursor:pointer;outline:none;
}
.goog-te-gadget .goog-te-combo option{background:#1a1a2e;color:#ccc}
.goog-te-banner-frame{display:none!important}
body{top:0!important}
</style>
<a class="back-link" href="../../index.html">← 戻る</a>
<div class="gtranslate-wrap">
<div id="google_translate_element"></div>
</div>
<script>
function googleTranslateElementInit(){
  new google.translate.TranslateElement({
    pageLanguage:'ja',
    includedLanguages:'ja,en,zh-CN,ko',
    layout:google.translate.TranslateElement.InlineLayout.SIMPLE,
    autoDisplay:false
  },'google_translate_element');
}
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
<script>
(function(){
  var p=new URLSearchParams(location.search);
  var lang=p.get('lang');
  if(lang&&lang!=='ja'){
    var map={en:'en',zh:'zh-CN',ko:'ko'};
    var target=map[lang]||lang;
    var attempts=0;
    var iv=setInterval(function(){
      attempts++;
      var sel=document.querySelector('.goog-te-combo');
      if(sel){sel.value=target;sel.dispatchEvent(new Event('change'));clearInterval(iv);}
      if(attempts>50)clearInterval(iv);
    },200);
  }
})();
</script>
'''


def patch_file(filepath: Path):
    content = filepath.read_text(encoding='utf-8')

    # Remove old v1 or v2 patch if present
    if '<!-- i18n patch' in content:
        content = re.sub(
            r'\n*<!-- i18n patch[^>]*-->.*?</script>\s*(?=\n*</body>)',
            '', content, flags=re.DOTALL
        )
        print(f"  (old patch removed)")

    if '</body>' in content:
        content = content.replace('</body>', I18N_INJECT_V2 + '\n</body>')
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
