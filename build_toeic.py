import json

with open(r"C:\Users\chan7\toeic words\toeic_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

words_json = json.dumps(words, ensure_ascii=False)

html_part1 = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TOEIC 영단어장</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-primary: #0c0f1a;
    --bg-card: #151929;
    --bg-elevated: #1c2137;
    --bg-input: #1a1f35;
    --border: #2a3050;
    --border-hover: #4a5580;
    --text-primary: #eef0f6;
    --text-secondary: #8b92ab;
    --text-dim: #5a6178;
    --accent: #6c8cff;
    --accent-hover: #5570e0;
    --accent-glow: rgba(108,140,255,0.15);
    --accent-soft: rgba(108,140,255,0.08);
    --green: #4ade80;
    --green-bg: rgba(74,222,128,0.08);
    --green-border: rgba(74,222,128,0.3);
    --red: #f87171;
    --red-bg: rgba(248,113,113,0.08);
    --red-border: rgba(248,113,113,0.3);
    --amber: #fbbf24;
    --amber-bg: rgba(251,191,36,0.08);
    --amber-border: rgba(251,191,36,0.3);
    --purple: #c4b5fd;
    --radius: 12px;
    --radius-sm: 8px;
    --radius-full: 100px;
    --shadow: 0 4px 24px rgba(0,0,0,0.25);
    --shadow-sm: 0 2px 8px rgba(0,0,0,0.2);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Inter', 'Noto Sans KR', -apple-system, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    min-height: 100vh;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }

  /* ===== HEADER ===== */
  .header {
    background: linear-gradient(180deg, #141830, var(--bg-primary));
    padding: 24px 32px;
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 16px;
    border-bottom: 1px solid var(--border);
  }
  .header h1 {
    font-size: 1.4rem; font-weight: 700; color: var(--text-primary);
    letter-spacing: -0.3px;
  }
  .header h1 span { color: var(--accent); }
  .header-stats { display: flex; gap: 12px; font-size: 0.82rem; }
  .header-stats .stat {
    background: var(--bg-card); padding: 7px 16px;
    border-radius: var(--radius-full); border: 1px solid var(--border);
    color: var(--text-secondary);
  }
  .stat-value { color: var(--accent); font-weight: 600; }

  /* ===== NAV ===== */
  .nav {
    background: var(--bg-card); padding: 10px 32px;
    display: flex; gap: 6px; flex-wrap: wrap; align-items: center;
    border-bottom: 1px solid var(--border);
  }
  .nav button {
    padding: 7px 18px; border: 1px solid transparent;
    background: transparent; color: var(--text-secondary); border-radius: var(--radius-full);
    cursor: pointer; font-size: 0.85rem; font-weight: 500; transition: all 0.2s;
  }
  .nav button:hover { background: var(--accent-soft); color: var(--text-primary); }
  .nav button.active {
    background: var(--accent); color: white; border-color: var(--accent);
    box-shadow: 0 2px 12px rgba(108,140,255,0.3);
  }
  .nav select {
    padding: 7px 14px; border: 1px solid var(--border);
    background: var(--bg-elevated); color: var(--text-secondary);
    border-radius: var(--radius-sm); font-size: 0.82rem; font-family: inherit;
  }
  .nav .divider {
    width: 1px; height: 20px; background: var(--border); margin: 0 6px;
  }

  /* ===== CONTAINER ===== */
  .container { max-width: 1200px; margin: 0 auto; padding: 24px; }

  /* ===== WORD CARDS ===== */
  .word-list-view {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 10px;
  }
  .word-card {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 16px 20px; display: flex; align-items: baseline; gap: 14px;
    transition: all 0.2s; cursor: pointer; user-select: none; position: relative;
  }
  .word-card:hover {
    border-color: var(--border-hover); background: var(--bg-elevated);
    box-shadow: var(--shadow-sm);
  }
  .word-card .num {
    color: var(--text-dim); font-size: 0.75rem; min-width: 28px;
    font-weight: 500; font-variant-numeric: tabular-nums;
  }
  .word-card .eng {
    color: var(--accent); font-weight: 600; font-size: 1.05rem; min-width: 120px;
  }
  .word-card .kor { color: var(--text-secondary); font-size: 0.88rem; line-height: 1.5; }
  .word-card .ipa-text { color: var(--text-dim); font-size: 0.78rem; font-style: italic; min-width: 0; font-family: 'Noto Sans', 'Lucida Sans Unicode', 'Arial Unicode MS', sans-serif; }
  .speak-btn {
    background: var(--accent-soft); border: 1px solid var(--border); color: var(--accent);
    width: 28px; height: 28px; border-radius: 50%; cursor: pointer; font-size: 0.7rem;
    display: inline-flex; align-items: center; justify-content: center;
    transition: all 0.2s; flex-shrink: 0; padding: 0;
  }
  .speak-btn:hover { background: var(--accent); color: white; }
  .word-card .card-badge {
    font-size: 0.65rem; font-weight: 600; padding: 3px 10px; border-radius: var(--radius-full);
    position: absolute; top: 10px; right: 12px; letter-spacing: 0.3px;
  }
  .word-card.status-learned {
    border-color: var(--green-border); background: var(--green-bg);
  }
  .word-card.status-learned .card-badge { background: var(--green); color: #052e16; }
  .word-card.status-confused {
    border-color: var(--amber-border); background: var(--amber-bg);
  }
  .word-card.status-confused .card-badge { background: var(--amber); color: #451a03; }

  /* ===== CATEGORY FILTERS ===== */
  .category-filters {
    display: flex; gap: 8px; margin-bottom: 18px; flex-wrap: wrap; align-items: center;
  }
  .category-filters button {
    padding: 6px 16px; border: 1px solid var(--border); background: var(--bg-card);
    color: var(--text-secondary); border-radius: var(--radius-full); cursor: pointer;
    font-size: 0.8rem; font-weight: 500; transition: all 0.2s; font-family: inherit;
  }
  .category-filters button:hover { border-color: var(--accent); color: var(--text-primary); }
  .category-filters button.active {
    background: var(--accent); color: white; border-color: var(--accent);
  }
  .category-filters .filter-count { font-size: 0.72rem; color: var(--text-dim); margin-left: 3px; }

  /* ===== TYPING / LEARNING ===== */
  .typing-view { display: none; }
  .typing-view.active { display: block; }
  .word-list-view.active { display: grid; }
  .typing-area { max-width: 700px; margin: 40px auto; text-align: center; }
  .typing-progress {
    margin-bottom: 36px; display: flex;
    justify-content: space-between; align-items: center;
  }
  .progress-bar-bg {
    flex: 1; height: 6px; background: var(--bg-elevated);
    border-radius: 3px; margin: 0 16px; overflow: hidden;
  }
  .progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), #a78bfa);
    border-radius: 3px; transition: width 0.4s ease;
  }
  .progress-text { color: var(--text-dim); font-size: 0.82rem; min-width: 55px; font-weight: 500; }
  .word-display { margin-bottom: 12px; }
  .word-display .meaning-text {
    font-size: 1.15rem; color: var(--text-secondary); margin-bottom: 16px; min-height: 28px;
  }
  .word-display .english-word {
    font-size: 3.2rem; font-weight: 700; color: var(--accent);
    margin-bottom: 8px; letter-spacing: 3px; min-height: 60px;
  }
  .word-display .repeat-count {
    font-size: 0.85rem; color: var(--text-dim); margin-bottom: 28px; font-weight: 500;
  }
  .typing-input-area { position: relative; margin-bottom: 20px; }
  .typing-input {
    width: 100%; max-width: 460px; padding: 16px 24px;
    font-size: 1.5rem; text-align: center; background: var(--bg-input);
    border: 2px solid var(--border); border-radius: var(--radius);
    color: var(--text-primary); outline: none; letter-spacing: 3px;
    transition: all 0.25s; font-family: 'Inter', monospace;
  }
  .typing-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow); }
  .typing-input.correct { border-color: var(--green); background: var(--green-bg); }
  .typing-input.wrong { border-color: var(--red); background: var(--red-bg); }
  .char-preview {
    display: flex; justify-content: center; gap: 5px;
    margin-bottom: 24px; min-height: 50px; flex-wrap: wrap;
  }
  .char-box {
    width: 38px; height: 46px; display: flex; align-items: center;
    justify-content: center; font-size: 1.25rem; font-weight: 600;
    border-radius: var(--radius-sm); border: 2px solid var(--border);
    background: var(--bg-card); color: var(--text-dim); transition: all 0.15s;
    font-family: 'Inter', monospace;
  }
  .char-box.filled { color: var(--text-primary); border-color: var(--border-hover); }
  .char-box.correct { color: var(--green); border-color: var(--green-border); background: var(--green-bg); }
  .char-box.wrong { color: var(--red); border-color: var(--red-border); background: var(--red-bg); }
  .char-box.current { border-color: var(--accent); box-shadow: 0 0 12px var(--accent-glow); }
  .typing-feedback { font-size: 1.05rem; min-height: 28px; margin-bottom: 12px; font-weight: 500; }
  .feedback-correct { color: var(--green); }
  .feedback-wrong { color: var(--red); }
  .feedback-info { color: var(--accent); }

  /* ===== BUTTONS ===== */
  .typing-controls {
    display: flex; gap: 10px; justify-content: center; margin-top: 24px;
  }
  .typing-controls button {
    padding: 10px 26px; border: 1px solid var(--border); background: var(--bg-elevated);
    color: var(--text-secondary); border-radius: var(--radius-sm); cursor: pointer;
    font-size: 0.88rem; font-weight: 500; transition: all 0.2s; font-family: inherit;
  }
  .typing-controls button:hover { background: var(--accent); color: white; border-color: var(--accent); }
  .btn-primary {
    background: var(--accent) !important; color: white !important;
    border-color: var(--accent) !important;
    box-shadow: 0 2px 12px rgba(108,140,255,0.25);
  }
  .btn-primary:hover { background: var(--accent-hover) !important; }

  /* ===== SETTINGS ===== */
  .settings-panel {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 24px; margin-bottom: 20px;
    display: none; box-shadow: var(--shadow-sm);
  }
  .settings-panel.active { display: block; }
  .settings-row {
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 14px; flex-wrap: wrap;
  }
  .settings-row label {
    color: var(--text-secondary); min-width: 120px; font-size: 0.88rem; font-weight: 500;
  }
  .settings-row input, .settings-row select {
    padding: 8px 14px; background: var(--bg-input); border: 1px solid var(--border);
    color: var(--text-primary); border-radius: var(--radius-sm); font-size: 0.88rem;
    font-family: inherit; transition: border-color 0.2s;
  }
  .settings-row input:focus, .settings-row select:focus {
    border-color: var(--accent); outline: none;
  }

  /* ===== COMPLETE / RESULTS ===== */
  .complete-screen {
    text-align: center; padding: 60px 20px; display: none;
  }
  .complete-screen.active { display: block; }
  .complete-screen h2 { font-size: 1.8rem; color: var(--green); margin-bottom: 20px; font-weight: 700; }
  .complete-stats {
    display: flex; gap: 16px; justify-content: center; margin: 30px 0; flex-wrap: wrap;
  }
  .complete-stat {
    background: var(--bg-card); padding: 24px 32px; border-radius: var(--radius);
    border: 1px solid var(--border); min-width: 150px;
  }
  .complete-stat .label {
    color: var(--text-dim); font-size: 0.8rem; margin-bottom: 10px;
    text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;
  }
  .complete-stat .value { color: var(--accent); font-size: 2rem; font-weight: 700; }

  /* ===== SEARCH ===== */
  .search-box {
    padding: 8px 16px; background: var(--bg-input); border: 1px solid var(--border);
    color: var(--text-primary); border-radius: var(--radius-full); font-size: 0.85rem;
    width: 200px; font-family: inherit; transition: all 0.2s;
  }
  .search-box:focus { border-color: var(--accent); outline: none; box-shadow: 0 0 0 3px var(--accent-glow); }
  .search-box::placeholder { color: var(--text-dim); }

  /* ===== PAGINATION ===== */
  .pagination {
    display: flex; justify-content: center; align-items: center;
    gap: 6px; margin: 24px 0; flex-wrap: wrap;
  }
  .pagination button {
    padding: 7px 14px; border: 1px solid var(--border); background: var(--bg-card);
    color: var(--text-secondary); border-radius: var(--radius-sm); cursor: pointer;
    font-size: 0.82rem; transition: all 0.2s; min-width: 38px; font-family: inherit;
    font-weight: 500;
  }
  .pagination button:hover { background: var(--accent-soft); border-color: var(--accent); color: var(--text-primary); }
  .pagination button.active { background: var(--accent); color: white; border-color: var(--accent); }
  .pagination button:disabled { opacity: 0.3; cursor: default; }
  .pagination button:disabled:hover { background: var(--bg-card); border-color: var(--border); color: var(--text-secondary); }
  .pagination .page-info { color: var(--text-dim); font-size: 0.82rem; margin: 0 8px; font-weight: 500; }

  /* ===== TEST MODE ===== */
  .test-view { display: none; }
  .test-setup { max-width: 520px; margin: 48px auto; text-align: center; }
  .test-setup h2 {
    color: var(--text-primary); font-size: 1.6rem; margin-bottom: 36px;
    font-weight: 700; letter-spacing: -0.3px;
  }
  .test-type-buttons {
    display: flex; gap: 16px; justify-content: center; margin-bottom: 32px; flex-wrap: wrap;
  }
  .test-type-btn {
    flex: 1; min-width: 210px; padding: 28px 20px;
    background: var(--bg-card); border: 2px solid var(--border); border-radius: var(--radius);
    color: var(--text-primary); cursor: pointer; transition: all 0.25s; text-align: center;
  }
  .test-type-btn:hover {
    border-color: var(--accent); transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(108,140,255,0.12);
  }
  .test-type-btn.selected {
    border-color: var(--accent); background: var(--accent-soft);
    box-shadow: 0 0 0 3px var(--accent-glow);
  }
  .test-type-btn .icon {
    font-size: 1.6rem; margin-bottom: 12px; font-weight: 700; color: var(--accent);
  }
  .test-type-btn .title { font-size: 1.05rem; font-weight: 600; margin-bottom: 8px; }
  .test-type-btn .desc { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.4; }
  .test-settings { margin: 24px 0; }
  .test-settings .settings-row { justify-content: center; }
  .test-start-btn {
    padding: 14px 48px; background: var(--accent); color: white; border: none;
    border-radius: var(--radius-sm); font-size: 1.05rem; font-weight: 600;
    cursor: pointer; transition: all 0.2s; margin-top: 12px; font-family: inherit;
    box-shadow: 0 4px 16px rgba(108,140,255,0.3);
  }
  .test-start-btn:hover { background: var(--accent-hover); transform: translateY(-1px); }
  .test-start-btn:disabled { opacity: 0.35; cursor: default; transform: none; box-shadow: none; }

  .test-area { max-width: 700px; margin: 40px auto; text-align: center; display: none; }
  .test-question-label {
    font-size: 0.88rem; color: var(--text-dim); margin-bottom: 12px;
    font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;
  }
  .test-question {
    font-size: 2rem; font-weight: 700; color: var(--purple);
    margin-bottom: 8px; min-height: 50px; line-height: 1.4;
  }
  .test-question-sub { font-size: 0.85rem; color: var(--text-dim); margin-bottom: 28px; }
  .test-input {
    width: 100%; max-width: 460px; padding: 14px 24px;
    font-size: 1.3rem; text-align: center; background: var(--bg-input);
    border: 2px solid var(--border); border-radius: var(--radius);
    color: var(--text-primary); outline: none; transition: all 0.25s;
    font-family: 'Inter', monospace; letter-spacing: 1px;
  }
  .test-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow); }
  .test-input.correct { border-color: var(--green); background: var(--green-bg); }
  .test-input.wrong { border-color: var(--red); background: var(--red-bg); }
  .test-answer-reveal { margin-top: 18px; font-size: 1rem; min-height: 24px; }
  .test-answer-reveal .answer-word { color: var(--accent); font-weight: 700; font-size: 1.15rem; }
  .test-answer-reveal .answer-meaning { color: var(--text-secondary); }
  .test-nav-btn {
    padding: 10px 32px; background: var(--accent); color: white; border: none;
    border-radius: var(--radius-sm); font-size: 0.92rem; font-weight: 500;
    cursor: pointer; margin-top: 20px; transition: all 0.2s; font-family: inherit;
  }
  .test-nav-btn:hover { background: var(--accent-hover); }

  /* Test result */
  .test-result { display: none; max-width: 700px; margin: 40px auto; text-align: center; }
  .test-result h2 { font-size: 1.8rem; margin-bottom: 10px; font-weight: 700; }
  .test-result .score-circle {
    width: 150px; height: 150px; border-radius: 50%; margin: 28px auto;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    border: 4px solid var(--accent); background: var(--bg-card);
    box-shadow: 0 0 30px var(--accent-glow);
  }
  .score-circle .score-num { font-size: 2.8rem; font-weight: 700; color: var(--accent); }
  .score-circle .score-label { font-size: 0.8rem; color: var(--text-dim); font-weight: 500; }
  .test-result-list {
    text-align: left; margin: 24px 0; max-height: 400px; overflow-y: auto;
  }
  .test-result-list::-webkit-scrollbar { width: 6px; }
  .test-result-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
  .result-item {
    display: flex; align-items: center; gap: 14px; padding: 12px 18px;
    background: var(--bg-card); border-radius: var(--radius-sm); margin-bottom: 6px;
    border-left: 4px solid var(--green);
  }
  .result-item.wrong-item { border-left-color: var(--red); }
  .result-item .ri-status { font-size: 1.2rem; min-width: 24px; }
  .result-item .ri-word { color: var(--accent); font-weight: 600; min-width: 120px; }
  .result-item .ri-meaning { color: var(--text-secondary); font-size: 0.88rem; flex: 1; }
  .result-item .ri-typed { color: var(--red); font-size: 0.82rem; font-weight: 500; }

  /* ===== CHOICES (Multiple Choice) ===== */
  .choices-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
    max-width: 520px; margin: 0 auto;
  }
  .choice-btn {
    padding: 18px 16px; background: var(--bg-card); border: 2px solid var(--border);
    border-radius: var(--radius); color: var(--text-primary); cursor: pointer;
    font-size: 0.92rem; text-align: left; transition: all 0.2s;
    line-height: 1.5; font-family: inherit;
  }
  .choice-btn:hover { border-color: var(--accent); background: var(--accent-soft); }
  .choice-btn.choice-correct { border-color: var(--green); background: var(--green-bg); }
  .choice-btn.choice-wrong { border-color: var(--red); background: var(--red-bg); }
  .choice-btn.choice-dim { opacity: 0.4; cursor: default; }
  .choice-btn .choice-num {
    color: var(--text-dim); font-size: 0.75rem; margin-right: 8px;
    font-weight: 600;
  }

  /* ===== LIGHT MODE ===== */
  body.light {
    --bg-primary: #f5f6fa;
    --bg-card: #ffffff;
    --bg-elevated: #f0f1f5;
    --bg-input: #ffffff;
    --border: #dfe2ea;
    --border-hover: #b8bdd0;
    --text-primary: #1a1d2e;
    --text-secondary: #5a5f73;
    --text-dim: #8b90a3;
    --accent: #4f6df5;
    --accent-hover: #3d5ae0;
    --accent-glow: rgba(79,109,245,0.12);
    --accent-soft: rgba(79,109,245,0.06);
    --green: #16a34a;
    --green-bg: rgba(22,163,74,0.06);
    --green-border: rgba(22,163,74,0.25);
    --red: #dc2626;
    --red-bg: rgba(220,38,38,0.06);
    --red-border: rgba(220,38,38,0.25);
    --amber: #d97706;
    --amber-bg: rgba(217,119,6,0.06);
    --amber-border: rgba(217,119,6,0.25);
    --purple: #7c3aed;
    --shadow: 0 4px 24px rgba(0,0,0,0.08);
    --shadow-sm: 0 2px 8px rgba(0,0,0,0.05);
  }
  body.light .header { background: linear-gradient(180deg, #eef0f8, var(--bg-primary)); }
  body.light .word-card.status-learned .card-badge { color: white; }
  body.light .word-card.status-confused .card-badge { color: white; }

  /* ===== DICTIONARY PANEL ===== */
  .dict-overlay {
    display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.6); z-index: 999;
    justify-content: center; align-items: center;
    backdrop-filter: blur(4px);
  }
  .dict-overlay.active { display: flex; }
  .dict-panel {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 28px; width: 90%; max-width: 560px;
    max-height: 80vh; overflow-y: auto; box-shadow: var(--shadow);
  }
  .dict-panel::-webkit-scrollbar { width: 6px; }
  .dict-panel::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
  .dict-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
  .dict-header h3 { font-size: 1.4rem; font-weight: 700; color: var(--accent); }
  .dict-close {
    background: var(--bg-elevated); border: 1px solid var(--border); color: var(--text-secondary);
    width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-size: 1.1rem;
    display: flex; align-items: center; justify-content: center;
  }
  .dict-phonetic { color: var(--text-dim); font-size: 0.88rem; margin-bottom: 16px; font-style: italic; }
  .dict-pos { color: var(--accent); font-weight: 600; font-size: 0.9rem; margin-top: 14px; margin-bottom: 6px; font-style: italic; }
  .dict-def { color: var(--text-primary); font-size: 0.9rem; margin-bottom: 4px; padding-left: 12px; border-left: 2px solid var(--border); line-height: 1.6; }
  .dict-example { color: var(--text-dim); font-size: 0.82rem; font-style: italic; margin: 4px 0 8px 12px; }
  .dict-loading { text-align: center; color: var(--text-dim); padding: 30px; }
  .dict-error { text-align: center; color: var(--red); padding: 20px; }
  .dict-src { color: var(--text-dim); font-size: 0.72rem; margin-top: 16px; text-align: right; }

  /* ===== ADD WORD MODAL ===== */
  .modal-overlay {
    display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.6); z-index: 1000;
    justify-content: center; align-items: center;
    backdrop-filter: blur(4px);
  }
  .modal-overlay.active { display: flex; }
  .modal {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 28px; width: 90%; max-width: 460px;
    box-shadow: var(--shadow);
  }
  .modal h3 { font-size: 1.2rem; font-weight: 700; margin-bottom: 20px; color: var(--text-primary); }
  .modal-field { margin-bottom: 14px; }
  .modal-field label { display: block; color: var(--text-secondary); font-size: 0.85rem; font-weight: 500; margin-bottom: 6px; }
  .modal-field input {
    width: 100%; padding: 10px 14px; background: var(--bg-input); border: 1px solid var(--border);
    border-radius: var(--radius-sm); color: var(--text-primary); font-size: 0.95rem; font-family: inherit;
  }
  .modal-field input:focus { border-color: var(--accent); outline: none; }
  .modal-btns { display: flex; gap: 10px; margin-top: 20px; }
  .modal-btns button {
    flex: 1; padding: 10px; border-radius: var(--radius-sm); font-size: 0.9rem;
    font-weight: 500; cursor: pointer; font-family: inherit; border: 1px solid var(--border);
  }
  .modal-btns .m-save { background: var(--accent); color: white; border-color: var(--accent); }
  .modal-btns .m-cancel { background: var(--bg-elevated); color: var(--text-secondary); }
  .modal-msg { font-size: 0.85rem; margin-top: 10px; min-height: 20px; }

  /* ===== RESPONSIVE ===== */
  @media (max-width: 768px) {
    .header { padding: 18px 16px; }
    .header h1 { font-size: 1.15rem; }
    .nav { padding: 10px 16px; }
    .container { padding: 16px; }
    .word-display .english-word { font-size: 2.2rem; }
    .typing-input { font-size: 1.2rem; max-width: 100%; }
    .char-box { width: 30px; height: 38px; font-size: 1rem; }
    .word-list-view { grid-template-columns: 1fr; }
    .choices-grid { grid-template-columns: 1fr; }
    .header-stats { gap: 8px; }
    .header-stats .stat { padding: 5px 10px; font-size: 0.75rem; }
  }
</style>
</head>
<body>
<div class="header">
  <div style="display:flex; align-items:center; gap:12px;">
    <h1><span>TOEIC</span> 영단어장</h1>
    <button onclick="toggleTheme()" id="themeBtn" style="background:var(--bg-elevated); border:1px solid var(--border); color:var(--text-secondary); padding:6px 12px; border-radius:var(--radius-full); cursor:pointer; font-size:0.8rem; font-family:inherit; transition:all 0.2s;">Dark</button>
  </div>
  <div class="header-stats">
    <div class="stat">전체 <span class="stat-value" id="totalWords">0</span>개</div>
    <div class="stat">학습완료 <span class="stat-value" id="learnedCount">0</span>개</div>
    <div class="stat">진행도 <span class="stat-value" id="progressPct">0</span>%</div>
    <div class="stat">정확도 <span class="stat-value" id="accuracy">0</span>%</div>
  </div>
</div>
<div class="nav">
  <button id="btnList" class="active" onclick="switchMode('list')">단어 목록</button>
  <button id="btnTyping" onclick="switchMode('typing')">단어 학습</button>
  <button id="btnTest" onclick="switchMode('test')">테스트</button>
  <button id="btnSettings" onclick="toggleSettings()">설정</button>
  <button onclick="openAddWord()">단어 추가</button>
  <select id="rangeSelect" onchange="changeRange()">
    <option value="all">전체 (1-2035)</option>
  </select>
  <input type="text" class="search-box" id="searchBox" placeholder="단어 검색..." oninput="searchWords()">
</div>
<div class="container">
  <div class="settings-panel" id="settingsPanel">
    <div class="settings-row">
      <label>반복 횟수:</label>
      <input type="number" id="repeatCount" value="3" min="1" max="20" style="width:70px">
      <span style="color:#64748b; font-size:0.85rem">각 단어를 몇 번 타이핑할지</span>
    </div>
    <div class="settings-row">
      <label>학습 순서:</label>
      <select id="orderSelect">
        <option value="sequential">순서대로</option>
        <option value="random">랜덤</option>
      </select>
    </div>
    <div class="settings-row">
      <label>뜻 표시:</label>
      <select id="meaningDisplay">
        <option value="always">항상 표시</option>
        <option value="before">타이핑 전에만</option>
        <option value="hidden">숨기기 (영단어만)</option>
      </select>
    </div>
    <div class="settings-row">
      <label>자동 넘김:</label>
      <select id="autoNext">
        <option value="yes">정답 시 자동 넘김</option>
        <option value="no">Enter로 넘기기</option>
      </select>
    </div>
    <div class="settings-row">
      <label>학습 카테고리:</label>
      <select id="typingCategorySelect" onchange="updateTypingCategoryInfo()">
        <option value="all">전체</option>
        <option value="none">미학습 단어</option>
        <option value="learned">학습 완료 단어</option>
        <option value="confused">헷갈리는 단어</option>
      </select>
      <span style="color:#94a3b8; font-size:0.85rem;" id="typingCategoryInfo"></span>
    </div>
    <div style="text-align:right; margin-top:16px;">
      <button class="btn-primary" style="padding:8px 24px; border:none; border-radius:8px; font-size:0.9rem; cursor:pointer;" onclick="applySettings()">적용</button>
      <button style="padding:8px 24px; border:1px solid #475569; background:#334155; color:#cbd5e1; border-radius:8px; font-size:0.9rem; cursor:pointer; margin-left:8px;" onclick="cancelSettings()">취소</button>
    </div>
  </div>
  <div class="category-filters" id="categoryFilters">
    <button class="active" onclick="filterCategory('all',event)">전체</button>
    <button onclick="filterCategory('none',event)">미학습 <span class="filter-count" id="countNone"></span></button>
    <button onclick="filterCategory('learned',event)">학습 완료 <span class="filter-count" id="countLearned"></span></button>
    <button onclick="filterCategory('confused',event)">헷갈리는 단어 <span class="filter-count" id="countConfused"></span></button>
    <span style="color:#64748b; font-size:0.75rem; margin-left:8px;">클릭 1회=학습완료 / 2회=헷갈림 / 3회=초기화</span>
  </div>
  <div class="word-list-view active" id="wordListView"></div>
  <div class="pagination" id="pagination"></div>
  <div class="typing-view" id="typingView">
    <div class="typing-area">
      <div class="typing-progress">
        <span class="progress-text" id="progressLeft">0 / 0</span>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" id="progressBar" style="width:0%"></div>
        </div>
        <span class="progress-text" id="progressRight">0%</span>
      </div>
      <div class="word-display">
        <div class="meaning-text" id="meaningText"></div>
        <div class="english-word" id="englishWord"></div>
        <div class="repeat-count" id="repeatInfo"></div>
      </div>
      <div class="char-preview" id="charPreview"></div>
      <div class="typing-input-area">
        <input type="text" class="typing-input" id="typingInput" placeholder="여기에 타이핑하세요" autocomplete="off" spellcheck="false">
      </div>
      <div class="typing-feedback" id="feedback"></div>
      <div class="typing-controls">
        <button onclick="skipWord()">건너뛰기</button>
        <button onclick="resetTyping()" class="btn-primary">다시 시작</button>
      </div>
    </div>
  </div>
  <!-- Test Mode -->
  <div class="test-view" id="testView">
    <div class="test-setup" id="testSetup">
      <h2>단어 테스트</h2>
      <div class="test-type-buttons">
        <div class="test-type-btn" id="testTypeKorToEng" onclick="selectTestType('kor-to-eng')">
          <div class="icon">KR &rarr; EN</div>
          <div class="title">한국어 &rarr; 영어</div>
          <div class="desc">한국어 뜻을 보고 영단어를 입력</div>
        </div>
        <div class="test-type-btn" id="testTypeEngToKor" onclick="selectTestType('eng-to-kor')">
          <div class="icon">EN &rarr; KR</div>
          <div class="title">영어 &rarr; 한국어</div>
          <div class="desc">영단어를 보고 한국어 뜻을 입력</div>
        </div>
      </div>
      <div class="test-settings">
        <div class="settings-row">
          <label>문제 수:</label>
          <select id="testQuestionCount">
            <option value="10">10문제</option>
            <option value="20" selected>20문제</option>
            <option value="30">30문제</option>
            <option value="50">50문제</option>
            <option value="all">전체</option>
          </select>
        </div>
        <div class="settings-row">
          <label>출제 카테고리:</label>
          <select id="testCategorySelect">
            <option value="all">전체</option>
            <option value="none">미학습 단어</option>
            <option value="learned">학습 완료 단어</option>
            <option value="confused">헷갈리는 단어</option>
          </select>
          <span style="color:#94a3b8; font-size:0.85rem;" id="testCategoryCount"></span>
        </div>
        <div class="settings-row">
          <label>출제 범위:</label>
          <span style="color:#94a3b8; font-size:0.85rem;" id="testRangeInfo">현재 선택된 범위에서 출제</span>
        </div>
      </div>
      <button class="test-start-btn" id="testStartBtn" onclick="startTest()" disabled>테스트 시작</button>
    </div>

    <div class="test-area" id="testArea">
      <div class="typing-progress">
        <span class="progress-text" id="testProgressLeft">0 / 0</span>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" id="testProgressBar" style="width:0%"></div>
        </div>
        <span class="progress-text" id="testProgressRight">0%</span>
      </div>
      <div class="test-question-label" id="testQuestionLabel"></div>
      <div class="test-question" id="testQuestion"></div>
      <div class="test-question-sub" id="testQuestionSub"></div>
      <div id="testTypingArea">
        <input type="text" class="test-input" id="testInput" placeholder="정답을 입력하세요" autocomplete="off" spellcheck="false">
      </div>
      <div id="testChoicesArea" style="display:none;"></div>
      <div class="test-answer-reveal" id="testAnswerReveal"></div>
      <div style="margin-top:15px;">
        <button class="test-nav-btn" id="testSubmitBtn" onclick="submitTestAnswer()">확인 (Enter)</button>
        <button class="test-nav-btn" id="testNextBtn" onclick="nextTestQuestion()" style="display:none;">다음 문제 (Enter)</button>
      </div>
    </div>

    <div class="test-result" id="testResult">
      <h2 id="testResultTitle">테스트 결과</h2>
      <div class="score-circle">
        <div class="score-num" id="testScoreNum">0</div>
        <div class="score-label" id="testScoreLabel">/ 0</div>
      </div>
      <div class="complete-stats">
        <div class="complete-stat">
          <div class="label">정답률</div>
          <div class="value" id="testResultAccuracy">0%</div>
        </div>
        <div class="complete-stat">
          <div class="label">소요 시간</div>
          <div class="value" id="testResultTime">0:00</div>
        </div>
      </div>
      <div style="margin:20px 0; text-align:left;">
        <h3 style="color:#94a3b8; margin-bottom:10px; text-align:center;">오답 목록</h3>
        <div class="test-result-list" id="testResultList"></div>
      </div>
      <div class="typing-controls">
        <button onclick="retestWrong()" id="retestWrongBtn" class="btn-primary">오답만 다시 테스트</button>
        <button onclick="switchMode('test')">다시 테스트하기</button>
        <button onclick="switchMode('list')">단어 목록으로</button>
      </div>
    </div>
  </div>

  <div class="complete-screen" id="completeScreen">
    <h2>학습 완료!</h2>
    <div class="complete-stats">
      <div class="complete-stat">
        <div class="label">학습한 단어</div>
        <div class="value" id="completedWords">0</div>
      </div>
      <div class="complete-stat">
        <div class="label">정확도</div>
        <div class="value" id="completedAccuracy">0%</div>
      </div>
      <div class="complete-stat">
        <div class="label">소요 시간</div>
        <div class="value" id="completedTime">0:00</div>
      </div>
    </div>
    <div class="typing-controls">
      <button onclick="resetTyping()" class="btn-primary">다시 학습하기</button>
      <button onclick="switchMode('list')">단어 목록으로</button>
    </div>
  </div>
</div>
<div class="dict-overlay" id="dictOverlay" onclick="if(event.target===this)closeDict()">
  <div class="dict-panel">
    <div class="dict-header">
      <h3 id="dictWord"></h3>
      <button class="dict-close" onclick="closeDict()">&times;</button>
    </div>
    <div id="dictContent"><div class="dict-loading">불러오는 중...</div></div>
  </div>
</div>
<div class="modal-overlay" id="addWordModal">
  <div class="modal">
    <h3>단어 추가</h3>
    <div class="modal-field">
      <label>영단어</label>
      <input type="text" id="addWordEng" placeholder="예: accomplish" autocomplete="off">
    </div>
    <div class="modal-field">
      <label>한국어 뜻</label>
      <input type="text" id="addWordKor" placeholder="예: (동)성취하다, 달성하다" autocomplete="off">
    </div>
    <div class="modal-btns">
      <button class="m-cancel" onclick="closeAddWord()">취소</button>
      <button class="m-save" onclick="saveAddWord()">추가</button>
    </div>
    <div class="modal-msg" id="addWordMsg"></div>
  </div>
</div>
<script>
"""

html_part2 = """
let currentMode = 'list';
let currentRange = [0, ALL_WORDS.length];
let filteredWords = [...ALL_WORDS];
let currentPage = 1;
const PAGE_SIZE = 50;
let currentCategoryFilter = 'all';

// Word status: 'none' (default), 'learned', 'confused'
var wordStatus = {};
try {
  var saved = localStorage.getItem('toeic_word_status');
  if (saved) wordStatus = JSON.parse(saved);
} catch(e) {}

function saveWordStatus() {
  try { localStorage.setItem('toeic_word_status', JSON.stringify(wordStatus)); } catch(e) {}
  updateHeaderStats();
}

function updateHeaderStats() {
  var total = ALL_WORDS.length;
  var learned = 0;
  var confused = 0;
  for (var i = 0; i < ALL_WORDS.length; i++) {
    var s = getWordStatus(ALL_WORDS[i].word);
    if (s === 'learned') learned++;
    else if (s === 'confused') confused++;
  }
  document.getElementById('totalWords').textContent = total;
  document.getElementById('learnedCount').textContent = learned;
  var progress = total > 0 ? Math.round((learned / total) * 100) : 0;
  document.getElementById('progressPct').textContent = progress;
  var touched = learned + confused;
  var acc = touched > 0 ? Math.round((learned / touched) * 100) : 0;
  document.getElementById('accuracy').textContent = acc;
}

function getWordStatus(word) {
  return wordStatus[word] || 'none';
}

function cycleWordStatus(word) {
  var current = getWordStatus(word);
  if (current === 'none') wordStatus[word] = 'learned';
  else if (current === 'learned') wordStatus[word] = 'confused';
  else { delete wordStatus[word]; }
  saveWordStatus();
}

function filterCategory(cat, e) {
  currentCategoryFilter = cat;
  currentPage = 1;
  var btns = document.getElementById('categoryFilters').querySelectorAll('button');
  for (var i = 0; i < btns.length; i++) btns[i].classList.remove('active');
  if (e && e.target) e.target.closest('button').classList.add('active');
  renderWordList();
}

function updateCategoryCounts() {
  var words = filteredWords;
  var search = document.getElementById('searchBox').value.toLowerCase();
  if (search) {
    words = ALL_WORDS.filter(function(w) {
      return w.word.toLowerCase().includes(search) || w.meaning.includes(search);
    });
  }
  var cNone = 0, cLearned = 0, cConfused = 0;
  for (var i = 0; i < words.length; i++) {
    var s = getWordStatus(words[i].word);
    if (s === 'learned') cLearned++;
    else if (s === 'confused') cConfused++;
    else cNone++;
  }
  document.getElementById('countNone').textContent = '(' + cNone + ')';
  document.getElementById('countLearned').textContent = '(' + cLearned + ')';
  document.getElementById('countConfused').textContent = '(' + cConfused + ')';
}
let typingWords = [];
let typingIndex = 0;
let currentRepeat = 0;
let totalAttempts = 0;
let correctAttempts = 0;
let startTime = null;

function initRanges() {
  const sel = document.getElementById('rangeSelect');
  const step = 50;
  for (let i = 0; i < ALL_WORDS.length; i += step) {
    const end = Math.min(i + step, ALL_WORDS.length);
    const opt = document.createElement('option');
    opt.value = i + '-' + end;
    opt.textContent = (i + 1) + ' - ' + end + '번';
    sel.appendChild(opt);
  }
}

function changeRange() {
  const val = document.getElementById('rangeSelect').value;
  if (val === 'all') {
    currentRange = [0, ALL_WORDS.length];
  } else {
    const [s, e] = val.split('-').map(Number);
    currentRange = [s, e];
  }
  filteredWords = ALL_WORDS.slice(currentRange[0], currentRange[1]);
  currentPage = 1;
  renderWordList();
  if (currentMode === 'typing') resetTyping();
}

function getDisplayWords() {
  const search = document.getElementById('searchBox').value.toLowerCase();
  if (search) {
    return ALL_WORDS.filter(w =>
      w.word.toLowerCase().includes(search) || w.meaning.includes(search)
    );
  }
  return filteredWords;
}

function renderWordList() {
  const container = document.getElementById('wordListView');
  var allDisplayWords = getDisplayWords();

  // Apply category filter
  if (currentCategoryFilter !== 'all') {
    allDisplayWords = allDisplayWords.filter(function(w) {
      return getWordStatus(w.word) === currentCategoryFilter;
    });
  }

  const totalPages = Math.ceil(allDisplayWords.length / PAGE_SIZE);
  if (currentPage > totalPages) currentPage = totalPages || 1;

  const start = (currentPage - 1) * PAGE_SIZE;
  const pageWords = allDisplayWords.slice(start, start + PAGE_SIZE);

  container.innerHTML = pageWords.map(function(w) {
    var globalIdx = ALL_WORDS.indexOf(w) + 1;
    var status = getWordStatus(w.word);
    var statusClass = status !== 'none' ? ' status-' + status : '';
    var badge = '';
    if (status === 'learned') badge = '<span class="card-badge">학습 완료</span>';
    else if (status === 'confused') badge = '<span class="card-badge">헷갈림</span>';
    return '<div class="word-card' + statusClass + '" data-word="' + w.word + '">' +
      badge +
      '<span class="num">' + globalIdx + '</span>' +
      '<span class="eng">' + w.word + '</span>' +
      '<button class="speak-btn" onclick="event.stopPropagation();speak(&apos;' + w.word + '&apos;)" title="발음 듣기">&#9654;</button>' +
      '<button class="speak-btn" onclick="event.stopPropagation();openDict(&apos;' + w.word + '&apos;)" title="사전 보기" style="font-size:0.75rem;">&#128214;</button>' +
      '<span class="kor">' + w.meaning + '</span>' +
    '</div>';
  }).join('');
  document.getElementById('totalWords').textContent = ALL_WORDS.length;
  renderPagination(totalPages);
  updateCategoryCounts();
}

document.getElementById('wordListView').addEventListener('click', function(e) {
  var card = e.target.closest('.word-card');
  if (!card) return;
  var word = card.getAttribute('data-word');
  if (!word) return;
  cycleWordStatus(word);
  renderWordList();
});

function renderPagination(totalPages) {
  const container = document.getElementById('pagination');
  if (totalPages <= 1) { container.innerHTML = ''; return; }
  let html = '';
  html += '<button onclick="goPage(1)" ' + (currentPage === 1 ? 'disabled' : '') + '>&laquo;</button>';
  html += '<button onclick="goPage(' + (currentPage - 1) + ')" ' + (currentPage === 1 ? 'disabled' : '') + '>&lsaquo;</button>';

  var startP = Math.max(1, currentPage - 3);
  var endP = Math.min(totalPages, currentPage + 3);
  if (startP > 1) html += '<span class="page-info">...</span>';
  for (var p = startP; p <= endP; p++) {
    html += '<button onclick="goPage(' + p + ')" class="' + (p === currentPage ? 'active' : '') + '">' + p + '</button>';
  }
  if (endP < totalPages) html += '<span class="page-info">...</span>';

  html += '<button onclick="goPage(' + (currentPage + 1) + ')" ' + (currentPage === totalPages ? 'disabled' : '') + '>&rsaquo;</button>';
  html += '<button onclick="goPage(' + totalPages + ')" ' + (currentPage === totalPages ? 'disabled' : '') + '>&raquo;</button>';
  html += '<span class="page-info">' + currentPage + ' / ' + totalPages + ' 페이지</span>';
  container.innerHTML = html;
}

function goPage(p) {
  var dw = getDisplayWords();
  if (currentCategoryFilter !== 'all') dw = dw.filter(function(w) { return getWordStatus(w.word) === currentCategoryFilter; });
  var totalPages = Math.ceil(dw.length / PAGE_SIZE);
  if (p < 1 || p > totalPages) return;
  currentPage = p;
  renderWordList();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function searchWords() { currentPage = 1; renderWordList(); }

function switchMode(mode) {
  currentMode = mode;
  document.getElementById('btnList').classList.toggle('active', mode === 'list');
  document.getElementById('btnTyping').classList.toggle('active', mode === 'typing');
  document.getElementById('btnTest').classList.toggle('active', mode === 'test');
  document.getElementById('completeScreen').classList.remove('active');

  document.getElementById('wordListView').style.display = 'none';
  document.getElementById('pagination').style.display = 'none';
  document.getElementById('typingView').style.display = 'none';
  document.getElementById('testView').style.display = 'none';

  if (mode === 'list') {
    document.getElementById('wordListView').style.display = 'grid';
    document.getElementById('pagination').style.display = 'flex';
  } else if (mode === 'typing') {
    document.getElementById('typingView').style.display = 'block';
    updateTypingCategoryInfo();
    resetTyping();
  } else if (mode === 'test') {
    document.getElementById('testView').style.display = 'block';
    showTestSetup();
  }
}

var savedSettings = {};
var settingsKeys = ['repeatCount', 'orderSelect', 'meaningDisplay', 'autoNext', 'typingCategorySelect'];
var settingsDefaults = { repeatCount: '3', orderSelect: 'sequential', meaningDisplay: 'always', autoNext: 'yes', typingCategorySelect: 'all' };

function loadSavedSettings() {
  try {
    var s = localStorage.getItem('toeic_settings');
    if (s) {
      var parsed = JSON.parse(s);
      for (var i = 0; i < settingsKeys.length; i++) {
        var k = settingsKeys[i];
        if (parsed[k]) document.getElementById(k).value = parsed[k];
      }
    }
  } catch(e) {}
}
function persistSettings() {
  var obj = {};
  for (var i = 0; i < settingsKeys.length; i++) {
    obj[settingsKeys[i]] = document.getElementById(settingsKeys[i]).value;
  }
  try { localStorage.setItem('toeic_settings', JSON.stringify(obj)); } catch(e) {}
}
function snapshotSettings() {
  savedSettings = {};
  for (var i = 0; i < settingsKeys.length; i++) {
    savedSettings[settingsKeys[i]] = document.getElementById(settingsKeys[i]).value;
  }
}
function restoreSettings() {
  for (var i = 0; i < settingsKeys.length; i++) {
    var k = settingsKeys[i];
    document.getElementById(k).value = savedSettings[k] || settingsDefaults[k];
  }
  updateTypingCategoryInfo();
}
function toggleSettings() {
  var panel = document.getElementById('settingsPanel');
  if (!panel.classList.contains('active')) {
    snapshotSettings();
  }
  panel.classList.toggle('active');
}
function applySettings() {
  persistSettings();
  document.getElementById('settingsPanel').classList.remove('active');
  if (currentMode === 'typing') resetTyping();
}
function cancelSettings() {
  restoreSettings();
  document.getElementById('settingsPanel').classList.remove('active');
}

function getTypingPool() {
  var cat = document.getElementById('typingCategorySelect').value;
  if (cat === 'all') return filteredWords;
  return filteredWords.filter(function(w) { return getWordStatus(w.word) === cat; });
}

function updateTypingCategoryInfo() {
  var pool = getTypingPool();
  document.getElementById('typingCategoryInfo').textContent = '(' + pool.length + '개)';
}

function resetTyping() {
  var pool = getTypingPool();
  if (pool.length === 0) {
    document.getElementById('typingView').innerHTML =
      '<div style="text-align:center; margin-top:80px;">' +
      '<div style="font-size:1.5rem; color:#f59e0b; margin-bottom:16px;">선택한 카테고리에 단어가 없습니다</div>' +
      '<div style="color:#94a3b8; margin-bottom:30px;">설정에서 다른 카테고리를 선택해 주세요</div>' +
      '<button class="btn-primary" style="padding:10px 24px; border:none; border-radius:8px; font-size:0.95rem; cursor:pointer;" onclick="document.getElementById(&apos;settingsPanel&apos;).classList.add(&apos;active&apos;)">설정 열기</button>' +
      '</div>';
    return;
  }
  // Restore typing view HTML if it was replaced
  restoreTypingView();
  const order = document.getElementById('orderSelect').value;
  typingWords = pool.slice();
  if (order === 'random') {
    for (let i = typingWords.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [typingWords[i], typingWords[j]] = [typingWords[j], typingWords[i]];
    }
  }
  typingIndex = 0;
  currentRepeat = 0;
  totalAttempts = 0;
  correctAttempts = 0;
  startTime = Date.now();
  document.getElementById('completeScreen').classList.remove('active');
  document.getElementById('typingView').style.display = 'block';
  showCurrentWord();
}

var typingViewOriginal = '';
var testSetupOriginal = '';
function saveTypingViewHTML() { typingViewOriginal = document.getElementById('typingView').innerHTML; }
function saveTestSetupHTML() { testSetupOriginal = document.getElementById('testSetup').innerHTML; }
function restoreTypingView() {
  if (typingViewOriginal && document.getElementById('typingInput') === null) {
    document.getElementById('typingView').innerHTML = typingViewOriginal;
    document.getElementById('typingInput').addEventListener('input', typingInputHandler);
    document.getElementById('typingInput').addEventListener('keydown', typingKeydownHandler);
  }
}
function restoreTestSetup() {
  if (testSetupOriginal && document.getElementById('testCategorySelect') === null) {
    document.getElementById('testSetup').innerHTML = testSetupOriginal;
  }
}

function showCurrentWord() {
  if (typingIndex >= typingWords.length) {
    showComplete();
    return;
  }
  const word = typingWords[typingIndex];
  const repeatMax = parseInt(document.getElementById('repeatCount').value) || 3;
  const meaningMode = document.getElementById('meaningDisplay').value;

  document.getElementById('englishWord').textContent = word.word;
  if (meaningMode === 'always' || (meaningMode === 'before' && currentRepeat === 0)) {
    document.getElementById('meaningText').textContent = word.meaning;
  } else {
    document.getElementById('meaningText').textContent = '';
  }
  document.getElementById('repeatInfo').textContent = (currentRepeat + 1) + ' / ' + repeatMax + ' 회';

  const total = typingWords.length * repeatMax;
  const done = typingIndex * repeatMax + currentRepeat;
  const pct = Math.round((done / total) * 100);
  document.getElementById('progressLeft').textContent = (typingIndex + 1) + ' / ' + typingWords.length;
  document.getElementById('progressBar').style.width = pct + '%';
  document.getElementById('progressRight').textContent = pct + '%';

  renderCharPreview(word.word, '');
  const input = document.getElementById('typingInput');
  input.value = '';
  input.className = 'typing-input';
  input.focus();
  document.getElementById('feedback').innerHTML = '';
}

function renderCharPreview(target, typed) {
  const container = document.getElementById('charPreview');
  let html = '';
  for (let i = 0; i < target.length; i++) {
    let cls = 'char-box';
    if (i < typed.length) {
      cls += typed[i].toLowerCase() === target[i].toLowerCase() ? ' correct filled' : ' wrong filled';
    } else if (i === typed.length) {
      cls += ' current';
    }
    const display = i < typed.length ? typed[i] : target[i];
    html += '<div class="' + cls + '">' + display + '</div>';
  }
  container.innerHTML = html;
}

function typingInputHandler(e) {
  var el = document.getElementById('typingInput');
  const word = typingWords[typingIndex];
  if (!word) return;
  const typed = el.value;
  renderCharPreview(word.word, typed);

  if (typed.length === word.word.length) {
    totalAttempts++;
    if (typed.toLowerCase() === word.word.toLowerCase()) {
      correctAttempts++;
      el.className = 'typing-input correct';
      document.getElementById('feedback').innerHTML = '<span class="feedback-correct">정답!</span>';
      const repeatMax = parseInt(document.getElementById('repeatCount').value) || 3;
      currentRepeat++;
      if (currentRepeat >= repeatMax) {
        currentRepeat = 0;
        typingIndex++;
      }
      const autoNext = document.getElementById('autoNext').value;
      if (autoNext === 'yes') {
        setTimeout(function() { showCurrentWord(); }, 400);
      }
    } else {
      el.className = 'typing-input wrong';
      document.getElementById('feedback').innerHTML =
        '<span class="feedback-wrong">오답! 정답: <strong>' + word.word + '</strong></span>';
    }
  } else {
    el.className = 'typing-input';
    document.getElementById('feedback').innerHTML = '';
  }
}

function typingKeydownHandler(e) {
  var el = document.getElementById('typingInput');
  if (e.key === 'Enter') {
    if (el.className.includes('wrong')) {
      el.value = '';
      el.className = 'typing-input';
      document.getElementById('feedback').innerHTML = '<span class="feedback-info">다시 입력하세요</span>';
      renderCharPreview(typingWords[typingIndex].word, '');
    } else if (el.className.includes('correct')) {
      showCurrentWord();
    }
  }
}

document.getElementById('typingInput').addEventListener('input', typingInputHandler);
document.getElementById('typingInput').addEventListener('keydown', typingKeydownHandler);
saveTypingViewHTML();
saveTestSetupHTML();

function skipWord() {
  currentRepeat = 0;
  typingIndex++;
  showCurrentWord();
}

function updateAccuracy() {
  const pct = totalAttempts > 0 ? Math.round((correctAttempts / totalAttempts) * 100) : 0;
  document.getElementById('accuracy').textContent = pct;
}

function showComplete() {
  document.getElementById('typingView').style.display = 'none';
  const screen = document.getElementById('completeScreen');
  screen.classList.add('active');
  document.getElementById('completedWords').textContent = typingWords.length;
  const pct = totalAttempts > 0 ? Math.round((correctAttempts / totalAttempts) * 100) : 0;
  document.getElementById('completedAccuracy').textContent = pct + '%';
  const elapsed = Math.round((Date.now() - startTime) / 1000);
  const min = Math.floor(elapsed / 60);
  const sec = elapsed % 60;
  document.getElementById('completedTime').textContent = min + ':' + String(sec).padStart(2, '0');
}

/* ===== TEST MODE ===== */
var testType = '';
var testQuestions = [];
var testIndex = 0;
var testResults = [];
var testStartTime = null;
var testAnswered = false;

function selectTestType(type) {
  testType = type;
  document.getElementById('testTypeKorToEng').classList.toggle('selected', type === 'kor-to-eng');
  document.getElementById('testTypeEngToKor').classList.toggle('selected', type === 'eng-to-kor');
  document.getElementById('testStartBtn').disabled = false;
}

function getTestPool() {
  var cat = document.getElementById('testCategorySelect').value;
  if (cat === 'all') return filteredWords;
  return filteredWords.filter(function(w) { return getWordStatus(w.word) === cat; });
}

function updateTestCategoryCount() {
  var pool = getTestPool();
  var count = pool.length;
  document.getElementById('testCategoryCount').textContent = '(' + count + '개)';
  var rangeText = document.getElementById('rangeSelect').options[document.getElementById('rangeSelect').selectedIndex].textContent;
  var catName = document.getElementById('testCategorySelect').options[document.getElementById('testCategorySelect').selectedIndex].textContent;
  document.getElementById('testRangeInfo').textContent = rangeText + ' 범위 중 ' + catName + ' ' + count + '개에서 출제';
}

function showTestSetup() {
  restoreTestSetup();
  document.getElementById('testSetup').style.display = 'block';
  document.getElementById('testArea').style.display = 'none';
  document.getElementById('testResult').style.display = 'none';
  testType = '';
  document.getElementById('testTypeKorToEng').classList.remove('selected');
  document.getElementById('testTypeEngToKor').classList.remove('selected');
  document.getElementById('testStartBtn').disabled = true;
  document.getElementById('testCategorySelect').value = 'all';
  var rangeText = document.getElementById('rangeSelect').options[document.getElementById('rangeSelect').selectedIndex].textContent;
  document.getElementById('testRangeInfo').textContent = rangeText + ' 범위에서 출제';
  updateTestCategoryCount();
  document.getElementById('testCategorySelect').onchange = updateTestCategoryCount;
}

function shuffleArray(arr) {
  var a = arr.slice();
  for (var i = a.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = a[i]; a[i] = a[j]; a[j] = tmp;
  }
  return a;
}

function startTest(customWords) {
  var pool = customWords || getTestPool();
  if (pool.length === 0) {
    document.getElementById('testSetup').innerHTML =
      '<div style="text-align:center; margin-top:80px;">' +
      '<div style="font-size:1.5rem; color:#f59e0b; margin-bottom:16px;">선택한 카테고리에 단어가 없습니다</div>' +
      '<div style="color:#94a3b8; margin-bottom:30px;">다른 카테고리를 선택해 주세요</div>' +
      '<button class="btn-primary" style="padding:10px 24px; border:none; border-radius:8px; font-size:0.95rem; cursor:pointer;" onclick="switchMode(&apos;test&apos;)">돌아가기</button>' +
      '</div>';
    return;
  }
  var countEl = document.getElementById('testQuestionCount');
  var countVal = countEl ? countEl.value : 'all';
  var count = countVal === 'all' ? pool.length : parseInt(countVal);
  count = Math.min(count, pool.length);

  testQuestions = shuffleArray(pool).slice(0, count);
  testIndex = 0;
  testResults = [];
  testStartTime = Date.now();
  testAnswered = false;

  document.getElementById('testSetup').style.display = 'none';
  document.getElementById('testArea').style.display = 'block';
  document.getElementById('testResult').style.display = 'none';
  showTestQuestion();
}

function generateChoices(correctWord) {
  var choices = [correctWord];
  var pool = ALL_WORDS.slice();
  // Shuffle pool
  for (var i = pool.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = pool[i]; pool[i] = pool[j]; pool[j] = tmp;
  }
  for (var k = 0; k < pool.length && choices.length < 4; k++) {
    if (pool[k].word !== correctWord.word) {
      choices.push(pool[k]);
    }
  }
  // Shuffle choices
  for (var i = choices.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = choices[i]; choices[i] = choices[j]; choices[j] = tmp;
  }
  return choices;
}

function selectChoice(idx) {
  if (testAnswered) return;
  testAnswered = true;
  var word = testQuestions[testIndex];
  var choices = currentChoices;
  var selected = choices[idx];
  var isCorrect = selected.word === word.word;

  testResults.push({ word: word, typed: selected.meaning, correct: isCorrect });

  var btns = document.getElementById('testChoicesArea').querySelectorAll('.choice-btn');
  for (var i = 0; i < btns.length; i++) {
    if (choices[i].word === word.word) {
      btns[i].classList.add('choice-correct');
    } else if (i === idx) {
      btns[i].classList.add('choice-wrong');
    } else {
      btns[i].classList.add('choice-dim');
    }
    btns[i].style.cursor = 'default';
  }

  if (isCorrect) {
    document.getElementById('testAnswerReveal').innerHTML = '<span class="feedback-correct">정답!</span>';
  } else {
    var rHtml = '<span class="feedback-wrong">오답!</span> <span style="color:var(--text-secondary,#94a3b8);">정답: <strong style="color:var(--accent,#60a5fa);">' + word.word + '</strong> ' + word.meaning + '</span>';
    if (getWordStatus(word.word) === 'learned') {
      rHtml += '<div style="margin-top:10px;padding:10px;background:var(--amber-bg,rgba(251,191,36,0.08));border:1px solid var(--amber-border,rgba(251,191,36,0.3));border-radius:8px;">';
      rHtml += '<div style="color:var(--amber,#fbbf24);font-size:0.88rem;margin-bottom:8px;">학습 완료 단어인데 틀렸습니다. 헷갈리는 단어로 이동할까요?</div>';
      rHtml += '<button onclick="moveToConfused(&apos;' + word.word + '&apos;,this)" style="padding:6px 16px;background:var(--amber,#fbbf24);color:#451a03;border:none;border-radius:6px;cursor:pointer;font-size:0.82rem;font-weight:600;font-family:inherit;margin-right:6px;">이동</button>';
      rHtml += '<button onclick="this.parentElement.style.display=&apos;none&apos;" style="padding:6px 16px;background:var(--bg-elevated,#1c2137);color:var(--text-secondary,#8b92ab);border:1px solid var(--border,#2a3050);border-radius:6px;cursor:pointer;font-size:0.82rem;font-family:inherit;">유지</button>';
      rHtml += '</div>';
    }
    document.getElementById('testAnswerReveal').innerHTML = rHtml;
  }

  document.getElementById('testSubmitBtn').style.display = 'none';
  document.getElementById('testNextBtn').style.display = 'inline-block';
  document.getElementById('testNextBtn').focus();
}

var currentChoices = [];

function showTestQuestion() {
  testSynonymRetry = false;
  if (testIndex >= testQuestions.length) {
    showTestResult();
    return;
  }
  testAnswered = false;
  var word = testQuestions[testIndex];
  var pct = Math.round((testIndex / testQuestions.length) * 100);
  document.getElementById('testProgressLeft').textContent = (testIndex + 1) + ' / ' + testQuestions.length;
  document.getElementById('testProgressBar').style.width = pct + '%';
  document.getElementById('testProgressRight').textContent = pct + '%';

  document.getElementById('testAnswerReveal').innerHTML = '';
  document.getElementById('testNextBtn').style.display = 'none';

  if (testType === 'kor-to-eng') {
    document.getElementById('testQuestionLabel').textContent = '다음 뜻에 해당하는 영단어를 입력하세요';
    document.getElementById('testQuestion').textContent = word.meaning;
    document.getElementById('testQuestionSub').textContent = word.word.length + '글자';
    document.getElementById('testTypingArea').style.display = 'block';
    document.getElementById('testChoicesArea').style.display = 'none';
    document.getElementById('testSubmitBtn').style.display = 'inline-block';
    var input = document.getElementById('testInput');
    input.value = '';
    input.className = 'test-input';
    input.focus();
  } else {
    document.getElementById('testQuestionLabel').textContent = '다음 영단어의 뜻을 고르세요';
    document.getElementById('testQuestion').textContent = word.word;
    document.getElementById('testQuestionSub').textContent = '';
    document.getElementById('testTypingArea').style.display = 'none';
    document.getElementById('testChoicesArea').style.display = 'block';
    document.getElementById('testSubmitBtn').style.display = 'none';

    currentChoices = generateChoices(word);
    var choicesHtml = '<div class="choices-grid">';
    for (var i = 0; i < currentChoices.length; i++) {
      choicesHtml += '<button class="choice-btn" onclick="selectChoice(' + i + ')">' +
        '<span class="choice-num">' + (i + 1) + '</span>' +
        currentChoices[i].meaning + '</button>';
    }
    choicesHtml += '</div>';
    document.getElementById('testChoicesArea').innerHTML = choicesHtml;
  }
}

var testSynonymRetry = false;

function isSynonym(typed, targetWord) {
  if (testType !== 'kor-to-eng') return false;
  var typedLower = typed.toLowerCase();
  // Check if typed word exists in the word list but is a different word
  for (var i = 0; i < ALL_WORDS.length; i++) {
    if (ALL_WORDS[i].word.toLowerCase() === typedLower && ALL_WORDS[i].word.toLowerCase() !== targetWord.word.toLowerCase()) {
      // Check if meanings overlap
      var typedMeaning = ALL_WORDS[i].meaning;
      var targetMeaning = targetWord.meaning;
      // Extract Korean keywords (2+ chars, not grammar markers)
      var getKeywords = function(m) {
        return m.replace(/\\([^)]*\\)/g, ' ').replace(/[,]/g, ' ').split(/\\s+/).filter(function(s) {
          return s.length >= 2 && !/^(하다|되다|시키다|있는|없는|되는|하는)$/.test(s);
        });
      };
      var kw1 = getKeywords(typedMeaning);
      var kw2 = getKeywords(targetMeaning);
      for (var a = 0; a < kw1.length; a++) {
        for (var b = 0; b < kw2.length; b++) {
          if (kw1[a] === kw2[b] || kw1[a].includes(kw2[b]) || kw2[b].includes(kw1[a])) {
            return true;
          }
        }
      }
    }
  }
  return false;
}

function showTestHint() {
  var word = testQuestions[testIndex];
  var hint = word.word[0] + '_'.repeat(word.word.length - 1);
  document.getElementById('testHintArea').innerHTML =
    '<span style="color:#60a5fa; font-size:1.2rem; letter-spacing:3px; font-weight:bold;">' + hint + '</span>' +
    ' <span style="color:#64748b;">(' + word.word.length + '글자)</span>';
}

function submitTestAnswer() {
  if (testAnswered) return;
  var word = testQuestions[testIndex];
  var input = document.getElementById('testInput');
  var typed = input.value.trim();
  var isCorrect = false;

  if (testType === 'kor-to-eng') {
    isCorrect = typed.toLowerCase() === word.word.toLowerCase();
  } else {
    var meaningClean = word.meaning.replace(/\\([^)]*\\)/g, '').replace(/,/g, ' ').replace(/\\s+/g, ' ').trim();
    var meaningParts = meaningClean.split(' ').filter(function(s) { return s.length > 1; });
    var typedClean = typed.replace(/\\s+/g, '');
    isCorrect = false;
    if (typedClean.length >= 2) {
      if (word.meaning.includes(typedClean)) {
        isCorrect = true;
      } else {
        for (var k = 0; k < meaningParts.length; k++) {
          if (meaningParts[k].includes(typedClean) || typedClean.includes(meaningParts[k])) {
            isCorrect = true;
            break;
          }
        }
      }
    }
  }

  // Synonym detection for kor-to-eng
  if (!isCorrect && testType === 'kor-to-eng' && !testSynonymRetry && isSynonym(typed, word)) {
    testSynonymRetry = true;
    input.className = 'test-input';
    input.style.borderColor = '#f59e0b';
    var revealHtml = '<div style="color:#f59e0b; margin-bottom:8px;">해당 단어도 의미는 맞습니다. 하지만 다른 단어도 있습니다!</div>';
    revealHtml += '<div style="color:#94a3b8; font-size:0.85rem; margin-bottom:10px;">다시 입력해 보세요</div>';
    revealHtml += '<div id="testHintArea" style="margin-bottom:10px;"></div>';
    revealHtml += '<button class="test-nav-btn" style="padding:6px 18px; font-size:0.85rem;" onclick="showTestHint()">힌트 보기 (첫 글자)</button>';
    document.getElementById('testAnswerReveal').innerHTML = revealHtml;
    input.value = '';
    input.focus();
    return;
  }

  testAnswered = true;
  testSynonymRetry = false;
  testResults.push({ word: word, typed: typed, correct: isCorrect });

  if (isCorrect) {
    input.className = 'test-input correct';
    document.getElementById('testAnswerReveal').innerHTML = '<span class="feedback-correct">정답!</span>';
  } else {
    input.className = 'test-input wrong';
    var revealHtml = '<span class="feedback-wrong">오답</span><br>';
    revealHtml += '<span class="answer-word">' + word.word + '</span> ';
    revealHtml += '<span class="answer-meaning">' + word.meaning + '</span>';
    // 학습완료 단어가 오답이면 헷갈리는 단어로 이동 제안
    if (getWordStatus(word.word) === 'learned') {
      revealHtml += '<div style="margin-top:10px;padding:10px;background:var(--amber-bg,rgba(251,191,36,0.08));border:1px solid var(--amber-border,rgba(251,191,36,0.3));border-radius:8px;">';
      revealHtml += '<div style="color:var(--amber,#fbbf24);font-size:0.88rem;margin-bottom:8px;">학습 완료 단어인데 틀렸습니다. 헷갈리는 단어로 이동할까요?</div>';
      revealHtml += '<button onclick="moveToConfused(&apos;' + word.word + '&apos;,this)" style="padding:6px 16px;background:var(--amber,#fbbf24);color:#451a03;border:none;border-radius:6px;cursor:pointer;font-size:0.82rem;font-weight:600;font-family:inherit;margin-right:6px;">이동</button>';
      revealHtml += '<button onclick="this.parentElement.style.display=&apos;none&apos;" style="padding:6px 16px;background:var(--bg-elevated,#1c2137);color:var(--text-secondary,#8b92ab);border:1px solid var(--border,#2a3050);border-radius:6px;cursor:pointer;font-size:0.82rem;font-family:inherit;">유지</button>';
      revealHtml += '</div>';
    }
    document.getElementById('testAnswerReveal').innerHTML = revealHtml;
  }

  document.getElementById('testSubmitBtn').style.display = 'none';
  document.getElementById('testNextBtn').style.display = 'inline-block';
  document.getElementById('testNextBtn').focus();
}

function moveToConfused(word, btn) {
  wordStatus[word] = 'confused';
  saveWordStatus();
  updateHeaderStats();
  btn.parentElement.innerHTML = '<span style="color:var(--green,#4ade80);font-size:0.85rem;">헷갈리는 단어로 이동 완료!</span>';
}

function nextTestQuestion() {
  testIndex++;
  showTestQuestion();
}

function showTestResult() {
  document.getElementById('testArea').style.display = 'none';
  document.getElementById('testResult').style.display = 'block';

  var correctCount = testResults.filter(function(r) { return r.correct; }).length;
  var total = testResults.length;
  var pct = total > 0 ? Math.round((correctCount / total) * 100) : 0;

  document.getElementById('testScoreNum').textContent = correctCount;
  document.getElementById('testScoreLabel').textContent = '/ ' + total;
  document.getElementById('testResultAccuracy').textContent = pct + '%';

  // Color the score circle based on result
  var circle = document.querySelector('.score-circle');
  if (pct >= 90) { circle.style.borderColor = '#22c55e'; document.getElementById('testScoreNum').style.color = '#22c55e'; document.getElementById('testResultTitle').textContent = '훌륭합니다!'; }
  else if (pct >= 70) { circle.style.borderColor = '#60a5fa'; document.getElementById('testScoreNum').style.color = '#60a5fa'; document.getElementById('testResultTitle').textContent = '잘했습니다!'; }
  else if (pct >= 50) { circle.style.borderColor = '#f59e0b'; document.getElementById('testScoreNum').style.color = '#f59e0b'; document.getElementById('testResultTitle').textContent = '조금 더 노력해봐요!'; }
  else { circle.style.borderColor = '#ef4444'; document.getElementById('testScoreNum').style.color = '#ef4444'; document.getElementById('testResultTitle').textContent = '다시 복습해보세요!'; }

  var elapsed = Math.round((Date.now() - testStartTime) / 1000);
  var min = Math.floor(elapsed / 60);
  var sec = elapsed % 60;
  document.getElementById('testResultTime').textContent = min + ':' + String(sec).padStart(2, '0');

  // Build result list (wrong answers only)
  var wrongResults = testResults.filter(function(r) { return !r.correct; });
  var listHtml = '';
  if (wrongResults.length === 0) {
    listHtml = '<div style="text-align:center; color:#22c55e; padding:20px;">모두 정답! 오답이 없습니다.</div>';
    document.getElementById('retestWrongBtn').style.display = 'none';
  } else {
    document.getElementById('retestWrongBtn').style.display = 'inline-block';
    for (var i = 0; i < wrongResults.length; i++) {
      var r = wrongResults[i];
      listHtml += '<div class="result-item wrong-item">' +
        '<span class="ri-word">' + r.word.word + '</span>' +
        '<span class="ri-meaning">' + r.word.meaning + '</span>' +
        '<span class="ri-typed">입력: ' + (r.typed || '(미입력)') + '</span>' +
      '</div>';
    }
  }
  document.getElementById('testResultList').innerHTML = listHtml;
}

function retestWrong() {
  var wrongWords = testResults.filter(function(r) { return !r.correct; }).map(function(r) { return r.word; });
  if (wrongWords.length === 0) return;
  startTest(wrongWords);
}

// Test input Enter key handler
document.getElementById('testInput').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') {
    if (!testAnswered) {
      submitTestAnswer();
    } else {
      nextTestQuestion();
    }
  }
});

// Keyboard support for multiple choice (1-4) and Enter for next
document.addEventListener('keydown', function(e) {
  if (currentMode !== 'test' || testType !== 'eng-to-kor') return;
  if (e.key >= '1' && e.key <= '4' && !testAnswered) {
    selectChoice(parseInt(e.key) - 1);
  } else if (e.key === 'Enter' && testAnswered) {
    nextTestQuestion();
  }
});

function toggleTheme() {
  var isLight = document.body.classList.toggle('light');
  document.getElementById('themeBtn').textContent = isLight ? 'Light' : 'Dark';
  try { localStorage.setItem('toeic_theme', isLight ? 'light' : 'dark'); } catch(e) {}
}
(function() {
  try {
    var t = localStorage.getItem('toeic_theme');
    if (t === 'light') {
      document.body.classList.add('light');
      document.getElementById('themeBtn').textContent = 'Light';
    }
  } catch(e) {}
})();

/* ===== CUSTOM WORDS ===== */
/* ===== DICTIONARY ===== */
var posMap = {noun:'명사',verb:'동사',adjective:'형용사',adverb:'부사',preposition:'전치사',conjunction:'접속사',interjection:'감탄사',pronoun:'대명사'};
function translateText(text) {
  return fetch('https://api.mymemory.translated.net/get?q=' + encodeURIComponent(text) + '&langpair=en|ko')
    .then(function(r) { return r.json(); })
    .then(function(d) { return (d.responseData && d.responseData.translatedText) || text; })
    .catch(function() { return text; });
}
function openDict(word) {
  document.getElementById('dictOverlay').classList.add('active');
  document.getElementById('dictWord').textContent = word;
  document.getElementById('dictContent').innerHTML = '<div class="dict-loading">번역하는 중...</div>';
  fetch('https://api.dictionaryapi.dev/api/v2/entries/en/' + encodeURIComponent(word))
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (!Array.isArray(data) || data.length === 0) throw new Error('not found');
      var entry = data[0];
      var phonetic = entry.phonetic || '';
      if (!phonetic && entry.phonetics) {
        for (var p = 0; p < entry.phonetics.length; p++) {
          if (entry.phonetics[p].text) { phonetic = entry.phonetics[p].text; break; }
        }
      }
      // Collect all definitions and examples to translate
      var items = []; // {type, pos, text, example}
      if (entry.meanings) {
        for (var m = 0; m < entry.meanings.length; m++) {
          var mg = entry.meanings[m];
          var defs = mg.definitions || [];
          for (var d = 0; d < Math.min(defs.length, 3); d++) {
            items.push({ pos: mg.partOfSpeech, def: defs[d].definition, example: defs[d].example || '' });
          }
        }
      }
      // Translate all definitions in parallel
      var promises = items.map(function(it) {
        return translateText(it.def).then(function(tr) { it.defKo = tr; return it; });
      });
      return Promise.all(promises).then(function() {
        var html = '';
        if (phonetic) html += '<div class="dict-phonetic">' + phonetic + '</div>';
        var lastPos = '';
        for (var i = 0; i < items.length; i++) {
          if (items[i].pos !== lastPos) {
            lastPos = items[i].pos;
            html += '<div class="dict-pos">' + (posMap[lastPos] || lastPos) + ' (' + lastPos + ')</div>';
          }
          html += '<div class="dict-def">' + items[i].defKo + '</div>';
          html += '<div style="color:var(--text-dim);font-size:0.78rem;margin:2px 0 6px 12px;">' + items[i].def + '</div>';
          if (items[i].example) {
            html += '<div class="dict-example">&ldquo;' + items[i].example + '&rdquo;</div>';
          }
        }
        html += '<div class="dict-src">Source: dictionaryapi.dev + mymemory.translated.net</div>';
        document.getElementById('dictContent').innerHTML = html;
      });
    })
    .catch(function() {
      document.getElementById('dictContent').innerHTML = '<div class="dict-error">사전 데이터를 찾을 수 없습니다.<br><span style="font-size:0.82rem;color:var(--text-dim);">인터넷 연결을 확인하세요.</span></div>';
    });
}
function closeDict() {
  document.getElementById('dictOverlay').classList.remove('active');
}

/* ===== TTS ===== */
function speak(word) {
  try {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(word);
    u.lang = 'en-US'; u.rate = 0.9;
    window.speechSynthesis.speak(u);
  } catch(e) {}
}

function loadCustomWords() {
  try {
    var cw = localStorage.getItem('toeic_custom_words');
    if (cw) {
      var arr = JSON.parse(cw);
      arr.forEach(function(w) {
        if (!ALL_WORDS.some(function(aw) { return aw.word.toLowerCase() === w.word.toLowerCase(); })) {
          ALL_WORDS.push(w);
        }
      });
    }
  } catch(e) {}
}
function saveCustomWords() {
  try {
    var cw = localStorage.getItem('toeic_custom_words');
    var arr = cw ? JSON.parse(cw) : [];
    localStorage.setItem('toeic_custom_words', JSON.stringify(arr));
  } catch(e) {}
}
function openAddWord() {
  document.getElementById('addWordModal').classList.add('active');
  document.getElementById('addWordEng').value = '';
  document.getElementById('addWordKor').value = '';
  document.getElementById('addWordMsg').innerHTML = '';
  document.getElementById('addWordEng').focus();
}
function closeAddWord() {
  document.getElementById('addWordModal').classList.remove('active');
}
function saveAddWord() {
  var eng = document.getElementById('addWordEng').value.trim();
  var kor = document.getElementById('addWordKor').value.trim();
  if (!eng || !kor) {
    document.getElementById('addWordMsg').innerHTML = '<span style="color:var(--red);">영단어와 뜻을 모두 입력하세요</span>';
    return;
  }
  if (ALL_WORDS.some(function(w) { return w.word.toLowerCase() === eng.toLowerCase(); })) {
    document.getElementById('addWordMsg').innerHTML = '<span style="color:var(--amber);">이미 존재하는 단어입니다</span>';
    return;
  }
  var newWord = { word: eng, meaning: kor };
  ALL_WORDS.push(newWord);
  // Save to localStorage
  try {
    var cw = localStorage.getItem('toeic_custom_words');
    var arr = cw ? JSON.parse(cw) : [];
    arr.push(newWord);
    localStorage.setItem('toeic_custom_words', JSON.stringify(arr));
  } catch(e) {}
  // Update range & list
  filteredWords = ALL_WORDS.slice(currentRange[0], currentRange[1]);
  document.getElementById('addWordMsg').innerHTML = '<span style="color:var(--green);"><b>' + eng + '</b> 추가 완료!</span>';
  document.getElementById('addWordEng').value = '';
  document.getElementById('addWordKor').value = '';
  document.getElementById('addWordEng').focus();
  renderWordList();
  updateHeaderStats();
}
// Enter key in modal
document.getElementById('addWordKor').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') saveAddWord();
});
// Close modal on overlay click
document.getElementById('addWordModal').addEventListener('click', function(e) {
  if (e.target === this) closeAddWord();
});

loadCustomWords();
initRanges();
loadSavedSettings();
renderWordList();
updateHeaderStats();
</script>
<footer style="text-align:center;padding:24px 16px 32px;color:var(--text-dim,#5a6178);font-size:0.75rem;line-height:1.6;">
  <div style="margin-bottom:4px;">Made by <strong style="color:var(--text-secondary,#8b92ab);">김찬희 (Kim Chanhee)</strong> &copy; 2026</div>
  <div>단어 데이터 출처: dokjongban.com &middot; MIT License</div>
</footer>
</body>
</html>"""

full_html = html_part1 + "const ALL_WORDS = " + words_json + ";\n" + html_part2

with open(r"C:\Users\chan7\toeic words\toeic-typing.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Created: C:\\Users\\chan7\\toeic-typing.html")
print(f"Total words: {len(words)}")
print(f"File size: {len(full_html)} bytes")
