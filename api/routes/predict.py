from fastapi import Response, HTTPException, APIRouter
from api.db.schemas.models_available import ModelsAvailable
from api.db.schemas.model_prediction_duration import ModelPredictionDuration
from src.predict_prev_acoes import prever
from time import perf_counter

router = APIRouter()


@router.post(path="/predict", tags=["Predict"])
async def get_result(id_model: str):
    """Informe o nome da ação para obter os resultados da previsão"""
    try:
        start = perf_counter()

        model_selected = ModelsAvailable.get(ModelsAvailable.id == id_model)
        result = prever(
            ticker=model_selected.ticker, model_name=model_selected.filename
        ).to_json(orient="records")

        end = perf_counter()
        duration = end - start

        ModelPredictionDuration.create(
            model_id=model_selected.id, start=start, duration=duration
        )

        return Response(content=result, media_type="application/json")
    except ModelsAvailable.DoesNotExist:
        raise HTTPException(status_code=404, detail="Modelo ainda nao treinado")
