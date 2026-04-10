/**
 * AX(접근성) 검사 스크립트 - Node.js 기반 (방법 A)
 * pa11y (puppeteer 기반)를 사용하여 실제 브라우저 렌더링 기반 검사
 *
 * 사용법: node ax_check_node.js
 */

const pa11y = require("pa11y");
const path = require("path");
const http = require("http");
const fs = require("fs");

// index.html은 리다이렉트 전용이므로 제외
const TARGET_FILES = [
  "toeic-typing.html",
  "toeic-mobile.html",
  "toeic-ios.html",
];

const PORT = 8765;
const BASE_DIR = __dirname;

// ── 정적 파일 서버 ──
function startServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let filePath = path.join(BASE_DIR, req.url === "/" ? "index.html" : req.url.split("?")[0]);
      const ext = path.extname(filePath);
      const mimeTypes = {
        ".html": "text/html; charset=utf-8",
        ".css": "text/css",
        ".js": "application/javascript",
        ".json": "application/json",
      };

      fs.readFile(filePath, (err, data) => {
        if (err) {
          res.writeHead(404);
          res.end("Not Found");
        } else {
          res.writeHead(200, { "Content-Type": mimeTypes[ext] || "text/plain" });
          res.end(data);
        }
      });
    });

    server.listen(PORT, () => {
      console.log(`  Server: http://localhost:${PORT}\n`);
      resolve(server);
    });
  });
}

// ── 메인 ──
async function main() {
  console.log("=".repeat(60));
  console.log("  AX Audit - pa11y (WCAG 2.0 AA / Browser Rendering)");
  console.log("=".repeat(60));

  const server = await startServer();

  let totalErrors = 0;
  let totalWarnings = 0;
  let totalNotices = 0;

  for (const file of TARGET_FILES) {
    const filePath = path.join(BASE_DIR, file);
    if (!fs.existsSync(filePath)) {
      console.log(`  ${file} -- not found, skip`);
      continue;
    }

    const url = `http://localhost:${PORT}/${file}`;
    console.log("-".repeat(50));
    console.log(`  ${file}`);
    console.log("-".repeat(50));

    try {
      const results = await pa11y(url, {
        standard: "WCAG2AA",
        timeout: 30000,
        wait: 1000,
        chromeLaunchConfig: {
          args: ["--no-sandbox", "--disable-setuid-sandbox"],
        },
      });

      if (!results.issues || results.issues.length === 0) {
        console.log("  [OK] No issues found!\n");
        continue;
      }

      for (const issue of results.issues) {
        const type = issue.type;
        const icon = type === "error" ? "X" : type === "warning" ? "!" : "i";

        if (type === "error") totalErrors++;
        else if (type === "warning") totalWarnings++;
        else totalNotices++;

        console.log(`  [${icon}] ${issue.message}`);
        if (issue.selector) console.log(`      -> ${issue.selector}`);
        if (issue.code) console.log(`      rule: ${issue.code}`);
        console.log();
      }
    } catch (e) {
      console.log(`  [!] Error: ${e.message}\n`);
    }
  }

  server.close();

  console.log("=".repeat(60));
  console.log("  Summary (pa11y)");
  console.log("=".repeat(60));
  console.log(`  [X] Errors:   ${totalErrors}`);
  console.log(`  [!] Warnings: ${totalWarnings}`);
  console.log(`  [i] Notices:  ${totalNotices}`);

  if (totalErrors > 0) {
    console.log("\n  FAIL -- fix the errors above!");
    process.exit(1);
  } else {
    console.log("\n  PASS!");
    process.exit(0);
  }
}

main().catch((e) => {
  console.error("Fatal:", e.message);
  process.exit(1);
});
