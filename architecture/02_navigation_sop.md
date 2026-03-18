# Architectural SOP: Navigation & Pipeline

## Layer 2 (Navigation)
- **Role:** The System Pilot (LLM Agent) acts as the Navigation layer, bridging Tools through reasoning.
- **Workflow:**
  1. Trigger Layer 3 scraping scripts (`scrape_reddit.py`, `scrape_html_events.py`) to gather raw JSON into `.tmp/`.
  2. The LLM reads the scraped raw data from `.tmp/`.
  3. The LLM processes context and extracts big events into the `Event Payload` JSON schema defined in `gemini.md`.
  4. The LLM maps the event payloads to a unified structured JSON block (`.tmp/payload.json`).
  5. The LLM triggers `tools/build_calendar.py` to compile the final `calendar.html` payload.

## Constraints
- Never guess event details; strictly verify against the raw JSON.
- Only include events large enough to impact hotel demand (e.g. festivals, multi-day sports, large concerts).
- If extraction fails or data is empty, do not hallucinate events.
