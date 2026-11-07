// node shot_one.js <in.html> <out.png>
const { chromium } = require('playwright');
(async () => {
  const [, , inp, out] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1200 }, deviceScaleFactor: 2 });
  await p.goto('file://' + require('path').resolve(inp));
  await p.waitForTimeout(300);
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
})();
