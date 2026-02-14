from datetime import date

from pydantic import BaseModel


class ParametersToTrain(BaseModel):
    ticker: str
    start: date
    end: date
    janela: int
    epochs: int
    batch: int = 32
    patience: int = 4