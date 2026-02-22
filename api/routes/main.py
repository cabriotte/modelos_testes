from fastapi import APIRouter


router = APIRouter(tags=["Main"])

@router.get('/')
async def index():
    return {"status": "OK"}