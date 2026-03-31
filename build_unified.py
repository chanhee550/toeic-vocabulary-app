import json

with open(r"C:\Users\chan7\toeic words\toeic_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)
words_json = json.dumps(words, ensure_ascii=False)

# Read both full HTML files
with open(r"C:\Users\chan7\toeic words\toeic-typing.html", "r", encoding="utf-8") as f:
    pc_full = f.read()
with open(r"C:\Users\chan7\toeic words\toeic-mobile.html", "r", encoding="utf-8") as f:
    mob_full = f.read()

# For PC: extract everything between <body> and </body>
pc_body_s = pc_full.index('<body>') + 6
pc_body_e = pc_full.index('</body>')
pc_inner = pc_full[pc_body_s:pc_body_e]

# For Mobile: extract everything between <body> and </body>
mob_body_s = mob_full.index('<body>') + 6
mob_body_e = mob_full.index('</body>')
mob_inner = mob_full[mob_body_s:mob_body_e]

# Extract PC style
pc_style_s = pc_full.index('<style>') + 7
pc_style_e = pc_full.index('</style>')
pc_css = pc_full[pc_style_s:pc_style_e]

# Extract Mobile style
mob_style_s = mob_full.index('<style>') + 7
mob_style_e = mob_full.index('</style>')
mob_css = mob_full[mob_style_s:mob_style_e]

# Extract PC script
pc_script_s = pc_full.index('<script>') + 8
pc_script_e = pc_full.index('</script>')
pc_js = pc_full[pc_script_s:pc_script_e]

# Extract Mobile script
mob_script_s = mob_full.index('<script>') + 8
mob_script_e = mob_full.index('</script>')
mob_js = mob_full[mob_script_s:mob_script_e]

# Remove <script>...</script> and <footer> from inner bodies since we handle them separately
import re
pc_body_only = pc_inner[:pc_inner.index('<script>')]
mob_body_only = mob_inner[:mob_inner.index('<script>')]

# Remove footers from body (they'll be shared)
pc_body_only = re.sub(r'<footer.*?</footer>', '', pc_body_only, flags=re.DOTALL)
mob_body_only = re.sub(r'<footer.*?</footer>', '', mob_body_only, flags=re.DOTALL)

# Build the test char box CSS (new feature)
test_charbox_css = """
/* ===== TEST CHAR BOXES ===== */
.test-char-boxes {
  display: flex; justify-content: center; gap: 5px;
  margin-bottom: 16px; min-height: 46px; flex-wrap: wrap;
}
.test-char-box {
  width: 38px; height: 46px; display: flex; align-items: center;
  justify-content: center; font-size: 1.25rem; font-weight: 600;
  border-radius: 8px; border: 2px solid var(--border, #2a3050);
  background: var(--bg-card, #151929); color: var(--text-dim, #5a6178);
  font-family: 'Inter', monospace; transition: all 0.15s;
}
.test-char-box.tc-filled { color: var(--text-primary, #eef0f6); border-color: var(--border-hover, #4a5580); }
.test-char-box.tc-correct { color: var(--green, #4ade80); border-color: var(--green-border, rgba(74,222,128,0.3)); background: var(--green-bg, rgba(74,222,128,0.08)); }
.test-char-box.tc-wrong { color: var(--red, #f87171); border-color: var(--red-border, rgba(248,113,113,0.3)); background: var(--red-bg, rgba(248,113,113,0.08)); }
.test-char-box.tc-current { border-color: var(--accent, #6c8cff); box-shadow: 0 0 10px var(--accent-glow, rgba(108,140,255,0.15)); }
.test-char-box.tc-empty { color: var(--text-dim, #5a6178); }
"""

# Scope PC css inside #pc-ver
pc_css_scoped = pc_css.replace('\n  ', '\n  #pc-ver ')
# Fix: don't scope :root, body, and @media
pc_css_scoped = pc_css_scoped.replace('#pc-ver :root', ':root')
pc_css_scoped = pc_css_scoped.replace('#pc-ver body', 'body')
pc_css_scoped = pc_css_scoped.replace('#pc-ver body.light', 'body.light')
pc_css_scoped = pc_css_scoped.replace('#pc-ver @media', '@media')

# Actually, scoping is too error-prone. Let's use iframe-like approach:
# Hide/show entire blocks, and use separate style blocks with scoped-ish selectors.
# Simplest: just embed both CSS as-is but wrap mobile CSS overrides in a media query block.

# SIMPLEST APPROACH: Use two <div> wrappers, toggle visibility with JS.
# CSS from both won't conflict because the HTML structures are different (different IDs).

unified = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#0c0f1a">
<title>TOEIC 영단어장</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans:ital,wght@0,400;1,400&display=swap" rel="stylesheet">

<!-- PC STYLES -->
<style id="pcStyles">
''' + pc_css + test_charbox_css + '''
</style>

<!-- MOBILE STYLES -->
<style id="mobStyles">
''' + mob_css + test_charbox_css + '''
#mobile-ver .test-char-boxes { min-height: 40px; gap: 4px; }
#mobile-ver .test-char-box { width: 32px; height: 40px; font-size: 1.05rem; border-radius: 6px; }
</style>

<style>
/* Toggle visibility */
#pc-ver { display: none; }
#mobile-ver { display: none; }
</style>
</head>
<body>

<div id="pc-ver">
''' + pc_body_only + '''
</div>

<div id="mobile-ver">
''' + mob_body_only + '''
</div>

<footer style="text-align:center;padding:24px 16px 32px;color:var(--text-dim,#5a6178);font-size:0.75rem;line-height:1.6;">
  <div style="margin-bottom:4px;">Made by <strong style="color:var(--text-secondary,#8b92ab);">김찬희 (Kim Chanhee)</strong> &copy; 2026</div>
  <div>단어 데이터 출처: dokjongban.com &middot; MIT License</div>
</footer>

<script>
// ===== DEVICE DETECTION & VERSION SWITCH =====
var _isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  || (navigator.maxTouchPoints > 1 && window.innerWidth < 1024);

if (_isMobile) {
  document.getElementById('mobile-ver').style.display = 'block';
  document.getElementById('pcStyles').disabled = true;
} else {
  document.getElementById('pc-ver').style.display = 'block';
  document.getElementById('mobStyles').disabled = true;
}

// ===== TEST CHAR BOX RENDERER (shared) =====
function renderTestCharBoxes(containerId, targetWord, typedValue) {
  var container = document.getElementById(containerId);
  if (!container) return;
  var h = '';
  for (var i = 0; i < targetWord.length; i++) {
    var cls = 'test-char-box';
    var display = '';
    if (i < typedValue.length) {
      display = typedValue[i];
      cls += typedValue[i].toLowerCase() === targetWord[i].toLowerCase() ? ' tc-correct tc-filled' : ' tc-wrong tc-filled';
    } else if (i === typedValue.length) {
      cls += ' tc-current';
      display = '_';
    } else {
      cls += ' tc-empty';
      display = '_';
    }
    h += '<div class="' + cls + '">' + display + '</div>';
  }
  container.innerHTML = h;
}
</script>

<script>
// ===== PC VERSION =====
if (!_isMobile) {
''' + pc_js + '''
}
</script>

<script>
// ===== MOBILE VERSION =====
if (_isMobile) {
''' + mob_js + '''
}
</script>

</body>
</html>'''

with open(r"C:\Users\chan7\toeic words\toeic-unified.html", "w", encoding="utf-8") as f:
    f.write(unified)

print("Created: toeic-unified.html")
print("Size: %d bytes (%d KB)" % (len(unified), len(unified) // 1024))
