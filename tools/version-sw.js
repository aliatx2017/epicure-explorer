/**
 * tools/version-sw.js — Hash-based Service Worker cache versioning
 *
 * Reads every file the SW caches (STATIC pre-cache list + lazy-loaded
 * model JSONs + sw.js itself), computes a SHA-256 hash, and replaces
 * the hardcoded 'epicure-v1' version string in sw.js with a
 * content-derived fingerprint.
 *
 * Run before deploying changes to index.html, sw.js, or any data file:
 *   node tools/version-sw.js
 *
 * Zero external dependencies — uses only Node.js built-ins.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const SW_PATH = path.join(ROOT, 'sw.js');

// ---- Configuration ------------------------------------------------
// Files explicitly pre-cached in STATIC (minus './' which is virtual).
const STATIC_FILES = [
  'index.html',
  'icon-192.png',
  'icon-512.png',
  'data/epicure_shared.json',
  'data/epicure_nutrition.json',
  'data/recipe_nutrition.json',
  'data/recipe_detections_slim.json',
];

// Lazy-loaded model JSONs cached on first fetch in the fetch handler.
const LAZY_FILES = [
  'data/epicure_cooc.json',
  'data/epicure_core.json',
  'data/epicure_chem.json',
];

// Include sw.js itself so logic changes also invalidate the cache.
// The CACHE line is normalized to a fixed placeholder before hashing
// so the version string doesn't feedback into itself.
const SELF = ['sw.js'];

const ALL_FILES = [...STATIC_FILES, ...LAZY_FILES, ...SELF];

// ---- Compute content hash -----------------------------------------
const hash = crypto.createHash('sha256');

for (const relPath of ALL_FILES) {
  const fullPath = path.join(ROOT, relPath);
  try {
    let content = fs.readFileSync(fullPath);
    // Normalize sw.js: replace the actual CACHE value with a placeholder
    // so the hash is stable regardless of the current version string.
    if (relPath === 'sw.js') {
      content = content.toString().replace(
        /const CACHE = 'epicure-[^']+'/,
        "const CACHE = 'epicure-PLACEHOLDER'"
      );
    }
    hash.update(content);
  } catch (err) {
    console.warn(`  ⚠  Could not read ${relPath} — skipping (${err.code})`);
  }
}

const digest = hash.digest('hex').slice(0, 12);
const NEW_VERSION = `epicure-${digest}`;

// ---- Patch sw.js --------------------------------------------------
const swContent = fs.readFileSync(SW_PATH, 'utf-8');
const VERSION_RE = /const CACHE = 'epicure-[a-f0-9]+'/;

if (!VERSION_RE.test(swContent) && swContent.includes("const CACHE = 'epicure-v1'")) {
  // First run — replace the hardcoded v1 with the hash version
  const updated = swContent.replace(
    "const CACHE = 'epicure-v1'",
    `const CACHE = '${NEW_VERSION}'`
  );
  fs.writeFileSync(SW_PATH, updated);
  console.log(`✅  ${NEW_VERSION}  (first run — was epicure-v1)`);
} else if (VERSION_RE.test(swContent)) {
  // Subsequent run — update existing hash
  const updated = swContent.replace(VERSION_RE, `const CACHE = '${NEW_VERSION}'`);
  fs.writeFileSync(SW_PATH, updated);
  const oldV = swContent.match(VERSION_RE)[0].replace("const CACHE = '", "").replace("'", "");
  console.log(`✅  ${NEW_VERSION}  (previously ${oldV})`);
} else {
  // Unexpected format — bail
  console.error('❌  Could not find cache version string in sw.js (expected epicure-v1 or epicure-<hash>)');
  process.exit(1);
}

// Also record the version in a dotfile for CI/tooling
const versionFile = path.join(ROOT, '.sw-version');
fs.writeFileSync(versionFile, NEW_VERSION + '\n');
console.log(`📝  .sw-version written`);
