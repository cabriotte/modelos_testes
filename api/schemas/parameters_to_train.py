from datetime import date, datetime

from pydantic import BaseModel


class ParametersToTrain(BaseModel):
    ticker: str
    start: date
    end: date
    janela: int = 90
    epochs: int = 40
    batch: int = 32
    patience: int = 4

class ModelData(BaseModel):
    id: int
    ticker: str
    created_at: datetime
    time_series_used: str
    janela: int
    epochs: int
    batch: int
    patience: int
    activated: bool
    filename: str