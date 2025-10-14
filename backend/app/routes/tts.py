from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def tts_health():
    return {"status": "tts route loaded"}
