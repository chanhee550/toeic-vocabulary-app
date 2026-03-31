import markdown
import os

with open(r"C:\Users\chan7\toeic words\REPORT.md", "r", encoding="utf-8") as f:
    md_content = f.read()

html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

html = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>TOEIC 영단어장 - 개발 보고서</title>
<style>
  @page { margin: 20mm 18mm; size: A4; }
  body {
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    font-size: 11pt; line-height: 1.8; color: #222;
    max-width: 720px; margin: 0 auto; padding: 40px 20px;
  }
  h1 { font-size: 20pt; color: #1a237e; border-bottom: 3px solid #1a237e; padding-bottom: 10px; margin-bottom: 24px; }
  h2 { font-size: 15pt; color: #283593; margin-top: 32px; margin-bottom: 12px; border-left: 4px solid #3f51b5; padding-left: 12px; }
  h3 { font-size: 12pt; color: #37474f; margin-top: 20px; margin-bottom: 8px; }
  p { margin: 8px 0; text-align: justify; }
  ul, ol { margin: 8px 0 8px 20px; }
  li { margin: 4px 0; }
  table { border-collapse: collapse; width: 100%; margin: 16px 0; }
  th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; font-size: 10pt; }
  th { background: #e8eaf6; font-weight: bold; }
  tr:nth-child(even) td { background: #fafafa; }
  code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-size: 10pt; font-family: 'Consolas', monospace; }
  strong { color: #1a237e; }
  hr { border: none; border-top: 1px solid #ddd; margin: 24px 0; }
  @media print {
    body { padding: 0; }
    h1, h2 { page-break-after: avoid; }
    table { page-break-inside: avoid; }
  }
</style>
</head>
<body>
''' + html_body + '''
</body>
</html>'''

output_path = r"C:\Users\chan7\toeic words\REPORT.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Created: REPORT.html")
print("브라우저에서 열린 후 Ctrl+P → PDF로 저장하세요")

# Auto-open in browser
os.startfile(output_path)
