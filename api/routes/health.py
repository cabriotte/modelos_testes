from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get(path="/health", status_code=200, summary="Health")
async def health():
    return {"status": "OK"}