// Screenshot the generated HTML pages to PNG (uses the preinstalled Playwright).
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const root = path.resolve(__dirname, '..');
  const b = await chromium.launch();
  for (const name of ['1-leg-strength', '2-calves-ankles']) {
    const p = await b.newPage({ viewport: { width: 1080, height: 1200 }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.join(root, 'html', name + '.html'));
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(root, name + '.png'), fullPage: true });
    console.log('wrote', name + '.png');
  }
  await b.close();
})();
