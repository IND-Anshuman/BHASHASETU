from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def feedback_health():
    return {"status": "feedback route loaded"}
