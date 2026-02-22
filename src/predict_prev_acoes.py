import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import os
from datetime import datetime, timedelta

# Função para criar sequências
def criar_sequencias(dados, janela=90):
    X = []
    for i in range(janela, len(dados)):
        X.append(dados[i-janela:i, 0])
    return np.array(X)

def carregar_modelo(modelo_path_keras="models/modelo_lstm.keras",
                    modelo_path_h5="models/modelo_lstm.h5"):
    """
    Tenta carregar o modelo salvo em formato .keras (novo).
    Se não encontrar, tenta carregar em formato .h5 (legacy).
    """
    if os.path.exists(modelo_path_keras):
        print(f"Carregando modelo em formato Keras: {modelo_path_keras}")
        return tf.keras.models.load_model(modelo_path_keras)
    elif os.path.exists(modelo_path_h5):
        print(f"Carregando modelo em formato HDF5: {modelo_path_h5}")
        return tf.keras.models.load_model(modelo_path_h5)
    else:
        raise FileNotFoundError("Nenhum modelo encontrado em 'models/'.")

def prever(ticker: str, model_name: str, janela=90):
    # Coleta de dados recentes
    today = datetime.now()
    init_date = today - timedelta(days=365)
    dados = yf.download(ticker, start=init_date.strftime("%Y-%m-%d"), end=today.strftime("%Y-%m-%d"))
    precos = dados[['Close']].values

    # Normalização
    scaler = MinMaxScaler(feature_range=(0,1))
    precos_normalizados = scaler.fit_transform(precos)

    # Criar sequência para previsão
    X_input = criar_sequencias(precos_normalizados, janela=janela)
    X_input = np.reshape(X_input, (X_input.shape[0], X_input.shape[1], 1))

    # Carregar modelo
    modelo = carregar_modelo(model_name)

    # Fazer previsão
    y_pred = modelo.predict(X_input)

    # Reverter normalização
    y_pred_real = scaler.inverse_transform(y_pred)

    # Retornar DataFrame com previsões
    new_dates = [(dados.index[-1] + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, len(y_pred_real) + 1)]
    resultados = pd.DataFrame({
        "Data": new_dates,
        "Preco_Previsto": y_pred_real.flatten()
    })

    return resultados

if __name__ == "__main__":
    previsoes = prever("ITUB4.SA")
    # print(previsoes.head().to_json(orient="records"))
    print(previsoes.tail())