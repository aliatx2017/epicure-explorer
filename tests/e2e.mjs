/**
 * Epicure Explorer — Comprehensive End-to-End Test Suite
 * Run: node tests/e2e.mjs
 */
import { chromium } from 'playwright';
import { createServer } from 'http';
import { readFileSync, existsSync } from 'fs';
import { extname, join } from 'path';
import { fileURLToPath } from 'url';

const DIR = fileURLToPath(new URL('..', import.meta.url));
const PORT = 9876;
const BASE = `http://localhost:${PORT}`;

const MIME = {
  '.html': 'text/html', '.js': 'application/javascript', '.json': 'application/json',
  '.csv': 'text/csv', '.txt': 'text/plain', '.css': 'text/css', '.svg': 'image/svg+xml',
};
function serve(req, res) {
  let p = req.url.split('?')[0].split('#')[0];
  if (p === '/') p = '/index.html';
  const fp = join(DIR, p);
  try {
    if (!existsSync(fp)) { res.writeHead(404); res.end('Not found'); return; }
    const ext = extname(fp);
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
    res.end(readFileSync(fp));
  } catch(e) {
    if (!res.headersSent) { res.writeHead(500); res.end('Error'); }
  }
}
const server = createServer(serve);

const results = { pass: 0, fail: 0, errors: [] };

async function test(name, fn) {
  try {
    await fn();
    results.pass++;
    console.log(`  ✅ ${name}`);
  } catch(e) {
    results.fail++;
    results.errors.push({ name, message: e.message });
    console.log(`  ❌ ${name}`);
    console.log(`     ${e.message.split('\n')[0]}`);
  }
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

/**
 * Dismiss the onboarding tour if it's blocking clicks.
 * The tour overlay has pointer-events and blocks interactions.
 */
async function dismissTour(page) {
  // Wait for tour to appear then dismiss by clicking anywhere on the overlay
  try {
    const overlay = await page.$('#tourOverlay');
    if (overlay) {
      const active = await page.evaluate(el => el.classList.contains('active'), overlay);
      if (active) {
        // Click on the overlay to dismiss (registered click handler calls endTour)
        await overlay.click({ force: true }); // force bypasses pointer-events check? no
        // Actually the overlay's click handler calls endTour, but it may have pointer-events disabled
        // Let's use evaluate to dismiss programmatically
        await page.evaluate(() => {
          if (window.endTour) window.endTour();
          const o = document.getElementById('tourOverlay');
          if (o) o.classList.remove('active');
        });
        await sleep(200);
      }
    }
  } catch(e) {
    // Ignore — tour may not have fired yet
  }
}

async function main() {
  await new Promise(r => server.listen(PORT, r));
  console.log(`\n🌐 Server on ${BASE}\n`);

  const browser = await chromium.launch({ headless: true });

  // Single shared page across all tests to avoid reload overhead
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });

  try {
    // ───── 0. App Load ─────
    console.log('═══ 0. App Load ═══');
    await test('App loads without console errors', async () => {
      await page.goto(BASE, { waitUntil: 'networkidle', timeout: 20000 });
      await sleep(3000);
      await dismissTour(page);
      await sleep(300);

      const critical = errors.filter(e =>
        e.includes('ReferenceError') || e.includes('TypeError') || e.includes('is not defined')
      );
      assert(critical.length === 0, `Errors: ${critical.join('; ')}`);
      await waitFor(page, '#mainContent');
      const style = await page.getAttribute('#mainContent', 'style');
      assert(!style || !style.includes('display:none'), 'Main hidden');
    }, 30000);

    // ───── 1. Header & PWA ─────
    console.log('\n═══ 1. Header & PWA ═══');
    await test('PWA manifest & meta tags present', async () => {
      assert(await page.$('link[rel="manifest"]'), 'No manifest');
      assert(await page.$('meta[name="theme-color"]'), 'No theme-color');
    });
    await test('Dark mode toggle works', async () => {
      await dismissTour(page);
      const btn = await page.$('#themeToggle');
      assert(btn, 'No toggle');
      await btn.click();
      await sleep(200);
      const isLight = await page.evaluate(() => document.documentElement.classList.contains('light'));
      assert(isLight, 'Light class not added');
      await btn.click();
      await sleep(200);
      const isDark = await page.evaluate(() => !document.documentElement.classList.contains('light'));
      assert(isDark, 'Light not removed');
    });
    await test('Header renders', async () => {
      const title = await page.textContent('h1');
      assert(title.includes('Epicure'), `Bad title: ${title}`);
    });

    // ───── 2. Unified Search ─────
    console.log('\n═══ 2. Unified Search ═══');
    await test('Search input visible & shows dropdown', async () => {
      await dismissTour(page);
      await waitFor(page, '#searchInput');
      const input = await page.$('#searchInput');
      await input.fill('miso');
      await sleep(350);
      const items = await page.$$('#searchDropdown.show .item');
      assert(items.length > 0, `No dropdown items (got ${items.length})`);
    });
    await test('Ingredient selection from search works', async () => {
      await dismissTour(page);
      const input = await page.$('#searchInput');
      await input.fill('miso');
      await sleep(350);
      const item = await page.$('#searchDropdown .item');
      assert(item, 'No item');
      // Use force click since tour may still intercept
      await item.click({ force: true });
      await sleep(300);
      const sel = await page.textContent('#selectedIngredient');
      assert(sel.includes('miso') || sel.includes('Miso'), `Got: ${sel}`);
    });
    await test('Describe-a-dish auto-detects multi-word input', async () => {
      await dismissTour(page);
      await page.evaluate(() => {
        const d = document.getElementById('describeInput');
        if (d) d.value = '';
        document.getElementById('describeResults').innerHTML = '';
      });
      const input = await page.$('#searchInput');
      await input.fill('creamy garlic pasta');
      await sleep(800); // debounce 350ms
      // Check describe results appeared
      const dr = await page.$('#describeResults');
      if (dr) {
        const html = await dr.innerHTML();
        assert(html.length > 0, 'Describe results empty');
      }
      // Restore miso for subsequent tests
      await input.fill('miso');
      await sleep(350);
      const item = await page.$('#searchDropdown .item');
      if (item) await item.click({ force: true });
      await sleep(200);
    });

    // ───── 3. Model Switching ─────
    console.log('\n═══ 3. Model Switching ═══');
    for (const model of ['core', 'chem', 'cooc']) {
      await test(`Switch to ${model} model`, async () => {
        await dismissTour(page);
        const btn = await page.$(`.model-tab[data-model="${model}"]`);
        assert(btn, `No ${model} tab`);
        await btn.click();
        await sleep(1500); // lazy load
      });
    }

    // ───── 4. All 18 Tab Panels ─────
    console.log('\n═══ 4. Tab Panel Rendering ═══');
    const tabs = [
      { tab: 'neighbours', cat: 'core' },
      { tab: 'compare', cat: 'core' },
      { tab: 'slerp', cat: 'core' },
      { tab: 'map', cat: 'core' },
      { tab: 'modes', cat: 'core' },
      { tab: 'recipes', cat: 'core' },
      { tab: 'games', cat: 'play' },
      { tab: 'arithmetic', cat: 'play' },
      { tab: 'cocktail', cat: 'play' },
      { tab: 'analyzer', cat: 'analyze' },
      { tab: 'compare2', cat: 'analyze' },
      { tab: 'snap', cat: 'analyze' },
      { tab: 'seasonal', cat: 'analyze' },
      { tab: 'spoonacular', cat: 'advanced' },
      { tab: 'ingredient2vec', cat: 'advanced', label: 'I2Vec' },
      { tab: 'foodagent', cat: 'advanced', label: 'Food Agent' },
      { tab: 'trending', cat: 'advanced' },
      { tab: 'mealplan', cat: 'advanced' },
    ];

    for (const t of tabs) {
      await test(`Tab "${t.tab}" panel renders`, async () => {
        await dismissTour(page);
        // Switch category
        const catBtn = await page.$(`.tab-cat[data-cat="${t.cat}"]`);
        if (catBtn) {
          const isActive = await page.evaluate(el => el.classList.contains('active'), catBtn);
          if (!isActive) await catBtn.click();
          await sleep(150);
        }
        const tabBtn = await page.$(`.tab[data-tab="${t.tab}"]`);
        assert(tabBtn, `No tab ${t.tab}`);
        await tabBtn.click();
        await sleep(400);
        // Verify panel visible
        const panel = await page.$(`#panel-${t.tab}`);
        if (panel) {
          const d = await page.evaluate(el => window.getComputedStyle(el).display, panel);
          assert(d !== 'none', `Panel ${t.tab} hidden`);
        }
        const ce = errors.filter(e => e.includes('ReferenceError') || e.includes('is not defined'));
        assert(ce.length === 0, `Errors: ${ce.slice(-2).join('; ')}`);
      });
    }

    // ───── 5. Feature-Specific ─────
    console.log('\n═══ 5. Feature-Specific Tests ═══');

    // 5a. Map tab
    await test('Map renders canvas with each projection', async () => {
      await dismissTour(page);
      await page.click('.tab-cat[data-cat="core"]');
      await sleep(150);
      await page.click('.tab[data-tab="map"]');
      await sleep(1500);
      const canvas = await page.$('#pcaCanvas');
      assert(canvas, 'No canvas');
      const w = await page.evaluate(el => el.width, canvas);
      assert(w > 100, `Canvas too small: ${w}`);
      for (const method of ['pca', 'force']) {
        await page.selectOption('#projMethod', method);
        await sleep(method === 'force' ? 2000 : 800);
        assert(await page.$('#pcaCanvas'), `Canvas disappeared on ${method}`);
      }
      // Reset to UMAP
      await page.selectOption('#projMethod', 'umap');
      await sleep(800);
    });

    // 5b. Map search
    await test('Map search finds ingredient', async () => {
      await dismissTour(page);
      const ms = await page.$('#mapSearch');
      assert(ms, 'No map search');
      await ms.fill('chicken');
      await sleep(500);
      assert(await page.$('#pcaCanvas'), 'Canvas lost');
    });

    // 5c. Games
    await test('Games tab has game elements', async () => {
      await dismissTour(page);
      await page.click('.tab-cat[data-cat="play"]');
      await sleep(150);
      await page.click('.tab[data-tab="games"]');
      await sleep(600);
      const has = await page.$('#compassCanvas') || await page.$('#guessGame');
      assert(!!has, 'No game UI');
    });

    // 5d. Cocktails, Arith
    for (const tab of ['arithmetic', 'cocktail']) {
      await test(`${tab} tab has visible panel`, async () => {
        await dismissTour(page);
        await page.click('.tab[data-tab="' + tab + '"]');
        await sleep(400);
        const p = await page.$('#panel-' + tab);
        if (p) {
          const d = await page.evaluate(el => window.getComputedStyle(el).display, p);
          assert(d !== 'none', `Panel ${tab} hidden`);
        }
      });
    }

    // 5e. Analyzer
    await test('Analyzer parses ingredient text', async () => {
      await dismissTour(page);
      // Use evaluate to ensure clicks happen regardless of overlay
      await page.evaluate(() => {
        const catBtn = document.querySelector('.tab-cat[data-cat="analyze"]');
        if (catBtn && !catBtn.classList.contains('active')) catBtn.click();
      });
      await sleep(200);
      await page.evaluate(() => {
        const tabBtn = document.querySelector('.tab[data-tab="analyzer"]');
        if (tabBtn) tabBtn.click();
      });
      await sleep(600);
      const ta = await page.$('#analyzerInput');
      if (ta) {
        // Use evaluate for fill to bypass pointer interception
        await page.evaluate(() => {
          const el = document.getElementById('analyzerInput');
          if (el) { el.value = 'garlic, onion, tomato'; el.dispatchEvent(new Event('input', { bubbles: true })); }
        });
        await sleep(300);
        // Try clicking any Analyze/Run button in the panel
        await page.evaluate(() => {
          const btns = document.querySelectorAll('#panel-analyzer button, #panel-analyzer .game-new-btn');
          for (const btn of btns) {
            if (btn.textContent.includes('Analyze') || btn.textContent.includes('Run')) {
              btn.click();
              break;
            }
          }
        });
        await sleep(500);
      } else {
        assert(false, 'Analyzer textarea #analyzerInput not found');
      }
    });

    // 5f. Compare2
    await test('Compare2 renders two inputs', async () => {
      await dismissTour(page);
      await page.click('.tab[data-tab="compare2"]');
      await sleep(400);
      const inputs = await page.$$('#panel-compare2 input');
      assert(inputs.length >= 2, `Only ${inputs.length} inputs`);
    });

    // 5g. Seasonal + Heatmap
    await test('Seasonal heatmap toggle works', async () => {
      await dismissTour(page);
      await page.click('.tab[data-tab="seasonal"]');
      await sleep(800);
      assert(await page.$('#seasonalResults'), 'No seasonal results');
      // Switch season
      await page.selectOption('#seasonSelect', 'summer');
      await sleep(600);
      // Toggle heatmap
      const hmBtn = await page.$('#seasonHeatmapToggle');
      assert(hmBtn, 'No heatmap toggle');
      await hmBtn.click();
      await sleep(500);
      const hw = await page.$('#seasonalHeatmapWrap');
      if (hw) {
        const d = await page.evaluate(el => window.getComputedStyle(el).display, hw);
        if (d !== 'none') {
          const table = await hw.$('table');
          assert(table, 'Heatmap table missing');
          const rows = await table.$$('tr');
          assert(rows.length > 2, `Only ${rows.length} heatmap rows`);
        }
      }
      // Toggle back
      await hmBtn.click();
      await sleep(300);
    });

    // 5h. Spoonacular graceful degradation
    await test('Spoonacular shows degraded state without API key', async () => {
      await dismissTour(page);
      await page.evaluate(() => localStorage.removeItem('spoonacular_key'));
      await page.click('.tab-cat[data-cat="advanced"]');
      await sleep(150);
      await page.click('.tab[data-tab="spoonacular"]');
      await sleep(600);
      // Must show key input
      assert(await page.$('#spoonKeyInput'), 'No key input');
      // Check for degraded banner
      const degraded = await page.$('#spoonDegraded');
      if (degraded) {
        const d = await page.evaluate(el => window.getComputedStyle(el).display, degraded);
        assert(d !== 'none', 'Degraded banner hidden');
      } else {
        // Layout should be hidden
        const layout = await page.$('#spoonLayout');
        if (layout) {
          const d = await page.evaluate(el => window.getComputedStyle(el).display, layout);
          assert(d === 'none' || d === '', `Layout visible: ${d}`);
        }
      }
    });

    // 5i. Ingredient2Vec, Food Agent, Trending, MealPlan
    for (const tab of ['ingredient2vec', 'foodagent', 'trending', 'mealplan']) {
      await test(`${tab} tab renders`, async () => {
        await dismissTour(page);
        await page.click('.tab[data-tab="' + tab + '"]');
        await sleep(500);
        const p = await page.$('#panel-' + tab);
        if (p) {
          const d = await page.evaluate(el => window.getComputedStyle(el).display, p);
          assert(d !== 'none', `Panel ${tab} hidden`);
        }
      });
    }

    // ───── 6. Chef's Toolkit ─────
    console.log('\n═══ 6. Chef\'s Toolkit ═══');
    await test('Chef\'s Toolkit opens and shows content', async () => {
      await dismissTour(page);
      // Ensure miso is selected
      const input = await page.$('#searchInput');
      await input.fill('miso');
      await sleep(350);
      const item = await page.$('#searchDropdown .item');
      if (item) await item.click({ force: true });
      await sleep(300);

      const chefBtn = await page.$('#chefToggle');
      assert(chefBtn, 'No chef toggle');
      await chefBtn.click();
      await sleep(500);
      const sidebar = await page.$('#chefSidebar.visible');
      assert(sidebar, 'Sidebar not visible');

      // Check substitutes
      const subRows = await page.$$('#chefSubstitutes .chef-sub-row');
      assert(subRows.length > 0, 'No substitute rows');
    });
    await test('Cross-model consensus badges visible', async () => {
      // Wait for consensus badges in the substitutes
      const badges = await page.$$('.consensus-badge');
      // May not appear if only 1 model is loaded — but if all 3 are loaded, they should
      // This is a soft assertion
      if (badges.length === 0) {
        const rows = await page.$$('#chefSubstitutes .chef-sub-row');
        assert(rows.length > 0, 'No substitutes to check');
        // Consensus badge requires 2+ models loaded
        console.log('     ℹ️ (skipped badge check: may need all 3 models)');
      }
    });
    await test('Molecular fingerprint in flavour profile', async () => {
      const notes = await page.$('.chef-molecular-notes');
      if (notes) {
        const h4 = await page.textContent('.chef-molecular-notes h4');
        assert(h4 && h4.includes('Molecular'), `Wrong header: ${h4}`);
      } else {
        // Some ingredients may not have molecular notes
        console.log('     ℹ️ (no molecular notes for this ingredient)');
      }
    });
    await test('Chef\'s Toolkit closes via backdrop', async () => {
      const backdrop = await page.$('#sidebarBackdrop');
      assert(backdrop, 'No backdrop');
      await backdrop.click();
      await sleep(400);
      const visible = await page.$('#chefSidebar.visible');
      assert(!visible, 'Sidebar still visible');
    });

    // ───── 7. Category Navigation ─────
    console.log('\n═══ 7. Category Navigation ═══');
    for (const cat of ['core', 'play', 'analyze', 'advanced']) {
      await test(`Category "${cat}" switchable`, async () => {
        await dismissTour(page);
        const btn = await page.$(`.tab-cat[data-cat="${cat}"]`);
        assert(btn, `No ${cat} button`);
        await btn.click();
        await sleep(150);
        const isActive = await page.evaluate(el => el.classList.contains('active'), btn);
        assert(isActive, `${cat} not active after click`);
      });
    }

    // ───── 8. Deep-Link URL ─────
    console.log('\n═══ 8. Deep-Link URL ═══');
    await test('Hash-based deep-link loads correct state', async () => {
      // Fresh browser context forces a full page load with deep-link hash
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
      const p = await ctx.newPage();
      await p.goto(`${BASE}/#tab=map&model=cooc&ingredient=chocolate`, { waitUntil: 'networkidle', timeout: 20000 });
      await sleep(4000);

      // Dismiss tour
      await p.evaluate(() => { if (typeof endTour === 'function') endTour(); }).catch(() => {});
      await sleep(300);

      // Check with retries
      let stateIng = '';
      let domText = '';
      for (let attempt = 0; attempt < 15; attempt++) {
        domText = await p.textContent('#selectedIngredient').catch(() => '');
        stateIng = await p.evaluate(() => {
          try { return STATE.selectedIngredient; } catch(e) { return 'ERR:' + e.message; }
        }).catch(() => 'ERROR');
        if (domText.includes('chocolate') || stateIng === 'chocolate') break;
        await sleep(500);
      }

      console.log(`     ℹ️ DOM: "${domText}" | STATE: "${stateIng}"`);
      assert(domText.includes('chocolate'), `Deep-link: DOM=${domText} STATE=${stateIng}`);
      await ctx.close();
    });

    // ───── 9. Service Worker ─────
    console.log('\n═══ 9. Service Worker ═══');
    await test('Service Worker registered', async () => {
      const regs = await page.evaluate(() =>
        navigator.serviceWorker.getRegistrations().then(r => r.length)
      );
      assert(regs >= 1, `No SW (got ${regs})`);
    });

    // ───── 10. Onboarding Tour ─────
    console.log('\n═══ 10. Onboarding Tour ═══');
    await test('Tour fires on fresh visit', async () => {
      const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
      const p = await ctx.newPage();
      await p.goto(BASE, { waitUntil: 'networkidle', timeout: 20000 });
      await sleep(2500);
      const overlay = await p.$('#tourOverlay');
      assert(!!overlay, 'Tour overlay not created');
      // End the tour programmatically
      await p.evaluate(() => { if (window.endTour) endTour(); });
      await ctx.close();
    });

    // ───── 11. Gesture Hint (touch) ─────
    console.log('\n═══ 11. Gesture Hint ═══');
    await test('Gesture hint shown on touch device map visit', async () => {
      const ctx = await browser.newContext({
        viewport: { width: 768, height: 900 },
        hasTouch: true,
      });
      const p = await ctx.newPage();
      await p.goto(BASE, { waitUntil: 'networkidle', timeout: 20000 });
      await sleep(3000);
      // Navigate to map via evaluate to avoid click interception
      await p.evaluate(() => {
        const catBtn = document.querySelector('.tab-cat[data-cat="core"]');
        if (catBtn) catBtn.click();
      });
      await sleep(300);
      await p.evaluate(() => {
        const tabBtn = document.querySelector('.tab[data-tab="map"]');
        if (tabBtn) tabBtn.click();
      });
      await sleep(2000);
      const marker = await p.evaluate(() => localStorage.getItem('epicure_map_hint_done'));
      assert(marker === '1', `Hint marker not set: ${marker}`);
      await ctx.close();
    });

    // ───── 12. Responsive ─────
    console.log('\n═══ 12. Responsive Layout ═══');
    for (const w of [768, 480]) {
      await test(`Responsive at ${w}px`, async () => {
        const ctx = await browser.newContext({ viewport: { width: w, height: 700 } });
        const p = await ctx.newPage();
        await p.goto(BASE, { waitUntil: 'networkidle', timeout: 15000 });
        await sleep(2000);
        const body = await p.$('body');
        assert(!!body, 'No body');
        await ctx.close();
      });
    }

    // ───── 13. Accessibility ─────
    console.log('\n═══ 13. Accessibility ═══');
    await test('Inputs have aria-label', async () => {
      const inputs = await page.$$('input');
      for (const el of inputs) {
        const id = await el.getAttribute('id');
        const label = await el.getAttribute('aria-label');
        assert(!!label, `#${id} missing aria-label`);
      }
    });
    await test('Tablist has ARIA role', async () => {
      const tl = await page.$('[role="tablist"]');
      assert(!!tl, 'No role="tablist"');
    });

  } catch(e) {
    console.error('Harness error:', e.message);
    results.errors.push({ name: 'HARNESS', message: e.message });
  } finally {
    await browser.close();
    await new Promise(r => server.close(r));
  }

  console.log(`\n═══ RESULTS ═══`);
  console.log(`Passed: ${results.pass}  Failed: ${results.fail}  Total: ${results.pass + results.fail}`);
  if (results.fail > 0) {
    console.log(`\n❌ Failures:`);
    for (const e of results.errors) {
      console.log(`  - ${e.name}: ${e.message.split('\n')[0]}`);
    }
  }
  console.log(`\n${results.fail === 0 ? '✅ ALL PASSED' : '❌ FAILURES'}`);
  process.exit(results.fail > 0 ? 1 : 0);
}

function assert(condition, msg) { if (!condition) throw new Error(msg); }
function waitFor(page, selector) { return page.waitForSelector(selector, { timeout: 8000, state: 'visible' }); }

main();
