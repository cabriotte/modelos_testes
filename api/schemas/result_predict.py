from pydantic import BaseModel


class ResultPredict(BaseModel):
    Data: str
    Preco_Previsto: float