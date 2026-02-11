import argparse
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tensorflow as tf
from tensorflow.keras import Input, Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import os

def criar_sequencias(dados, janela=90):
    X, y = [], []
    for i in range(janela, len(dados)):
        X.append(dados[i-janela:i, 0])
        y.append(dados[i, 0])
    return np.array(X), np.array(y)

def main(args):
    # parâmetros vindos da linha de comando ou API
    ticker = args.ticker
    start_date = args.start
    end_date = args.end
    janela_dias = args.janela
    epocas = args.epochs
    batchsize = args.batch

    print(f"Treinando modelo para {ticker} de {start_date} até {end_date}")

    # 1. Coleta de dados
    dados = yf.download(ticker, start=start_date, end=end_date)
    precos = dados[['Close']].values

    # 2. Normalização
    scaler = MinMaxScaler(feature_range=(0,1))
    precos_normalizados = scaler.fit_transform(precos)

    # 3. Criar sequências
    X, y = criar_sequencias(precos_normalizados, janela=janela_dias)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # 4. Split treino/teste
    tamanho_treino = int(len(X) * 0.8)
    X_train, X_test = X[:tamanho_treino], X[tamanho_treino:]
    y_train, y_test = y[:tamanho_treino], y[tamanho_treino:]

    # 5. Modelo LSTM
    modelo = Sequential([
        Input(shape=(X_train.shape[1], 1)),
        LSTM(units=50, return_sequences=True),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=1)
    ])
    modelo.compile(optimizer='adam', loss='mean_squared_error')

    # 6. Treinamento
    early_stop = EarlyStopping(monitor='val_loss', patience=args.patience, restore_best_weights=True)
    modelo.fit(X_train, y_train,
               epochs=epocas,
               batch_size=batchsize,
               validation_data=(X_test, y_test),
               callbacks=[early_stop])

    # 7. Salvar modelo
    os.makedirs("models", exist_ok=True)
    modelo.save(f"models/modelo_{ticker}.keras")
    print(f"Modelo salvo em models/modelo_{ticker}.keras")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Treinar modelo LSTM para previsão de preços")
    parser.add_argument("--ticker", type=str, default="ITUB4.SA", help="Código do ativo")
    parser.add_argument("--start", type=str, default="2024-01-01", help="Data inicial")
    parser.add_argument("--end", type=str, default="2025-12-31", help="Data final")
    parser.add_argument("--janela", type=int, default=90, help="Tamanho da janela de dias")
    parser.add_argument("--epochs", type=int, default=40, help="Número de épocas")
    parser.add_argument("--batch", type=int, default=32, help="Tamanho do batch")
    parser.add_argument("--patience", type=int, default=4, help="Número de épocas sem melhora antes de parar o treino")
    args = parser.parse_args()

    main(args)