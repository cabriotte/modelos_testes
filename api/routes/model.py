from datetime import datetime

from fastapi import HTTPException, APIRouter, status

from api.db.schemas.models_available import ModelsAvailable
from api.schemas.parameters_to_train import ModelData, ParametersToTrain
from src.train_prev_acoes import main

router = APIRouter(prefix="/model", tags=["Model"])

@router.post(path="/train")
async def train_model(data: ParametersToTrain):
    """Forneça o nome da ação e as data que deseja usar como treinamento"""
    try:
        file_name = main(data)
        ModelsAvailable(
            ticker=data.ticker,
            created_at=datetime.now(),
            time_series_used="{} á {}".format(data.start, data.end),
            janela=data.janela,
            epochs=data.epochs,
            batch=data.batch,
            patience=data.patience,
            filename=file_name
        ).save()
        return dict(ticker=data.ticker, message="Modelo treinado com sucesso")
    except ValueError:
        raise HTTPException(status_code=400, detail="Erro ao treinar o modelo")

@router.get(path="/list")
async def list_model_available():
    return [
        ModelData.model_validate(model) for model in ModelsAvailable.select().where(ModelsAvailable.activated == True).dicts()
    ]

@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def list_model_available(id: int):
    ModelsAvailable.update(activated=False).where(ModelsAvailable.id == id).execute()
    return 
