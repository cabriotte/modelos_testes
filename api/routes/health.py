from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.post("/health")
async def health():
    return {"status": "OK"}