from fastapi import Response, APIRouter, HTTPException
from api.db.schemas.model_prediction_duration import ModelPredictionDuration

router = APIRouter()


@router.get(path="/duration-stats", tags=["Duration Stats"])
async def get_duration_stats():
    """Obtenha as estatísticas de duração das previsões dos modelos treinados"""
    try:
        duration_stats = ModelPredictionDuration.select().dicts()
        return Response(
            content=str(list(duration_stats)), media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Erro ao obter as estatísticas de duração"
        )
