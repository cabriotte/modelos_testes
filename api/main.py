import json
from typing import Dict
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from src.predict_prev_acoes import prever
from src.train_prev_acoes import main
from api.schemas.parameters_to_train import ParametersToTrain
import uvicorn

cache: Dict[str, str] = {

}

app = FastAPI(title="API Pred yfinance")
add_pagination(app)

@app.post("/health", tags=["Health"])
async def health():
    return {"status": "OK"}

@app.post(path="/train_model")
async def train_model(data: ParametersToTrain):
    """Forneça o nome da ação e as data que deseja usar como treinamento"""
    main(data)
    return dict(
        ticker=data.ticker,
        message="Modelo treinado com sucesso"
    )

@app.get(path="/predict")
async def get_result(ticker: str):
    """Informe o nome da ação para obter os resultados da previsão"""
    if ticker in cache:
        return JSONResponse(cache[ticker], status_code=200)
    else:
        try:
            result = prever(ticker).to_json(orient="records")
            cache[ticker] = json.loads(result)
            return JSONResponse(cache[ticker], status_code=200)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Modelo ainda nao treinado")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)