from fastapi import FastAPI
from api.routes import health, model, predict, main

import uvicorn


app = FastAPI(title="API Pred yfinance")

router = [
    health.router,
    model.router,
    predict.router,
    main.router
]

for route in router:
    app.include_router(route)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)