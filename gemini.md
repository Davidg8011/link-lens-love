# Data Schema & Law

## JSON Data Schema

### Input Shape (Raw Scraped Data)
```json
{
  "source_url": "string",
  "source_type": "string",
  "raw_text": "string",
  "scraped_at": "string (ISO 8601)"
}
```

### Output Shape (Event Payload)
```json
{
  "event_name": "string",
  "start_date": "string (YYYY-MM-DD)",
  "end_date": "string (YYYY-MM-DD)",
  "verification_url": "string",
  "description": "string"
}
```

## Rules
- **North Star:** Utility to track big events in South Lake Tahoe to predict hotel demand.
- **Tone/Behavior:** Simple, reasonable, straightforward.
- **Integrations:** Scraping articles, Reddit, and local postings.
- **Source of Truth & Delivery Payload:** A simple, local-hosted calendar website that lists big events and includes a link to verify the event.

## Maintenance Log
- [2026-03-18] Initialized Data Schema and Rules based on Discovery.
- [2026-03-18] Completed Phase 1 to Phase 5. Built Navigation script (`tools/navigation.py`) orchestrated with Gemini LLM extraction. Finalized payload building to `.tmp/payload.json` and stylized calendar locally. Created Task Scheduler trigger batch script (`run_pipeline.bat`).
