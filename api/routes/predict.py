from fastapi import Response, HTTPException, APIRouter
from api.db.schemas.models_available import ModelsAvailable
from src.predict_prev_acoes import prever

router = APIRouter()

@router.post(path="/predict", tags=["Predict"])
async def get_result(id_model: str):
    """Informe o nome da ação para obter os resultados da previsão"""
    try:
        model_selected = ModelsAvailable.get(ModelsAvailable.id == id_model)
        result = prever(
            ticker=model_selected.ticker,
            model_name=model_selected.filename
        ).to_json(orient="records")
        return Response(content=result, media_type="application/json")
    except ModelsAvailable.DoesNotExist:
        raise HTTPException(status_code=404, detail="Modelo ainda nao treinado")