import json
import logging
import time
from typing import Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from src.predict_prev_acoes import prever
from src.train_prev_acoes import main
from api.schemas.parameters_to_train import ParametersToTrain
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

cache: Dict[str, str] = {}

app = FastAPI(
    title="API de Previsão de Ações com LSTM",
    description="API RESTful para treinar modelos LSTM e prever preços de ações usando dados do Yahoo Finance",
    version="1.0.0"
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log da requisição
    logger.info(f"Requisição recebida: {request.method} {request.url.path}")
    
    # Processar requisição
    response = await call_next(request)
    
    # Calcular tempo de processamento
    process_time = time.time() - start_time
    logger.info(f"Requisição concluída em {process_time:.2f}s - Status: {response.status_code}")
    
    # Adicionar header com tempo de processamento
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


@app.get("/health", tags=["Health"])
async def health():
    """
    Endpoint de health check para verificar se a API está funcionando.
    """
    return {"status": "OK", "message": "API está funcionando corretamente"}

@app.post(path="/train_model", tags=["Training"])
async def train_model(data: ParametersToTrain):
    """
    Treina um novo modelo LSTM para previsão de preços de ações.
    
    Parâmetros:
    - ticker: Código da ação (ex: ITUB4.SA, PETR4.SA, AAPL)
    - start: Data inicial para coleta de dados
    - end: Data final para coleta de dados
    - janela: Número de dias usados como histórico (default: 90)
    - epochs: Número de épocas de treinamento (default: 40)
    - batch: Tamanho do batch (default: 32)
    - patience: Paciência para early stopping (default: 4)
    """
    try:
        logger.info(f"Iniciando treinamento do modelo para {data.ticker}")
        main(data)
        logger.info(f"Modelo treinado com sucesso para {data.ticker}")
        
        # Limpar cache para este ticker
        if data.ticker in cache:
            del cache[data.ticker]
            
        return dict(ticker=data.ticker, message="Modelo treinado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao treinar modelo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao treinar modelo: {str(e)}")

@app.get(path="/predict/{ticker}", tags=["Prediction"])
async def get_result(ticker: str, janela: int = 90):
    """
    Obtém previsões de preços para uma ação específica.
    
    Parâmetros:
    - ticker: Código da ação (ex: ITUB4.SA, PETR4.SA, AAPL)
    - janela: Número de dias usados como histórico (default: 90)
    
    Retorna as primeiras 5 previsões em formato JSON.
    """
    cache_key = f"{ticker}_{janela}"
    
    if cache_key in cache:
        logger.info(f"Retornando previsão do cache para {ticker}")
        return JSONResponse(content=cache[cache_key], status_code=200)
    else:
        try:
            logger.info(f"Gerando previsão para {ticker}")
            result = prever(ticker, janela=janela).head().to_json(orient="records")
            cache[cache_key] = json.loads(result)
            logger.info(f"Previsão gerada com sucesso para {ticker}")
            return JSONResponse(content=cache[cache_key], status_code=200)
        except FileNotFoundError:
            logger.warning(f"Modelo não encontrado para {ticker}")
            raise HTTPException(status_code=404, detail=f"Modelo para {ticker} ainda não foi treinado. Use o endpoint /train_model primeiro.")
        except Exception as e:
            logger.error(f"Erro ao gerar previsão: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao gerar previsão: {str(e)}")

@app.get(path="/models", tags=["Models"])
async def list_models():
    """
    Lista todos os modelos treinados disponíveis.
    """
    import os
    models_dir = "models"
    
    if not os.path.exists(models_dir):
        return {"models": []}
    
    models = [f.replace("modelo_", "").replace(".keras", "") 
              for f in os.listdir(models_dir) 
              if f.startswith("modelo_") and f.endswith(".keras")]
    
    logger.info(f"Modelos disponíveis: {models}")
    return {"models": models, "count": len(models)}
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)