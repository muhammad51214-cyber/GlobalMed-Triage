"""
Medical Office Triage Voice Agent
- Collects history, follows protocols, HIPAA-compliant
- Exposes async functions for backend orchestrator
"""
async def collect_history(audio_bytes: bytes) -> dict:
    """Collects medical history from audio using a production NLP/voice API (replace URL with real endpoint)."""
    import httpx
    url = "REPLACE_WITH_PRODUCTION_HISTORY_API_URL"
    headers = {"Content-Type": "application/octet-stream"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, content=audio_bytes)
        response.raise_for_status()
        data = response.json()
        return {"history": data.get("history", "No history found.")}
