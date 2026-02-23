from fastapi import FastAPI
import uvicorn
import mlflow

from api.routes import health, model, predict, main, duration_stats

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("MLflow yfinance API")
mlflow.sklearn.autolog()
mlflow.tensorflow.autolog()

app = FastAPI(title="API Pred yfinance")

router = [
    health.router,
    model.router,
    predict.router,
    main.router,
    duration_stats.router,
]

for route in router:
    app.include_router(route)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
