"""
Agent Orchestrator for GlobalMedTriage
- Coordinates all agents via async calls
- Entry point for backend to route requests
"""
from agents import (
    voice_interface_agent,
    medical_triage_agent,
    translation_coordinator_agent,
    medical_office_triage_voice_agent,
    emergency_dispatch_agent,
    vital_signs_monitor_agent,
    insurance_verification_agent
)

import asyncio

async def run_emergency_flow(audio_bytes: bytes, user_language: str = "auto") -> dict:
    """
    Orchestrate the full emergency triage flow.
    Returns dict of all agent responses.
    """
    # 1. Transcribe and detect language/panic
    voice_result = await voice_interface_agent.transcribe_audio(audio_bytes, language=user_language)
    # 2. Analyze symptoms
    triage_result = await medical_triage_agent.analyze_symptoms(voice_result["text"], language=voice_result["language"])
    # 3. Translate response
    translation = await translation_coordinator_agent.translate_medical(
        f"ESI Level: {triage_result['esi_level']}", voice_result["language"])
    # 4. Collect history
    history = await medical_office_triage_voice_agent.collect_history(audio_bytes)
    # 5. Analyze vitals
    vitals = await vital_signs_monitor_agent.analyze_vitals(audio_bytes)
    # 6. Dispatch ambulance (location to be provided by frontend or extracted from user data)
    dispatch = await emergency_dispatch_agent.dispatch_ambulance("REPLACE_WITH_REAL_LOCATION")
    # 7. Verify insurance (user_id to be provided by frontend or extracted from user data)
    insurance = await insurance_verification_agent.verify_insurance("REPLACE_WITH_REAL_USER_ID")
    return {
        "voice": voice_result,
        "triage": triage_result,
        "translation": translation,
        "history": history,
        "vitals": vitals,
        "dispatch": dispatch,
        "insurance": insurance
    }
