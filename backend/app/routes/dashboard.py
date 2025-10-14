from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def dashboard_health():
    return {"status": "dashboard route loaded"}
