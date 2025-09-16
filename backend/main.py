"""
GlobalMedTriage FastAPI backend entrypoint.
- Orchestrates Coral Protocol agents
- Provides WebSocket for real-time agent communication
- JWT authentication
- API endpoints for triage, logs, and protocols
"""
import os
from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GlobalMedTriage API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = os.getenv("JWT_SECRET", "changeme")
ALGORITHM = "HS256"

# --- Auth utils ---
def verify_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/health")
def health():
    return {"status": "ok"}

# --- WebSocket for agent orchestration ---
@app.websocket("/ws/triage")
async def ws_triage(websocket: WebSocket):
    from agent_orchestrator import run_emergency_flow
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        # Expecting {"audio": ...base64...}
        import base64
        audio_b64 = data.get("audio")
        if not audio_b64:
            await websocket.send_json({"error": "No audio provided."})
            continue
        try:
            audio_bytes = base64.b64decode(audio_b64.split(",")[-1])
            result = await run_emergency_flow(audio_bytes)
            await websocket.send_json(result)
        except Exception as e:
            await websocket.send_json({"error": str(e)})

## Production endpoints to be implemented here
