"""
iOS 전용 TOEIC 단어장 빌드 스크립트
- toeic-mobile.html 기반 + iOS Safari 호환성 패치
- Safari 9+ 지원 (padStart, includes, closest, classList.toggle 대체)
"""
import json, re

with open(r"C:\Users\chan7\toeic words\toeic_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

with open(r"C:\Users\chan7\toeic words\toeic-mobile.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix duplicate apple-mobile-web-app-capable (add iOS-specific meta instead)
html = html.replace(
    '<meta name="apple-mobile-web-app-capable" content="yes">',
    '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n<meta name="format-detection" content="telephone=no">',
    1  # only first occurrence
)

# 2. Add polyfills for Safari 9 compatibility right after <script> opening
polyfills = """
// === iOS Safari Polyfills ===
if(!String.prototype.includes){String.prototype.includes=function(s,p){return this.indexOf(s,p||0)!==-1;};}
if(!String.prototype.padStart){String.prototype.padStart=function(len,fill){var s=String(fill||' ');var r=String(this);while(r.length<len)r=s+r;return r.slice(-len);};}
if(!Array.prototype.includes){Array.prototype.includes=function(v,i){return this.indexOf(v,i||0)!==-1;};}
if(!Element.prototype.closest){Element.prototype.closest=function(s){var el=this;while(el&&el.nodeType===1){if(el.matches(s))return el;el=el.parentElement;}return null;};}
if(!Element.prototype.matches){Element.prototype.matches=Element.prototype.msMatchesSelector||Element.prototype.webkitMatchesSelector||function(s){var m=(this.document||this.ownerDocument).querySelectorAll(s);for(var i=0;i<m.length;i++){if(m[i]===this)return true;}return false;};}
// classList.toggle polyfill for 2-arg form
(function(){var t=document.createElement('div');t.classList.toggle('x',false);if(t.classList.contains('x')){var orig=DOMTokenList.prototype.toggle;DOMTokenList.prototype.toggle=function(c,f){if(arguments.length>1){if(f)this.add(c);else this.remove(c);return f;}return orig.call(this,c);};}})();
// === End Polyfills ===
"""

# Find the first <script> tag in the body (after all HTML)
# Insert polyfills right after the first <script> in the JS section
script_tag = '<script>\n'
first_script_pos = html.find(script_tag, html.find('<body>'))
if first_script_pos != -1:
    insert_pos = first_script_pos + len(script_tag)
    html = html[:insert_pos] + polyfills + html[insert_pos:]

with open(r"C:\Users\chan7\toeic words\toeic-ios.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Created: toeic-ios.html")
print("Size: %d bytes (%d KB)" % (len(html), len(html) // 1024))
