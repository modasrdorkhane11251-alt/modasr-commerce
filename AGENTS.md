# Notes
- Only the Next.js frontend runs in the Base44 compose. `backend/` is incomplete (no `main.py`, no `requirements.txt`), so it cannot boot; add those before adding backend/postgres/redis services.
- `frontend/next.config.js` was converted to CommonJS (the original used TS syntax in a .js file) and the unsupported `i18n` option was dropped (App Router).
