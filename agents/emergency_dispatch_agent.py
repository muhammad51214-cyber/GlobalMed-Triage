"""
Emergency Dispatch Agent
- Simulates GPS + ambulance dispatch
- Exposes async functions for backend orchestrator
"""
async def dispatch_ambulance(location: str) -> dict:
    """Dispatch ambulance using a placeholder dispatch API."""
    import httpx
    url = "https://api.example.com/v1/dispatch/ambulance"
    payload = {"location": location}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return {"status": data.get("status", "dispatched"), "location": data.get("location", location)}
