# Next Session — Starting Point

**Branch:** `main`  
**Last commit:** Session 10 (feedback-driven polish sprint)  
**All 57 E2E tests pass · 0 console errors · 0 known bugs**

---

## Current State

| Metric | Value |
|--------|-------|
| `index.html` lines | **6,343** |
| JS functions | **136** |
| Tabs | 18 (4 categories) |
| File size | 339 KB |
| Console errors | **0** |
| Known bugs | **0** |
| E2E tests | **57/57 ✅** |
| Languages | EN, ES, FR, 中文, 日本語 |

---

## What Session 10 Shipped

- Spoonacular call tracking + 429 handling
- Offline banner + offline-aware API calls
- 50+ search aliases (coriander→cilantro, etc.)
- Density heatmap overlay on Map
- CSV neighbour export, Map PNG export, share link
- 5-language i18n (UI strings only)
- Search intent detection (cuisine/diet/nutrition keywords)
- Usage analytics (localStorage-based, privacy-preserving)

---

## Open Items & Gaps for Next Session

### Remaining Scoped Phases (from Sessions 6/9)
| Phase | Feature | Effort | Priority |
|-------|---------|--------|----------|
| 4 | Games interactivity upgrade (more game modes, leaderboard) | Medium | Low |
| 5 | Build-A-Dish mode (compose ingredient combinations with flavour preview) | High | Medium |
| 6 | Semantic Describe a Dish (upgrade natural-language parsing with semantic understanding) | Medium | Low |

### Unstarted Opportunities
| Item | Effort | Notes |
|------|--------|-------|
| **Performance optimization** | Medium | Larger-scale virtualized rendering for map |
| **Export/Share workflows** | Medium | Export pairing as image, share via QR |
| **i18n ingredient names** | High | Translate ingredient names themselves (not just UI), leveraging Epicure's 7-language data |
| **Map heatmap improvements** | Low | Dynamic density threshold slider, zoom-adaptive grid resolution |
| **Recipe generation (LLM)** | High | Needs backend — requires FastAPI/Node server, API key management, cost control |
| **Ingredient2Vec REST API** | High | Server-side project: auth, rate-limiting, billing |

### Feedback Items Not Yet Addressed
| Item | Notes |
|------|-------|
| Mobile UX — chef sidebar may clip on very small phones | Current `max-width: 90vw` with 768px breakpoint `width: 100%` — test on actual small devices |
| No "remaining calls" display was missing — now shipped ✅ | |
| Offline state was not communicated — now shipped ✅ | |
| No density heatmap — now shipped ✅ | |
| No CSV/PNG/share exports — now shipped ✅ | |

### Future Architectural Directions (Separate Project)
- Ingredient2Vec REST API + OpenAPI spec (requires server)
- Recipe generation via LLM (requires backend + API keys)
- Professional/Creator paid tier (requires auth, billing)
- Analytics dashboard (requires server logs or third-party service)

---

## Quick Start

```bash
cd epicure-explorer
python3 -m http.server 8080
# Open http://localhost:8080
```

## Run Tests

```bash
cd epicure-explorer
node tests/e2e.mjs   # 57 tests, ~45s
```
