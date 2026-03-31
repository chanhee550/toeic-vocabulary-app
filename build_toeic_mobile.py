import json

with open(r"C:\Users\chan7\toeic words\toeic_words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

words_json = json.dumps(words, ensure_ascii=False)

html_top = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#0c0f1a">
<title>TOEIC 단어장</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0c0f1a; --bg-card: #151929; --bg-el: #1c2137; --bg-input: #1a1f35;
    --border: #2a3050; --border-h: #4a5580;
    --t1: #eef0f6; --t2: #8b92ab; --t3: #5a6178;
    --acc: #6c8cff; --acc-h: #5570e0; --acc-glow: rgba(108,140,255,0.15); --acc-soft: rgba(108,140,255,0.08);
    --green: #4ade80; --green-bg: rgba(74,222,128,0.08); --green-bd: rgba(74,222,128,0.3);
    --red: #f87171; --red-bg: rgba(248,113,113,0.08); --red-bd: rgba(248,113,113,0.3);
    --amber: #fbbf24; --amber-bg: rgba(251,191,36,0.08); --amber-bd: rgba(251,191,36,0.3);
    --purple: #c4b5fd;
    --r: 14px; --r-sm: 10px; --r-full: 100px;
    --safe-b: env(safe-area-inset-bottom, 0px);
  }
  body.light {
    --bg: #f5f6fa; --bg-card: #ffffff; --bg-el: #f0f1f5; --bg-input: #ffffff;
    --border: #dfe2ea; --border-h: #b8bdd0;
    --t1: #1a1d2e; --t2: #5a5f73; --t3: #8b90a3;
    --acc: #4f6df5; --acc-h: #3d5ae0; --acc-glow: rgba(79,109,245,0.12); --acc-soft: rgba(79,109,245,0.06);
    --green: #16a34a; --green-bg: rgba(22,163,74,0.06); --green-bd: rgba(22,163,74,0.25);
    --red: #dc2626; --red-bg: rgba(220,38,38,0.06); --red-bd: rgba(220,38,38,0.25);
    --amber: #d97706; --amber-bg: rgba(217,119,6,0.06); --amber-bd: rgba(217,119,6,0.25);
    --purple: #7c3aed;
  }
  * { margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color: transparent; }
  body {
    font-family: 'Inter','Noto Sans KR',-apple-system,sans-serif;
    background: var(--bg); color: var(--t1);
    min-height: 100vh; min-height: 100dvh;
    -webkit-font-smoothing: antialiased;
    padding-bottom: calc(70px + var(--safe-b));
    overflow-x: hidden;
  }

  /* ===== TOP BAR ===== */
  .topbar {
    position: sticky; top: 0; z-index: 100;
    background: var(--bg); border-bottom: 1px solid var(--border);
    padding: 14px 16px; display: flex; justify-content: space-between; align-items: center;
    backdrop-filter: blur(12px);
  }
  .topbar h1 { font-size: 1.15rem; font-weight: 700; }
  .topbar h1 span { color: var(--acc); }
  .topbar-right { display: flex; gap: 8px; align-items: center; }
  .topbar-btn {
    background: var(--bg-el); border: 1px solid var(--border); color: var(--t2);
    padding: 6px 12px; border-radius: var(--r-full); cursor: pointer;
    font-size: 0.75rem; font-family: inherit; font-weight: 500;
  }

  /* ===== STATS BAR ===== */
  .stats-bar {
    display: flex; gap: 8px; padding: 10px 16px; overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  .stats-bar::-webkit-scrollbar { display: none; }
  .stat-chip {
    background: var(--bg-card); border: 1px solid var(--border);
    padding: 6px 14px; border-radius: var(--r-full); font-size: 0.75rem;
    color: var(--t2); white-space: nowrap; flex-shrink: 0;
  }
  .stat-chip b { color: var(--acc); font-weight: 600; }

  /* ===== BOTTOM NAV ===== */
  .bottom-nav {
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 100;
    background: var(--bg-card); border-top: 1px solid var(--border);
    display: flex; padding-bottom: var(--safe-b);
    backdrop-filter: blur(12px);
  }
  .nav-item {
    flex: 1; display: flex; flex-direction: column; align-items: center;
    padding: 10px 0 8px; cursor: pointer; color: var(--t3);
    font-size: 0.65rem; font-weight: 500; transition: color 0.2s;
    border: none; background: none; font-family: inherit;
  }
  .nav-item.active { color: var(--acc); }
  .nav-item svg { width: 22px; height: 22px; margin-bottom: 3px; }
  .nav-item.active svg { filter: drop-shadow(0 0 4px var(--acc-glow)); }

  /* ===== MAIN CONTENT ===== */
  .page { display: none; padding: 12px 16px; }
  .page.active { display: block; }

  /* ===== WORD LIST ===== */
  .filter-row {
    display: flex; gap: 6px; margin-bottom: 12px; overflow-x: auto;
    -webkit-overflow-scrolling: touch; padding-bottom: 4px;
  }
  .filter-row::-webkit-scrollbar { display: none; }
  .filter-btn {
    padding: 7px 14px; border: 1px solid var(--border); background: var(--bg-card);
    color: var(--t2); border-radius: var(--r-full); cursor: pointer;
    font-size: 0.78rem; font-weight: 500; white-space: nowrap; flex-shrink: 0;
    font-family: inherit;
  }
  .filter-btn.active { background: var(--acc); color: white; border-color: var(--acc); }
  .search-input {
    width: 100%; padding: 12px 16px; background: var(--bg-card);
    border: 1px solid var(--border); border-radius: var(--r);
    color: var(--t1); font-size: 0.92rem; font-family: inherit; margin-bottom: 12px;
  }
  .search-input:focus { border-color: var(--acc); outline: none; }
  .search-input::placeholder { color: var(--t3); }

  .wcard {
    background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--r);
    padding: 16px; margin-bottom: 8px; position: relative;
    transition: all 0.15s; cursor: pointer; -webkit-user-select: none; user-select: none;
  }
  .wcard:active { transform: scale(0.98); }
  .wcard .w-eng { color: var(--acc); font-weight: 600; font-size: 1.1rem; margin-bottom: 4px; }
  .wcard .w-kor { color: var(--t2); font-size: 0.88rem; line-height: 1.5; }
  .wcard .w-ipa { color: var(--t3); font-size: 0.75rem; font-style: italic; margin-bottom: 2px; font-family: 'Noto Sans', 'Lucida Sans Unicode', 'Arial Unicode MS', sans-serif; }
  .spk-btn {
    background: var(--acc-soft); border: 1px solid var(--border); color: var(--acc);
    width: 26px; height: 26px; border-radius: 50%; cursor: pointer; font-size: 0.65rem;
    display: inline-flex; align-items: center; justify-content: center;
    vertical-align: middle; margin-left: 6px; padding: 0;
  }
  .wcard .w-num { color: var(--t3); font-size: 0.7rem; position: absolute; top: 12px; right: 14px; }
  .wcard .w-badge {
    font-size: 0.6rem; font-weight: 600; padding: 2px 8px; border-radius: var(--r-full);
    position: absolute; bottom: 12px; right: 14px;
  }
  .wcard.st-learned { border-color: var(--green-bd); background: var(--green-bg); }
  .wcard.st-learned .w-badge { background: var(--green); color: #052e16; }
  .wcard.st-confused { border-color: var(--amber-bd); background: var(--amber-bg); }
  .wcard.st-confused .w-badge { background: var(--amber); color: #451a03; }
  body.light .wcard.st-learned .w-badge,
  body.light .wcard.st-confused .w-badge { color: white; }

  .range-select {
    width: 100%; padding: 10px 14px; background: var(--bg-card);
    border: 1px solid var(--border); border-radius: var(--r-sm);
    color: var(--t1); font-size: 0.85rem; font-family: inherit; margin-bottom: 12px;
  }

  .pager {
    display: flex; justify-content: center; align-items: center; gap: 8px;
    padding: 16px 0;
  }
  .pager button {
    padding: 10px 16px; background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r-sm); color: var(--t2); font-family: inherit;
    font-size: 0.85rem; font-weight: 500; cursor: pointer; min-width: 44px;
  }
  .pager button.active { background: var(--acc); color: white; border-color: var(--acc); }
  .pager button:disabled { opacity: 0.3; }
  .pager .pg-info { color: var(--t3); font-size: 0.8rem; }

  /* ===== LEARNING PAGE ===== */
  .learn-settings {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--r); padding: 18px; margin-bottom: 16px;
  }
  .ls-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
  .ls-row:last-child { margin-bottom: 0; }
  .ls-row label { color: var(--t2); font-size: 0.85rem; font-weight: 500; }
  .ls-row select, .ls-row input {
    padding: 8px 12px; background: var(--bg-input); border: 1px solid var(--border);
    border-radius: var(--r-sm); color: var(--t1); font-family: inherit; font-size: 0.85rem;
  }
  .start-btn {
    width: 100%; padding: 16px; background: var(--acc); color: white; border: none;
    border-radius: var(--r); font-size: 1rem; font-weight: 600; cursor: pointer;
    font-family: inherit; box-shadow: 0 4px 16px rgba(108,140,255,0.3);
  }
  .start-btn:active { transform: scale(0.98); }

  .learn-card {
    text-align: center; padding: 20px 0;
  }
  .lc-progress {
    display: flex; align-items: center; gap: 10px; margin-bottom: 28px;
  }
  .lc-pbar { flex: 1; height: 5px; background: var(--bg-el); border-radius: 3px; overflow: hidden; }
  .lc-pfill { height: 100%; background: linear-gradient(90deg, var(--acc), #a78bfa); border-radius: 3px; transition: width 0.3s; }
  .lc-ptext { color: var(--t3); font-size: 0.78rem; font-weight: 500; min-width: 40px; }
  .lc-meaning { font-size: 1.05rem; color: var(--t2); margin-bottom: 14px; min-height: 26px; }
  .lc-word { font-size: 2.6rem; font-weight: 700; color: var(--acc); letter-spacing: 2px; margin-bottom: 6px; }
  .lc-repeat { font-size: 0.82rem; color: var(--t3); margin-bottom: 24px; }
  .lc-chars {
    display: flex; justify-content: center; gap: 4px; margin-bottom: 20px;
    min-height: 46px; flex-wrap: wrap;
  }
  .lc-char {
    width: 34px; height: 42px; display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem; font-weight: 600; border-radius: var(--r-sm);
    border: 2px solid var(--border); background: var(--bg-card); color: var(--t3);
    font-family: 'Inter', monospace;
  }
  .lc-char.filled { color: var(--t1); border-color: var(--border-h); }
  .lc-char.correct { color: var(--green); border-color: var(--green-bd); background: var(--green-bg); }
  .lc-char.wrong { color: var(--red); border-color: var(--red-bd); background: var(--red-bg); }
  .lc-char.current { border-color: var(--acc); box-shadow: 0 0 10px var(--acc-glow); }
  .lc-input {
    width: 100%; padding: 14px; font-size: 1.4rem; text-align: center;
    background: var(--bg-input); border: 2px solid var(--border); border-radius: var(--r);
    color: var(--t1); font-family: 'Inter', monospace; letter-spacing: 3px; outline: none;
  }
  .lc-input:focus { border-color: var(--acc); }
  .lc-input.correct { border-color: var(--green); background: var(--green-bg); }
  .lc-input.wrong { border-color: var(--red); background: var(--red-bg); }
  .lc-feedback { font-size: 1rem; min-height: 26px; margin: 12px 0; font-weight: 500; }
  .lc-btns { display: flex; gap: 8px; margin-top: 12px; }
  .lc-btns button {
    flex: 1; padding: 12px; border: 1px solid var(--border); background: var(--bg-el);
    color: var(--t2); border-radius: var(--r-sm); cursor: pointer; font-family: inherit;
    font-size: 0.88rem; font-weight: 500;
  }
  .lc-btns .primary { background: var(--acc); color: white; border-color: var(--acc); }

  /* ===== TEST PAGE ===== */
  .test-type-card {
    background: var(--bg-card); border: 2px solid var(--border); border-radius: var(--r);
    padding: 22px 18px; margin-bottom: 10px; text-align: center; cursor: pointer;
    transition: all 0.2s;
  }
  .test-type-card:active { transform: scale(0.98); }
  .test-type-card.selected { border-color: var(--acc); background: var(--acc-soft); }
  .test-type-card .tt-icon { font-size: 1.4rem; font-weight: 700; color: var(--acc); margin-bottom: 8px; }
  .test-type-card .tt-title { font-size: 1rem; font-weight: 600; margin-bottom: 4px; }
  .test-type-card .tt-desc { font-size: 0.8rem; color: var(--t2); }

  .tq-label { font-size: 0.78rem; color: var(--t3); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; margin-bottom: 10px; }
  .tq-text { font-size: 1.6rem; font-weight: 700; color: var(--purple); line-height: 1.4; margin-bottom: 24px; min-height: 44px; }
  .tq-input {
    width: 100%; padding: 14px; font-size: 1.2rem; text-align: center;
    background: var(--bg-input); border: 2px solid var(--border); border-radius: var(--r);
    color: var(--t1); font-family: 'Inter', monospace; outline: none;
  }
  .tq-input:focus { border-color: var(--acc); }
  .tq-input.correct { border-color: var(--green); background: var(--green-bg); }
  .tq-input.wrong { border-color: var(--red); background: var(--red-bg); }
  .tq-reveal { margin-top: 14px; font-size: 0.95rem; min-height: 24px; }
  .tq-btn {
    width: 100%; padding: 14px; background: var(--acc); color: white; border: none;
    border-radius: var(--r-sm); font-size: 0.95rem; font-weight: 600; cursor: pointer;
    font-family: inherit; margin-top: 14px;
  }
  .tq-btn:active { transform: scale(0.98); }

  .choice-grid { display: flex; flex-direction: column; gap: 10px; }
  .ch-btn {
    padding: 16px; background: var(--bg-card); border: 2px solid var(--border);
    border-radius: var(--r); color: var(--t1); cursor: pointer; text-align: left;
    font-size: 0.92rem; line-height: 1.5; font-family: inherit; transition: all 0.15s;
  }
  .ch-btn:active { transform: scale(0.98); }
  .ch-btn .ch-num { color: var(--t3); font-size: 0.72rem; font-weight: 600; margin-right: 8px; }
  .ch-btn.ch-correct { border-color: var(--green); background: var(--green-bg); }
  .ch-btn.ch-wrong { border-color: var(--red); background: var(--red-bg); }
  .ch-btn.ch-dim { opacity: 0.35; }

  /* Score */
  .score-ring {
    width: 130px; height: 130px; border-radius: 50%; margin: 24px auto;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    border: 4px solid var(--acc); background: var(--bg-card);
    box-shadow: 0 0 30px var(--acc-glow);
  }
  .score-ring .s-num { font-size: 2.6rem; font-weight: 700; color: var(--acc); }
  .score-ring .s-lbl { font-size: 0.75rem; color: var(--t3); }
  .result-stats { display: flex; gap: 10px; margin: 20px 0; }
  .result-stats > div {
    flex: 1; background: var(--bg-card); padding: 16px; border-radius: var(--r);
    border: 1px solid var(--border); text-align: center;
  }
  .result-stats .rs-label { font-size: 0.7rem; color: var(--t3); text-transform: uppercase; letter-spacing: 0.3px; font-weight: 600; margin-bottom: 6px; }
  .result-stats .rs-val { font-size: 1.4rem; font-weight: 700; color: var(--acc); }
  .wrong-list { max-height: 300px; overflow-y: auto; }
  .wrong-list::-webkit-scrollbar { width: 4px; }
  .wrong-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
  .wl-item {
    background: var(--bg-card); border-radius: var(--r-sm); padding: 12px 14px;
    margin-bottom: 6px; border-left: 3px solid var(--red);
  }
  .wl-item .wl-word { color: var(--acc); font-weight: 600; font-size: 0.95rem; }
  .wl-item .wl-mean { color: var(--t2); font-size: 0.82rem; margin-top: 2px; }
  .wl-item .wl-typed { color: var(--red); font-size: 0.78rem; margin-top: 2px; }

  .empty-msg {
    text-align: center; padding: 60px 20px;
  }
  .empty-msg .em-icon { font-size: 2.5rem; margin-bottom: 12px; }
  .empty-msg .em-text { color: var(--amber); font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; }
  .empty-msg .em-sub { color: var(--t2); font-size: 0.88rem; }

  .fc { color: var(--green); } .fw { color: var(--red); } .fi { color: var(--acc); }
  .hidden { display: none !important; }
</style>
</head>
<body>

<!-- TOP BAR -->
<div class="topbar">
  <h1><span>TOEIC</span> 단어장</h1>
  <div class="topbar-right">
    <button class="topbar-btn" onclick="mOpenAdd()">+ 추가</button>
    <button class="topbar-btn" id="themeBtn" onclick="toggleTheme()">Dark</button>
  </div>
</div>

<!-- Add Word Modal -->
<!-- Dictionary Panel -->
<div id="dictOverlayM" onclick="if(event.target===this)closeDict()" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.6);z-index:999;justify-content:center;align-items:center;backdrop-filter:blur(4px);">
  <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r);padding:22px;width:92%;max-width:440px;max-height:80vh;overflow-y:auto;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
      <h3 id="dictWordM" style="font-size:1.3rem;font-weight:700;color:var(--acc);"></h3>
      <button onclick="closeDict()" style="background:var(--bg-el);border:1px solid var(--border);color:var(--t2);width:30px;height:30px;border-radius:50%;cursor:pointer;font-size:1rem;display:flex;align-items:center;justify-content:center;">&times;</button>
    </div>
    <div id="dictContentM"></div>
  </div>
</div>

<div id="addModal" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.6);z-index:1000;justify-content:center;align-items:center;backdrop-filter:blur(4px);">
  <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:var(--r);padding:24px;width:90%;max-width:400px;">
    <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:18px;">단어 추가</h3>
    <div style="margin-bottom:12px;"><label style="display:block;color:var(--t2);font-size:0.82rem;font-weight:500;margin-bottom:5px;">영단어</label><input type="text" id="maEng" style="width:100%;padding:10px 12px;background:var(--bg-input);border:1px solid var(--border);border-radius:var(--r-sm);color:var(--t1);font-size:0.95rem;font-family:inherit;" placeholder="예: accomplish" autocomplete="off"></div>
    <div style="margin-bottom:12px;"><label style="display:block;color:var(--t2);font-size:0.82rem;font-weight:500;margin-bottom:5px;">한국어 뜻</label><input type="text" id="maKor" style="width:100%;padding:10px 12px;background:var(--bg-input);border:1px solid var(--border);border-radius:var(--r-sm);color:var(--t1);font-size:0.95rem;font-family:inherit;" placeholder="예: (동)성취하다" autocomplete="off"></div>
    <div style="display:flex;gap:8px;margin-top:16px;">
      <button onclick="mCloseAdd()" style="flex:1;padding:10px;border-radius:var(--r-sm);background:var(--bg-el);color:var(--t2);border:1px solid var(--border);font-family:inherit;font-size:0.88rem;cursor:pointer;">취소</button>
      <button onclick="mSaveAdd()" style="flex:1;padding:10px;border-radius:var(--r-sm);background:var(--acc);color:white;border:none;font-family:inherit;font-size:0.88rem;font-weight:600;cursor:pointer;">추가</button>
    </div>
    <div id="maMsg" style="font-size:0.82rem;margin-top:10px;min-height:18px;"></div>
  </div>
</div>

<!-- STATS -->
<div class="stats-bar">
  <div class="stat-chip">전체 <b id="sTotal">0</b></div>
  <div class="stat-chip">학습완료 <b id="sLearned">0</b></div>
  <div class="stat-chip">진행도 <b id="sProgress">0</b>%</div>
  <div class="stat-chip">정확도 <b id="sAccuracy">0</b>%</div>
</div>

<!-- PAGE: WORD LIST -->
<div class="page active" id="pgList">
  <input type="text" class="search-input" id="mSearch" placeholder="단어 검색..." oninput="mRenderList()">
  <select class="range-select" id="mRange" onchange="mChangeRange()"></select>
  <div class="filter-row" id="mFilters"></div>
  <div id="mWordList"></div>
  <div class="pager" id="mPager"></div>
</div>

<!-- PAGE: LEARNING -->
<div class="page" id="pgLearn">
  <div id="learnSetup">
    <div class="learn-settings">
      <div class="ls-row"><label>반복 횟수</label><input type="number" id="mRepeat" value="3" min="1" max="20" style="width:65px;"></div>
      <div class="ls-row"><label>순서</label><select id="mOrder"><option value="sequential">순서대로</option><option value="random">랜덤</option></select></div>
      <div class="ls-row"><label>뜻 표시</label><select id="mMeaning"><option value="always">항상</option><option value="before">처음만</option><option value="hidden">숨기기</option></select></div>
      <div class="ls-row"><label>카테고리</label><select id="mLearnCat" onchange="mUpdateLearnInfo()"><option value="all">전체</option><option value="none">미학습</option><option value="learned">학습완료</option><option value="confused">헷갈림</option></select></div>
      <div class="ls-row"><label></label><span style="color:var(--t2);font-size:0.82rem;" id="mLearnInfo"></span></div>
    </div>
    <button class="start-btn" onclick="mStartLearn()">학습 시작</button>
  </div>
  <div id="learnCard" class="hidden">
    <div class="learn-card">
      <div class="lc-progress"><span class="lc-ptext" id="lcLeft"></span><div class="lc-pbar"><div class="lc-pfill" id="lcBar"></div></div><span class="lc-ptext" id="lcRight"></span></div>
      <div class="lc-meaning" id="lcMeaning"></div>
      <div class="lc-word" id="lcWord"></div>
      <div class="lc-repeat" id="lcRepeat"></div>
      <div class="lc-chars" id="lcChars"></div>
      <input type="text" class="lc-input" id="lcInput" autocomplete="off" spellcheck="false" placeholder="타이핑하세요">
      <div class="lc-feedback" id="lcFeedback"></div>
      <div class="lc-btns">
        <button onclick="mSkipWord()">건너뛰기</button>
        <button class="primary" onclick="mResetLearn()">다시 시작</button>
      </div>
    </div>
  </div>
  <div id="learnDone" class="hidden" style="text-align:center;padding:40px 0;">
    <h2 style="color:var(--green);font-size:1.5rem;margin-bottom:20px;">학습 완료!</h2>
    <div class="result-stats">
      <div><div class="rs-label">단어</div><div class="rs-val" id="ldWords">0</div></div>
      <div><div class="rs-label">정확도</div><div class="rs-val" id="ldAcc">0%</div></div>
      <div><div class="rs-label">시간</div><div class="rs-val" id="ldTime">0:00</div></div>
    </div>
    <button class="start-btn" onclick="mResetLearn()" style="margin-top:16px;">다시 학습</button>
  </div>
</div>

<!-- PAGE: TEST -->
<div class="page" id="pgTest">
  <div id="testSetupM">
    <h2 style="text-align:center;font-size:1.3rem;font-weight:700;margin-bottom:20px;">단어 테스트</h2>
    <div class="test-type-card" id="ttKE" onclick="mSelectTestType('kor-to-eng')">
      <div class="tt-icon">KR &rarr; EN</div>
      <div class="tt-title">한국어 &rarr; 영어</div>
      <div class="tt-desc">뜻을 보고 영단어 입력</div>
    </div>
    <div class="test-type-card" id="ttEK" onclick="mSelectTestType('eng-to-kor')">
      <div class="tt-icon">EN &rarr; KR</div>
      <div class="tt-title">영어 &rarr; 한국어</div>
      <div class="tt-desc">영단어를 보고 뜻 고르기 (4지선다)</div>
    </div>
    <div class="learn-settings" style="margin-top:16px;">
      <div class="ls-row"><label>문제 수</label><select id="mTestCount"><option value="10">10</option><option value="20" selected>20</option><option value="30">30</option><option value="50">50</option><option value="all">전체</option></select></div>
      <div class="ls-row"><label>카테고리</label><select id="mTestCat" onchange="mUpdateTestInfo()"><option value="all">전체</option><option value="none">미학습</option><option value="learned">학습완료</option><option value="confused">헷갈림</option></select></div>
      <div class="ls-row"><label></label><span style="color:var(--t2);font-size:0.82rem;" id="mTestInfo"></span></div>
    </div>
    <button class="start-btn" id="mTestStartBtn" onclick="mStartTest()" disabled style="margin-top:12px;">테스트 시작</button>
  </div>
  <div id="testAreaM" class="hidden" style="padding-top:8px;">
    <div class="lc-progress"><span class="lc-ptext" id="tqLeft"></span><div class="lc-pbar"><div class="lc-pfill" id="tqBar"></div></div><span class="lc-ptext" id="tqRight"></span></div>
    <div class="tq-label" id="tqLabel"></div>
    <div class="tq-text" id="tqText"></div>
    <div id="tqTypingArea"><input type="text" class="tq-input" id="tqInput" autocomplete="off" spellcheck="false" placeholder="정답 입력"></div>
    <div id="tqChoiceArea" class="hidden"></div>
    <div class="tq-reveal" id="tqReveal"></div>
    <button class="tq-btn" id="tqSubmit" onclick="mSubmitTest()">확인</button>
    <button class="tq-btn hidden" id="tqNext" onclick="mNextTest()">다음 문제</button>
  </div>
  <div id="testResultM" class="hidden" style="padding-top:8px;">
    <h2 id="trTitle" style="text-align:center;font-size:1.4rem;font-weight:700;margin-bottom:4px;">결과</h2>
    <div class="score-ring"><div class="s-num" id="trScore">0</div><div class="s-lbl" id="trTotal">/ 0</div></div>
    <div class="result-stats">
      <div><div class="rs-label">정답률</div><div class="rs-val" id="trAcc">0%</div></div>
      <div><div class="rs-label">시간</div><div class="rs-val" id="trTime">0:00</div></div>
    </div>
    <h3 style="color:var(--t2);font-size:0.9rem;margin:16px 0 8px;text-align:center;">오답 목록</h3>
    <div class="wrong-list" id="trWrong"></div>
    <button class="tq-btn" id="trRetestBtn" onclick="mRetestWrong()" style="margin-top:12px;">오답만 다시</button>
    <button class="tq-btn" onclick="mShowTestSetup()" style="background:var(--bg-el);color:var(--t2);margin-top:8px;">다시 테스트</button>
  </div>
</div>

<!-- BOTTOM NAV -->
<div class="bottom-nav">
  <button class="nav-item active" onclick="mNav('list')" id="navList">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    단어목록
  </button>
  <button class="nav-item" onclick="mNav('learn')" id="navLearn">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25"/></svg>
    학습
  </button>
  <button class="nav-item" onclick="mNav('test')" id="navTest">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4m6 2a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg>
    테스트
  </button>
</div>

<script>
"""

html_js = """
/* ===== STATE ===== */
var mCatFilter = 'all', mPage = 1, PS = 30;
var mRange = [0, W.length];
var mFiltered = W.slice();

var ws = {};
try { var sv = localStorage.getItem('toeic_word_status'); if(sv) ws = JSON.parse(sv); } catch(e){}
function saveWs() { try{localStorage.setItem('toeic_word_status',JSON.stringify(ws));}catch(e){} }
function getWs(w) { return ws[w]||'none'; }
function cycleWs(w) {
  var c = getWs(w);
  if(c==='none') ws[w]='learned'; else if(c==='learned') ws[w]='confused'; else delete ws[w];
  saveWs(); updateStats();
}

function updateStats() {
  var l=0,c=0;
  for(var i=0;i<W.length;i++){var s=getWs(W[i].word);if(s==='learned')l++;else if(s==='confused')c++;}
  document.getElementById('sTotal').textContent=W.length;
  document.getElementById('sLearned').textContent=l;
  document.getElementById('sProgress').textContent=W.length>0?Math.round(l/W.length*100):0;
  var t=l+c; document.getElementById('sAccuracy').textContent=t>0?Math.round(l/t*100):0;
}

/* ===== THEME ===== */
function toggleTheme(){
  var light=document.body.classList.toggle('light');
  document.getElementById('themeBtn').textContent=light?'Light':'Dark';
  document.querySelector('meta[name=theme-color]').content=light?'#f5f6fa':'#0c0f1a';
  try{localStorage.setItem('toeic_theme',light?'light':'dark');}catch(e){}
}
(function(){try{if(localStorage.getItem('toeic_theme')==='light'){document.body.classList.add('light');document.getElementById('themeBtn').textContent='Light';document.querySelector('meta[name=theme-color]').content='#f5f6fa';}}catch(e){}})();

/* ===== NAV ===== */
function mNav(pg){
  ['list','learn','test'].forEach(function(p){
    document.getElementById('pg'+p.charAt(0).toUpperCase()+p.slice(1)).classList.toggle('active',p===pg);
    document.getElementById('nav'+p.charAt(0).toUpperCase()+p.slice(1)).classList.toggle('active',p===pg);
  });
  if(pg==='learn') mUpdateLearnInfo();
  if(pg==='test'){ mShowTestSetup(); mUpdateTestInfo(); }
}

/* ===== WORD LIST ===== */
function initRanges(){
  var sel=document.getElementById('mRange');
  sel.innerHTML='<option value="all">전체 (1-'+W.length+')</option>';
  for(var i=0;i<W.length;i+=50){
    var e=Math.min(i+50,W.length);
    sel.innerHTML+='<option value="'+i+'-'+e+'">'+(i+1)+' - '+e+'번</option>';
  }
}
function mChangeRange(){
  var v=document.getElementById('mRange').value;
  if(v==='all') mRange=[0,W.length]; else {var p=v.split('-');mRange=[+p[0],+p[1]];}
  mFiltered=W.slice(mRange[0],mRange[1]); mPage=1; mRenderList();
}
function getDisplayW(){
  var s=document.getElementById('mSearch').value.toLowerCase();
  var base=s?W.filter(function(w){return w.word.toLowerCase().includes(s)||w.meaning.includes(s);}):mFiltered;
  if(mCatFilter!=='all') return base.filter(function(w){return getWs(w.word)===mCatFilter;});
  return base;
}
function mRenderFilters(){
  var words=mFiltered, s=document.getElementById('mSearch').value.toLowerCase();
  if(s) words=W.filter(function(w){return w.word.toLowerCase().includes(s)||w.meaning.includes(s);});
  var cn=0,cl=0,cc=0;
  for(var i=0;i<words.length;i++){var st=getWs(words[i].word);if(st==='learned')cl++;else if(st==='confused')cc++;else cn++;}
  var cats=[['all','전체',words.length],['none','미학습',cn],['learned','학습완료',cl],['confused','헷갈림',cc]];
  var h='';
  cats.forEach(function(c){h+='<button class="filter-btn'+(mCatFilter===c[0]?' active':'')+'" onclick="mSetCat(this,&apos;'+c[0]+'&apos;)">'+c[1]+' <span style="color:var(--t3);font-size:0.7rem;">('+c[2]+')</span></button>';});
  h+='<span style="color:var(--t3);font-size:0.68rem;white-space:nowrap;">1tap=완료 2tap=헷갈림 3tap=초기화</span>';
  document.getElementById('mFilters').innerHTML=h;
}
function mSetCat(el,cat){mCatFilter=cat;mPage=1;mRenderList();}
function mRenderList(){
  var dw=getDisplayW(), tp=Math.ceil(dw.length/PS)||1;
  if(mPage>tp)mPage=tp;
  var start=(mPage-1)*PS, pw=dw.slice(start,start+PS);
  var h='';
  pw.forEach(function(w){
    var gi=W.indexOf(w)+1, st=getWs(w.word);
    var sc=st!=='none'?' st-'+st:'';
    var badge='';
    if(st==='learned') badge='<span class="w-badge">완료</span>';
    else if(st==='confused') badge='<span class="w-badge">헷갈림</span>';
    h+='<div class="wcard'+sc+'" data-w="'+w.word+'">'+badge+'<span class="w-num">'+gi+'</span><div class="w-eng">'+w.word+' <button class="spk-btn" onclick="event.stopPropagation();speak(&apos;'+w.word+'&apos;)">&#9654;</button> <button class="spk-btn" onclick="event.stopPropagation();openDict(&apos;'+w.word+'&apos;)" style="font-size:0.6rem;">&#128214;</button></div><div class="w-kor">'+w.meaning+'</div></div>';
  });
  document.getElementById('mWordList').innerHTML=h;
  mRenderFilters();
  // Pager
  var ph='';
  if(tp>1){
    ph+='<button onclick="mGoPage('+(mPage-1)+')" '+(mPage===1?'disabled':'')+'>&#8249;</button>';
    var s=Math.max(1,mPage-2),e=Math.min(tp,mPage+2);
    for(var p=s;p<=e;p++) ph+='<button onclick="mGoPage('+p+')" class="'+(p===mPage?'active':'')+'">'+p+'</button>';
    ph+='<button onclick="mGoPage('+(mPage+1)+')" '+(mPage===tp?'disabled':'')+'>&#8250;</button>';
    ph+='<span class="pg-info">'+mPage+'/'+tp+'</span>';
  }
  document.getElementById('mPager').innerHTML=ph;
}
function mGoPage(p){var tp=Math.ceil(getDisplayW().length/PS)||1;if(p<1||p>tp)return;mPage=p;mRenderList();window.scrollTo({top:0,behavior:'smooth'});}
document.getElementById('mWordList').addEventListener('click',function(e){
  var card=e.target.closest('.wcard');if(!card)return;
  cycleWs(card.getAttribute('data-w')); mRenderList();
});

/* ===== LEARNING ===== */
var lWords=[],lIdx=0,lRep=0,lTotal=0,lCorrect=0,lStart=null;
function mUpdateLearnInfo(){
  var cat=document.getElementById('mLearnCat').value;
  var pool=cat==='all'?mFiltered:mFiltered.filter(function(w){return getWs(w.word)===cat;});
  document.getElementById('mLearnInfo').textContent=pool.length+'개';
}
function mStartLearn(){
  var cat=document.getElementById('mLearnCat').value;
  var pool=cat==='all'?mFiltered:mFiltered.filter(function(w){return getWs(w.word)===cat;});
  if(pool.length===0){
    document.getElementById('learnSetup').innerHTML='<div class="empty-msg"><div class="em-icon">!</div><div class="em-text">단어가 없습니다</div><div class="em-sub">다른 카테고리를 선택해주세요</div></div>';
    return;
  }
  lWords=pool.slice();
  if(document.getElementById('mOrder').value==='random'){for(var i=lWords.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=lWords[i];lWords[i]=lWords[j];lWords[j]=t;}}
  lIdx=0;lRep=0;lTotal=0;lCorrect=0;lStart=Date.now();
  document.getElementById('learnSetup').classList.add('hidden');
  document.getElementById('learnDone').classList.add('hidden');
  document.getElementById('learnCard').classList.remove('hidden');
  mShowLearnWord();
}
function mResetLearn(){
  document.getElementById('learnCard').classList.add('hidden');
  document.getElementById('learnDone').classList.add('hidden');
  document.getElementById('learnSetup').classList.remove('hidden');
  // Restore setup if emptied
  if(!document.getElementById('mLearnCat')){location.reload();}
  mUpdateLearnInfo();
}
function mShowLearnWord(){
  if(lIdx>=lWords.length){mShowLearnDone();return;}
  var w=lWords[lIdx], rm=+document.getElementById('mRepeat').value||3;
  var mm=document.getElementById('mMeaning').value;
  document.getElementById('lcWord').textContent=w.word;
  document.getElementById('lcMeaning').textContent=(mm==='always'||(mm==='before'&&lRep===0))?w.meaning:'';
  document.getElementById('lcRepeat').textContent=(lRep+1)+' / '+rm+' 회';
  var total=lWords.length*rm, done=lIdx*rm+lRep, pct=Math.round(done/total*100);
  document.getElementById('lcLeft').textContent=(lIdx+1)+'/'+lWords.length;
  document.getElementById('lcBar').style.width=pct+'%';
  document.getElementById('lcRight').textContent=pct+'%';
  mRenderChars(w.word,'');
  var inp=document.getElementById('lcInput');inp.value='';inp.className='lc-input';inp.focus();
  document.getElementById('lcFeedback').innerHTML='';
}
function mRenderChars(target,typed){
  var h='';
  for(var i=0;i<target.length;i++){
    var cls='lc-char';
    if(i<typed.length) cls+=typed[i].toLowerCase()===target[i].toLowerCase()?' correct filled':' wrong filled';
    else if(i===typed.length) cls+=' current';
    h+='<div class="'+cls+'">'+(i<typed.length?typed[i]:target[i])+'</div>';
  }
  document.getElementById('lcChars').innerHTML=h;
}
document.getElementById('lcInput').addEventListener('input',function(){
  var w=lWords[lIdx];if(!w)return;
  mRenderChars(w.word,this.value);
  if(this.value.length===w.word.length){
    lTotal++;
    if(this.value.toLowerCase()===w.word.toLowerCase()){
      lCorrect++;this.className='lc-input correct';
      document.getElementById('lcFeedback').innerHTML='<span class="fc">정답!</span>';
      var rm=+document.getElementById('mRepeat').value||3;lRep++;
      if(lRep>=rm){lRep=0;lIdx++;}
      setTimeout(mShowLearnWord,400);
    } else {
      this.className='lc-input wrong';
      document.getElementById('lcFeedback').innerHTML='<span class="fw">오답! 정답: <b>'+w.word+'</b></span>';
    }
  } else { this.className='lc-input'; document.getElementById('lcFeedback').innerHTML=''; }
});
document.getElementById('lcInput').addEventListener('keydown',function(e){
  if(e.key==='Enter'){
    if(this.className.includes('wrong')){this.value='';this.className='lc-input';document.getElementById('lcFeedback').innerHTML='<span class="fi">다시 입력</span>';mRenderChars(lWords[lIdx].word,'');}
    else if(this.className.includes('correct')) mShowLearnWord();
  }
});
function mSkipWord(){lRep=0;lIdx++;mShowLearnWord();}
function mShowLearnDone(){
  document.getElementById('learnCard').classList.add('hidden');
  document.getElementById('learnDone').classList.remove('hidden');
  document.getElementById('ldWords').textContent=lWords.length;
  document.getElementById('ldAcc').textContent=(lTotal>0?Math.round(lCorrect/lTotal*100):0)+'%';
  var el=Math.round((Date.now()-lStart)/1000);
  document.getElementById('ldTime').textContent=Math.floor(el/60)+':'+String(el%60).padStart(2,'0');
}

/* ===== TEST ===== */
var tType='',tQs=[],tIdx=0,tResults=[],tStart=null,tAnswered=false,tSynRetry=false,tChoices=[];
function mSelectTestType(t){
  tType=t;
  document.getElementById('ttKE').classList.toggle('selected',t==='kor-to-eng');
  document.getElementById('ttEK').classList.toggle('selected',t==='eng-to-kor');
  document.getElementById('mTestStartBtn').disabled=false;
}
function mUpdateTestInfo(){
  var cat=document.getElementById('mTestCat').value;
  var pool=cat==='all'?mFiltered:mFiltered.filter(function(w){return getWs(w.word)===cat;});
  document.getElementById('mTestInfo').textContent=pool.length+'개에서 출제';
}
function mShowTestSetup(){
  document.getElementById('testSetupM').classList.remove('hidden');
  document.getElementById('testAreaM').classList.add('hidden');
  document.getElementById('testResultM').classList.add('hidden');
  tType='';document.getElementById('ttKE').classList.remove('selected');
  document.getElementById('ttEK').classList.remove('selected');
  document.getElementById('mTestStartBtn').disabled=true;
  mUpdateTestInfo();
}
function shuffle(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;}
function mStartTest(custom){
  var cat=document.getElementById('mTestCat').value;
  var pool=custom||(cat==='all'?mFiltered:mFiltered.filter(function(w){return getWs(w.word)===cat;}));
  if(pool.length===0){document.getElementById('testSetupM').innerHTML='<div class="empty-msg"><div class="em-icon">!</div><div class="em-text">단어가 없습니다</div><div class="em-sub">다른 카테고리를 선택해주세요</div></div>';return;}
  var cvEl=document.getElementById('mTestCount');
  var cv=cvEl?cvEl.value:'all';
  var cnt=cv==='all'?pool.length:Math.min(+cv,pool.length);
  tQs=shuffle(pool).slice(0,cnt);tIdx=0;tResults=[];tStart=Date.now();tAnswered=false;tSynRetry=false;
  document.getElementById('testSetupM').classList.add('hidden');
  document.getElementById('testAreaM').classList.remove('hidden');
  document.getElementById('testResultM').classList.add('hidden');
  mShowTestQ();
}
function genChoices(w){
  var ch=[w],pool=shuffle(W);
  for(var i=0;i<pool.length&&ch.length<4;i++){if(pool[i].word!==w.word)ch.push(pool[i]);}
  return shuffle(ch);
}
function mShowTestQ(){
  tSynRetry=false;
  if(tIdx>=tQs.length){mShowTestResult();return;}
  tAnswered=false;
  var w=tQs[tIdx],pct=Math.round(tIdx/tQs.length*100);
  document.getElementById('tqLeft').textContent=(tIdx+1)+'/'+tQs.length;
  document.getElementById('tqBar').style.width=pct+'%';
  document.getElementById('tqRight').textContent=pct+'%';
  document.getElementById('tqReveal').innerHTML='';
  document.getElementById('tqNext').classList.add('hidden');
  document.getElementById('tqSubmit').classList.remove('hidden');
  if(tType==='kor-to-eng'){
    document.getElementById('tqLabel').textContent='뜻에 해당하는 영단어를 입력하세요';
    document.getElementById('tqText').textContent=w.meaning;
    document.getElementById('tqTypingArea').classList.remove('hidden');
    document.getElementById('tqChoiceArea').classList.add('hidden');
    var inp=document.getElementById('tqInput');inp.value='';inp.className='tq-input';inp.focus();
  } else {
    document.getElementById('tqLabel').textContent='영단어의 뜻을 고르세요';
    document.getElementById('tqText').textContent=w.word;
    document.getElementById('tqTypingArea').classList.add('hidden');
    document.getElementById('tqChoiceArea').classList.remove('hidden');
    document.getElementById('tqSubmit').classList.add('hidden');
    tChoices=genChoices(w);
    var h='<div class="choice-grid">';
    for(var i=0;i<tChoices.length;i++) h+='<button class="ch-btn" onclick="mSelectChoice('+i+')"><span class="ch-num">'+(i+1)+'</span>'+tChoices[i].meaning+'</button>';
    h+='</div>';
    document.getElementById('tqChoiceArea').innerHTML=h;
  }
}
function mSelectChoice(idx){
  if(tAnswered)return; tAnswered=true;
  var w=tQs[tIdx],sel=tChoices[idx],ok=sel.word===w.word;
  tResults.push({word:w,typed:sel.meaning,correct:ok});
  var btns=document.getElementById('tqChoiceArea').querySelectorAll('.ch-btn');
  for(var i=0;i<btns.length;i++){
    if(tChoices[i].word===w.word) btns[i].classList.add('ch-correct');
    else if(i===idx) btns[i].classList.add('ch-wrong');
    else btns[i].classList.add('ch-dim');
    btns[i].style.pointerEvents='none';
  }
  document.getElementById('tqReveal').innerHTML=ok?'<span class="fc">정답!</span>':'<span class="fw">오답!</span> 정답: <b style="color:var(--acc);">'+w.word+'</b>';
  document.getElementById('tqNext').classList.remove('hidden');
}
function isSyn(typed,target){
  if(tType!=='kor-to-eng')return false;
  var tl=typed.toLowerCase();
  for(var i=0;i<W.length;i++){
    if(W[i].word.toLowerCase()===tl&&W[i].word.toLowerCase()!==target.word.toLowerCase()){
      var gk=function(m){return m.replace(/\\([^)]*\\)/g,' ').replace(/,/g,' ').split(/\\s+/).filter(function(s){return s.length>=2;});};
      var k1=gk(W[i].meaning),k2=gk(target.meaning);
      for(var a=0;a<k1.length;a++) for(var b=0;b<k2.length;b++) if(k1[a].includes(k2[b])||k2[b].includes(k1[a])) return true;
    }
  }
  return false;
}
function mShowHint(){
  var w=tQs[tIdx];
  document.getElementById('tqHintArea').innerHTML='<span style="color:var(--acc);font-size:1.15rem;letter-spacing:3px;font-weight:700;">'+w.word[0]+'_'.repeat(w.word.length-1)+'</span> <span style="color:var(--t3);">('+w.word.length+'글자)</span>';
}
function mSubmitTest(){
  if(tAnswered)return;
  var w=tQs[tIdx],inp=document.getElementById('tqInput'),typed=inp.value.trim(),ok=false;
  if(tType==='kor-to-eng') ok=typed.toLowerCase()===w.word.toLowerCase();
  if(!ok&&tType==='kor-to-eng'&&!tSynRetry&&isSyn(typed,w)){
    tSynRetry=true; inp.style.borderColor='var(--amber)';
    document.getElementById('tqReveal').innerHTML='<div style="color:var(--amber);margin-bottom:6px;">의미는 맞지만, 다른 단어가 있습니다!</div><div id="tqHintArea"></div><button class="tq-btn" style="margin-top:8px;padding:8px 20px;font-size:0.82rem;background:var(--bg-el);color:var(--t2);" onclick="mShowHint()">힌트 보기</button>';
    inp.value='';inp.focus();return;
  }
  tAnswered=true;tSynRetry=false;
  tResults.push({word:w,typed:typed,correct:ok});
  if(ok){inp.className='tq-input correct';document.getElementById('tqReveal').innerHTML='<span class="fc">정답!</span>';}
  else{inp.className='tq-input wrong';document.getElementById('tqReveal').innerHTML='<span class="fw">오답</span><br><b style="color:var(--acc);">'+w.word+'</b> <span style="color:var(--t2);">'+w.meaning+'</span>';}
  document.getElementById('tqSubmit').classList.add('hidden');
  document.getElementById('tqNext').classList.remove('hidden');
}
function mNextTest(){tIdx++;mShowTestQ();}
document.getElementById('tqInput').addEventListener('keydown',function(e){
  if(e.key==='Enter'){if(!tAnswered)mSubmitTest();else mNextTest();}
});
function mShowTestResult(){
  document.getElementById('testAreaM').classList.add('hidden');
  document.getElementById('testResultM').classList.remove('hidden');
  var cc=tResults.filter(function(r){return r.correct;}).length,tot=tResults.length;
  var pct=tot>0?Math.round(cc/tot*100):0;
  document.getElementById('trScore').textContent=cc;
  document.getElementById('trTotal').textContent='/'+tot;
  document.getElementById('trAcc').textContent=pct+'%';
  var ring=document.querySelector('.score-ring');
  if(pct>=90){ring.style.borderColor='var(--green)';document.getElementById('trScore').style.color='var(--green)';document.getElementById('trTitle').textContent='훌륭합니다!';}
  else if(pct>=70){ring.style.borderColor='var(--acc)';document.getElementById('trScore').style.color='var(--acc)';document.getElementById('trTitle').textContent='잘했습니다!';}
  else if(pct>=50){ring.style.borderColor='var(--amber)';document.getElementById('trScore').style.color='var(--amber)';document.getElementById('trTitle').textContent='조금 더 노력!';}
  else{ring.style.borderColor='var(--red)';document.getElementById('trScore').style.color='var(--red)';document.getElementById('trTitle').textContent='다시 복습해봐요';}
  var el=Math.round((Date.now()-tStart)/1000);
  document.getElementById('trTime').textContent=Math.floor(el/60)+':'+String(el%60).padStart(2,'0');
  var wrongs=tResults.filter(function(r){return!r.correct;});
  if(wrongs.length===0){document.getElementById('trWrong').innerHTML='<div style="text-align:center;color:var(--green);padding:16px;">오답 없음!</div>';document.getElementById('trRetestBtn').classList.add('hidden');}
  else{
    document.getElementById('trRetestBtn').classList.remove('hidden');
    var h='';wrongs.forEach(function(r){h+='<div class="wl-item"><div class="wl-word">'+r.word.word+'</div><div class="wl-mean">'+r.word.meaning+'</div><div class="wl-typed">입력: '+(r.typed||'(없음)')+'</div></div>';});
    document.getElementById('trWrong').innerHTML=h;
  }
}
function mRetestWrong(){
  var ww=tResults.filter(function(r){return!r.correct;}).map(function(r){return r.word;});
  if(ww.length===0)return;mStartTest(ww);
}
// Keyboard 1-4 for choices
document.addEventListener('keydown',function(e){
  if(tType!=='eng-to-kor')return;
  if(e.key>='1'&&e.key<='4'&&!tAnswered) mSelectChoice(+e.key-1);
  else if(e.key==='Enter'&&tAnswered) mNextTest();
});

/* ===== DICTIONARY ===== */
var posMap={noun:'명사',verb:'동사',adjective:'형용사',adverb:'부사',preposition:'전치사',conjunction:'접속사',interjection:'감탄사',pronoun:'대명사'};
function trText(t){return fetch('https://api.mymemory.translated.net/get?q='+encodeURIComponent(t)+'&langpair=en|ko').then(function(r){return r.json();}).then(function(d){return(d.responseData&&d.responseData.translatedText)||t;}).catch(function(){return t;});}
function openDict(word){
  var ov=document.getElementById('dictOverlayM');ov.style.display='flex';
  document.getElementById('dictWordM').textContent=word;
  document.getElementById('dictContentM').innerHTML='<div style="text-align:center;color:var(--t3);padding:24px;">번역하는 중...</div>';
  fetch('https://api.dictionaryapi.dev/api/v2/entries/en/'+encodeURIComponent(word))
    .then(function(r){return r.json();})
    .then(function(data){
      if(!Array.isArray(data)||data.length===0)throw new Error('x');
      var e=data[0];
      var ph=e.phonetic||'';if(!ph&&e.phonetics)for(var p=0;p<e.phonetics.length;p++){if(e.phonetics[p].text){ph=e.phonetics[p].text;break;}}
      var items=[];
      if(e.meanings)for(var m=0;m<e.meanings.length;m++){
        var mg=e.meanings[m],ds=mg.definitions||[];
        for(var d=0;d<Math.min(ds.length,3);d++) items.push({pos:mg.partOfSpeech,def:ds[d].definition,example:ds[d].example||''});
      }
      return Promise.all(items.map(function(it){return trText(it.def).then(function(tr){it.defKo=tr;return it;});})).then(function(){
        var html='';
        if(ph) html+='<div style="color:var(--t3);font-size:0.85rem;font-style:italic;margin-bottom:14px;">'+ph+'</div>';
        var lastPos='';
        for(var i=0;i<items.length;i++){
          if(items[i].pos!==lastPos){lastPos=items[i].pos;html+='<div style="color:var(--acc);font-weight:600;font-size:0.88rem;margin-top:12px;margin-bottom:5px;font-style:italic;">'+(posMap[lastPos]||lastPos)+' ('+lastPos+')</div>';}
          html+='<div style="color:var(--t1);font-size:0.88rem;margin-bottom:3px;padding-left:10px;border-left:2px solid var(--border);line-height:1.6;">'+items[i].defKo+'</div>';
          html+='<div style="color:var(--t3);font-size:0.78rem;margin:2px 0 6px 10px;">'+items[i].def+'</div>';
          if(items[i].example) html+='<div style="color:var(--t3);font-size:0.8rem;font-style:italic;margin:3px 0 7px 10px;">&ldquo;'+items[i].example+'&rdquo;</div>';
        }
        html+='<div style="color:var(--t3);font-size:0.68rem;margin-top:14px;text-align:right;">Source: dictionaryapi.dev + mymemory</div>';
        document.getElementById('dictContentM').innerHTML=html;
      });
    })
    .catch(function(){document.getElementById('dictContentM').innerHTML='<div style="text-align:center;color:var(--red);padding:16px;">사전 데이터를 찾을 수 없습니다.</div>';});
}
function closeDict(){document.getElementById('dictOverlayM').style.display='none';}

/* ===== TTS ===== */
function speak(word){try{if(!window.speechSynthesis)return;window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(word);u.lang='en-US';u.rate=0.9;window.speechSynthesis.speak(u);}catch(e){}}

/* ===== ADD WORD ===== */
function mOpenAdd(){
  document.getElementById('addModal').style.display='flex';
  document.getElementById('maEng').value='';document.getElementById('maKor').value='';
  document.getElementById('maMsg').innerHTML='';document.getElementById('maEng').focus();
}
function mCloseAdd(){document.getElementById('addModal').style.display='none';}
function mSaveAdd(){
  var eng=document.getElementById('maEng').value.trim(),kor=document.getElementById('maKor').value.trim();
  if(!eng||!kor){document.getElementById('maMsg').innerHTML='<span style="color:var(--red);">모두 입력하세요</span>';return;}
  if(W.some(function(w){return w.word.toLowerCase()===eng.toLowerCase();})){document.getElementById('maMsg').innerHTML='<span style="color:var(--amber);">이미 존재하는 단어</span>';return;}
  var nw={word:eng,meaning:kor};W.push(nw);
  try{var cw=localStorage.getItem('toeic_custom_words');var arr=cw?JSON.parse(cw):[];arr.push(nw);localStorage.setItem('toeic_custom_words',JSON.stringify(arr));}catch(e){}
  mFiltered=W.slice(mRange[0],mRange[1]);
  document.getElementById('maMsg').innerHTML='<span style="color:var(--green);"><b>'+eng+'</b> 추가!</span>';
  document.getElementById('maEng').value='';document.getElementById('maKor').value='';document.getElementById('maEng').focus();
  mRenderList();updateStats();
}
document.getElementById('maKor').addEventListener('keydown',function(e){if(e.key==='Enter')mSaveAdd();});
document.getElementById('addModal').addEventListener('click',function(e){if(e.target===this)mCloseAdd();});
function loadCustomWords(){
  try{var cw=localStorage.getItem('toeic_custom_words');if(cw){var arr=JSON.parse(cw);arr.forEach(function(w){if(!W.some(function(aw){return aw.word.toLowerCase()===w.word.toLowerCase();}))W.push(w);});}}catch(e){}
}

/* ===== INIT ===== */
loadCustomWords(); initRanges(); mRenderList(); updateStats();
</script>
<footer style="text-align:center;padding:24px 16px calc(80px + var(--safe-b));color:var(--t3);font-size:0.7rem;line-height:1.6;">
  <div style="margin-bottom:4px;">Made by <strong style="color:var(--t2);">김찬희 (Kim Chanhee)</strong> &copy; 2026</div>
  <div>단어 데이터 출처: dokjongban.com &middot; MIT License</div>
</footer>
</body>
</html>
"""

full = html_top + "var W = " + words_json + ";\n" + html_js

with open(r"C:\Users\chan7\toeic words\toeic-mobile.html", "w", encoding="utf-8") as f:
    f.write(full)

print(f"Created: C:\\Users\\chan7\\toeic-mobile.html")
print(f"Total words: {len(words)}")
print(f"File size: {len(full)} bytes")
