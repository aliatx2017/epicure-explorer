#!/usr/bin/env node

/**
 * check-fallbacks.mjs
 *
 * Validates that inline fallback constants in index.html (SEASONAL_DATA,
 * NUTRITION_DATA) match the data in epicure_shared.json.
 *
 * Exit code 0 = no drift, non-zero = drift found or error.
 *
 * Usage: node tools/check-fallbacks.mjs
 */

import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const HTML_PATH = join(ROOT, 'index.html');
const JSON_PATH = join(ROOT, 'data', 'epicure_shared.json');

// ---- Helpers ----

/** Extract a JS object literal block between `var NAME = {` and the matching `};`. */
function extractBlock(html, varName) {
  const startMarker = `var ${varName} = {`;
  const startIdx = html.indexOf(startMarker);
  if (startIdx === -1) throw new Error(`Could not find "var ${varName} = {" in index.html`);

  // Find the matching `};` — start after the opening `{`
  const contentStart = startIdx + startMarker.length;
  let depth = 1;
  let pos = contentStart;
  while (depth > 0 && pos < html.length) {
    const ch = html[pos];
    if (ch === '{') depth++;
    else if (ch === '}') depth--;
    pos++;
  }
  // pos now points just past the closing `}`
  const block = html.slice(contentStart, pos - 1); // exclude the closing `}`
  return block;
}

/** Parse a JS object-literal block into a Map of key → value-string.
 *  Strips line comments and trailing commas, extracts key: value pairs. */
function parseBlock(block) {
  // Remove // line comments
  const noComments = block.replace(/\/\/[^\n]*/g, '');

  const map = new Map();
  // Match key: value pairs — keys are identifier-like, values match until comma or closing brace
  const re = /([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*('[^']*'|\[[^\]]*\])\s*,?\s*/g;
  let match;
  while ((match = re.exec(noComments)) !== null) {
    const key = match[1];
    const value = match[2].trim();
    // Normalise: strip outer quotes from strings, keep arrays as-is
    const normalised = (value.startsWith("'") && value.endsWith("'"))
      ? value.slice(1, -1)
      : value;
    map.set(key, normalised);
  }
  return map;
}

// ---- Main ----

let exitCode = 0;

try {
  const html = readFileSync(HTML_PATH, 'utf-8');
  const json = JSON.parse(readFileSync(JSON_PATH, 'utf-8'));

  // ── SEASONAL_DATA ──
  const seasonalInline = parseBlock(extractBlock(html, 'SEASONAL_DATA'));
  const seasonalJson = new Map(Object.entries(json.seasonal || {}));

  let seasonalDiffs = [];
  for (const [key, inlineVal] of seasonalInline) {
    if (!seasonalJson.has(key)) {
      seasonalDiffs.push(`  EXTRA in index.html: "${key}": '${inlineVal}' (missing in epicure_shared.json)`);
    } else if (seasonalJson.get(key) !== inlineVal) {
      seasonalDiffs.push(`  DIFFERS: "${key}" — index.html: '${inlineVal}', epicure_shared.json: '${seasonalJson.get(key)}'`);
    }
  }
  for (const [key, jsonVal] of seasonalJson) {
    if (!seasonalInline.has(key)) {
      seasonalDiffs.push(`  EXTRA in epicure_shared.json: "${key}": '${jsonVal}' (missing in index.html)`);
    }
  }

  if (seasonalDiffs.length > 0) {
    console.error(`❌ SEASONAL_DATA drift (${seasonalDiffs.length} difference(s)):`);
    seasonalDiffs.forEach(d => console.error(d));
    exitCode = 1;
  } else {
    console.log(`✅ SEASONAL_DATA: ${seasonalInline.size} entries match epicure_shared.json`);
  }

  // ── NUTRITION_DATA ──
  const nutritionInline = parseBlock(extractBlock(html, 'NUTRITION_DATA'));
  const nutritionJson = new Map(Object.entries(json.nutrition || {}));

  let nutritionDiffs = [];
  for (const [key, inlineVal] of nutritionInline) {
    if (!nutritionJson.has(key)) {
      nutritionDiffs.push(`  EXTRA in index.html: "${key}": ${inlineVal} (missing in epicure_shared.json)`);
    } else {
      const jsonVal = JSON.stringify(nutritionJson.get(key));
      if (jsonVal !== inlineVal) {
        nutritionDiffs.push(`  DIFFERS: "${key}" — index.html: ${inlineVal}, epicure_shared.json: ${jsonVal}`);
      }
    }
  }
  for (const [key, jsonVal] of nutritionJson) {
    if (!nutritionInline.has(key)) {
      nutritionDiffs.push(`  EXTRA in epicure_shared.json: "${key}": ${JSON.stringify(jsonVal)} (missing in index.html)`);
    }
  }

  if (nutritionDiffs.length > 0) {
    console.error(`❌ NUTRITION_DATA drift (${nutritionDiffs.length} difference(s)):`);
    nutritionDiffs.forEach(d => console.error(d));
    exitCode = 1;
  } else {
    console.log(`✅ NUTRITION_DATA: ${nutritionInline.size} entries match epicure_shared.json`);
  }

} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}

process.exit(exitCode);
