import json, re

with open(r"C:\Users\chan7\toeic words\toeic_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)
words_json = json.dumps(words, ensure_ascii=False)

# Read both full HTML files
with open(r"C:\Users\chan7\toeic words\toeic-typing.html", "r", encoding="utf-8") as f:
    pc_full = f.read()
with open(r"C:\Users\chan7\toeic words\toeic-mobile.html", "r", encoding="utf-8") as f:
    mob_full = f.read()

# Clean up: remove the footer from each (we'll add shared one)
pc_clean = re.sub(r'<footer.*?</footer>', '', pc_full, flags=re.DOTALL)
mob_clean = re.sub(r'<footer.*?</footer>', '', mob_full, flags=re.DOTALL)

# Escape for JS string embedding (backtick template literal won't work in old Safari)
# Instead, we'll store as two hidden textareas and swap innerHTML
# Actually simplest: just write both as complete pages and use document.write

# Approach: Single HTML that detects device in <head>, then document.write the correct full page
unified = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>TOEIC 영단어장</title>
<script>
// Detect mobile immediately and redirect to correct section
var _m = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  || (navigator.maxTouchPoints > 1 && screen.width < 768);
</script>
</head>
<body>
<div id="pc-ver" style="display:none;"></div>
<div id="mobile-ver" style="display:none;"></div>
<noscript>
<p style="text-align:center;padding:40px;font-family:sans-serif;color:#eee;background:#0c0f1a;min-height:100vh;">
JavaScript가 필요합니다.
</p>
</noscript>
<script>
if (!_m) {
  document.getElementById("mobile-ver").remove();
  document.getElementById("pc-ver").outerHTML = PC_HTML;
} else {
  document.getElementById("pc-ver").remove();
  document.getElementById("mobile-ver").outerHTML = MOB_HTML;
}
</script>
</body>
</html>'''

# This approach is tricky because we need to embed full HTML as JS strings.
# Instead, let's use a much simpler approach: iframe-like with srcdoc, or
# better yet: just concatenate into one page with the right version only.
#
# SIMPLEST RELIABLE APPROACH:
# Put a tiny detection script at top, then use document.write() to output
# the correct FULL page (replacing the current document entirely).

unified = '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no"><title>TOEIC</title></head><body><script>\n'
unified += 'var _m=/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)||(navigator.maxTouchPoints>1&&screen.width<768);\n'
unified += 'var PC_PAGE=' + json.dumps(pc_clean) + ';\n'
unified += 'var MOB_PAGE=' + json.dumps(mob_clean) + ';\n'
unified += 'document.open();document.write(_m?MOB_PAGE:PC_PAGE);document.close();\n'
unified += '</'+'script></body></html>'

with open(r"C:\Users\chan7\toeic words\toeic-unified.html", "w", encoding="utf-8") as f:
    f.write(unified)

print("Created: toeic-unified.html")
print("Size: %d bytes (%d KB)" % (len(unified), len(unified) // 1024))
