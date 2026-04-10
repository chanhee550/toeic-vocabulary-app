"""
AX(접근성) 검사 스크립트 - Python 기반 (방법 C)
HTML 파일을 파싱하여 접근성 문제를 정적으로 분석합니다.

사용법: python ax_check_python.py
"""

import os
import sys
import re
import io
from bs4 import BeautifulSoup

# Windows 콘솔 UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── 검사 대상 HTML 파일 ──
TARGET_FILES = [
    "index.html",
    "toeic-typing.html",
    "toeic-mobile.html",
    "toeic-unified.html",
    "toeic-ios.html",
]

# ── 결과 저장 ──
class Issue:
    def __init__(self, severity, rule, message, element=""):
        self.severity = severity  # "ERROR", "WARNING", "INFO"
        self.rule = rule
        self.message = message
        self.element = element[:120] if element else ""

    def __str__(self):
        tag = {"ERROR": "❌", "WARNING": "⚠️", "INFO": "💡"}[self.severity]
        line = f"  {tag} [{self.rule}] {self.message}"
        if self.element:
            line += f"\n      → {self.element}"
        return line


def check_file(filepath):
    """하나의 HTML 파일에 대해 AX 검사를 수행합니다."""
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")
    issues = []

    # ── 1. lang 속성 검사 ──
    html_tag = soup.find("html")
    if html_tag and not html_tag.get("lang"):
        issues.append(Issue("ERROR", "html-lang", "<html>에 lang 속성이 없습니다"))

    # ── 2. 이미지 alt 텍스트 ──
    for img in soup.find_all("img"):
        if not img.get("alt") and img.get("alt") != "":
            issues.append(Issue("ERROR", "img-alt", "이미지에 alt 속성이 없습니다", str(img)[:120]))

    # ── 3. 버튼 접근성 ──
    for btn in soup.find_all("button"):
        text = btn.get_text(strip=True)
        aria_label = btn.get("aria-label", "")
        aria_labelledby = btn.get("aria-labelledby", "")
        title = btn.get("title", "")

        # 텍스트가 이모지만 있거나 비어있으면 문제
        if not aria_label and not aria_labelledby and not title:
            clean_text = re.sub(r'[\U00010000-\U0010ffff\u2600-\u27bf\u2b50\u2b55\u23cf-\u23fa\u200d\ufe0f]', '', text).strip()
            if not clean_text:
                issues.append(Issue("ERROR", "button-name", "버튼에 접근 가능한 이름이 없습니다 (aria-label 필요)", str(btn)[:120]))

    # ── 4. 입력 필드 라벨 ──
    for inp in soup.find_all("input"):
        if inp.get("type") in ("hidden", "submit", "button", "reset"):
            continue
        inp_id = inp.get("id", "")
        aria_label = inp.get("aria-label", "")
        aria_labelledby = inp.get("aria-labelledby", "")
        has_label = False
        if inp_id:
            has_label = soup.find("label", attrs={"for": inp_id}) is not None
        if not has_label and not aria_label and not aria_labelledby:
            issues.append(Issue("ERROR", "input-label", "입력 필드에 연결된 <label> 또는 aria-label이 없습니다", str(inp)[:120]))

    # ── 5. select 라벨 ──
    for sel in soup.find_all("select"):
        sel_id = sel.get("id", "")
        aria_label = sel.get("aria-label", "")
        has_label = False
        if sel_id:
            has_label = soup.find("label", attrs={"for": sel_id}) is not None
        if not has_label and not aria_label:
            issues.append(Issue("WARNING", "select-label", "<select>에 연결된 라벨이 없습니다", str(sel)[:120]))

    # ── 6. 시맨틱 HTML 검사 ──
    semantic_tags = {"header", "nav", "main", "footer", "section", "article", "aside"}
    found_semantic = {tag for tag in semantic_tags if soup.find(tag)}
    missing = semantic_tags - found_semantic
    important_missing = {"main", "nav"} & missing
    if important_missing:
        issues.append(Issue("WARNING", "semantic-html",
                            f"시맨틱 태그 누락: {', '.join(f'<{t}>' for t in sorted(important_missing))}"))

    # ── 7. 제목 계층 구조 ──
    headings = soup.find_all(re.compile(r'^h[1-6]$'))
    if headings:
        levels = [int(h.name[1]) for h in headings]
        for i in range(1, len(levels)):
            if levels[i] > levels[i - 1] + 1:
                issues.append(Issue("WARNING", "heading-order",
                                    f"제목 레벨 건너뜀: h{levels[i-1]} → h{levels[i]}"))
                break
    else:
        issues.append(Issue("INFO", "heading-order", "페이지에 제목(h1~h6)이 없습니다"))

    # ── 8. 모달/다이얼로그 role 검사 ──
    modals_by_class = soup.find_all(class_=re.compile(r'modal|dialog|overlay|popup', re.I))
    for modal in modals_by_class:
        role = modal.get("role", "")
        if role not in ("dialog", "alertdialog"):
            issues.append(Issue("WARNING", "dialog-role",
                                "모달/다이얼로그에 role=\"dialog\"이 없습니다",
                                f"<{modal.name} class=\"{' '.join(modal.get('class', []))}\">"))

    # ── 9. aria-live 검사 (동적 콘텐츠) ──
    live_regions = soup.find_all(attrs={"aria-live": True})
    if not live_regions:
        # 동적 콘텐츠가 있는지 확인 (JS에서 innerHTML 변경하는 요소)
        scripts = soup.find_all("script")
        has_dynamic = any("innerHTML" in str(s) or "textContent" in str(s) for s in scripts)
        if has_dynamic:
            issues.append(Issue("INFO", "aria-live",
                                "동적 콘텐츠가 있지만 aria-live 리전이 없습니다. 스크린 리더가 변경을 감지 못할 수 있습니다"))

    # ── 10. outline:none 검사 (포커스 표시 제거) ──
    styles = soup.find_all("style")
    all_css = " ".join(str(s) for s in styles)
    if "outline: none" in all_css or "outline:none" in all_css:
        if ":focus-visible" not in all_css:
            issues.append(Issue("WARNING", "focus-visible",
                                "outline:none이 사용되었지만 :focus-visible 대체 스타일이 없습니다. 키보드 사용자가 포커스를 볼 수 없습니다"))

    # ── 11. 색상 대비 (CSS 변수 기반 간이 검사) ──
    dim_colors = re.findall(r'color:\s*#([0-9a-fA-F]{6})', all_css)
    for color_hex in dim_colors:
        r, g, b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
        # 상대 휘도 계산 (간이)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        if luminance < 0.25:
            issues.append(Issue("INFO", "color-contrast",
                                f"어두운 색상 #{color_hex} (휘도:{luminance:.2f}) — 어두운 배경에서 대비 부족 가능"))
            break  # 한 번만 경고

    # ── 12. tabindex 남용 검사 ──
    positive_tabindex = soup.find_all(attrs={"tabindex": re.compile(r'^[1-9]')})
    if positive_tabindex:
        issues.append(Issue("WARNING", "tabindex",
                            f"양수 tabindex 발견 ({len(positive_tabindex)}개). Tab 순서가 예측 불가능할 수 있습니다"))

    return issues


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    total_issues = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    all_results = {}

    print("=" * 60)
    print("  🔍 AX(접근성) 검사 — Python 정적 분석")
    print("=" * 60)

    for filename in TARGET_FILES:
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            print(f"\n⏭️  {filename} — 파일 없음, 건너뜀")
            continue

        issues = check_file(filepath)
        all_results[filename] = issues

        print(f"\n{'─' * 50}")
        print(f"📄 {filename}")
        print(f"{'─' * 50}")

        if not issues:
            print("  ✅ 문제 없음!")
        else:
            for issue in issues:
                total_issues[issue.severity] += 1
                print(str(issue))

    # ── 요약 ──
    print(f"\n{'=' * 60}")
    print(f"  📊 검사 요약")
    print(f"{'=' * 60}")
    print(f"  파일 수: {len(all_results)}")
    print(f"  ❌ 에러:  {total_issues['ERROR']}")
    print(f"  ⚠️  경고:  {total_issues['WARNING']}")
    print(f"  💡 정보:  {total_issues['INFO']}")
    print()

    if total_issues["ERROR"] > 0:
        print("  ❌ AX 검사 실패 — 에러를 수정해주세요!")
        return 1
    elif total_issues["WARNING"] > 0:
        print("  ⚠️  AX 검사 통과 (경고 있음)")
        return 0
    else:
        print("  ✅ AX 검사 통과!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
