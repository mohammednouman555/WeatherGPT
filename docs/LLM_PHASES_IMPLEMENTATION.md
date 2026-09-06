# WeatherGPT — Gemini Conversational AI Phases 1–5

## Included

- Phase 1: frontend calls current weather, forecast risk, hourly forecast, and chat APIs through the FastAPI backend.
- Phase 2: Gemini receives a controlled, personalized prompt with activity-specific guidance and user preferences.
- Phase 3: `/api/chat/message` provides conversational messages with a conversation ID; `/api/chat/explain` remains backward compatible.
- Phase 4: current weather, hourly forecast, risk-window summary and per-hour risk context are supplied to Gemini. Questions such as `Is it better later?` are answered from supplied forecast/risk data only.
- Phase 5: name and preferred activities are stored in browser `localStorage` and sent with each chat request. Short-term conversation history is kept server-side per conversation ID.

## Backend files changed/added

- `app/services/llm_service.py`
- `app/services/conversation_service.py`
- `app/api/chat.py`
- `app/schemas/chat.py`
- `app/core/config.py`
- `requirements.txt`

## Frontend files changed

- `app/static/index.html`
- `app/static/css/dashboard.css`
- `app/static/js/dashboard.js`

## Testing

The implementation was checked with:

- Python bytecode compilation of backend application/tests.
- JavaScript syntax check with `node --check`.
- Unit tests for prompt construction and bounded conversation history.
- FastAPI startup with SQLite override.
- Mocked Gemini API endpoint tests for `/api/chat/message`, `/api/chat/explain`, and conversation deletion.

## Real Gemini test

1. Copy `backend/.env.example` to `backend/.env`.
2. Put your current Gemini API key in `GEMINI_API_KEY`.
3. Keep `GEMINI_MODEL=gemini-2.5-flash-lite` if that is the model available to your account.
4. Activate the backend virtual environment.
5. Start from `backend`:

```powershell
uvicorn app.main:app --reload
```

6. Open `http://127.0.0.1:8000/docs`.
7. Test `POST /api/chat/message` with the sample payload from the project README or the dashboard.
8. Open `http://127.0.0.1:8000/dashboard/` and run an analysis.
9. Click `Explain current assessment`.
10. Ask follow-up questions such as:
   - `Is it better later?`
   - `Why is this moderate risk?`
   - `What should I watch for while cycling?`
   - `How does this compare with the next few hours?`
11. Change the name/preferred activities and ask again to verify personalization.
12. Click `New conversation` and verify that the next message starts a fresh conversation.

## Important

The deliverable does not contain a real API key. Add it locally to `backend/.env` and never commit that file.
