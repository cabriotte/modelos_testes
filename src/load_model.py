import argparse
import tensorflow as tf
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from datetime import datetime

def calcular_metricas_intervalo(y_real, y_prev, inicio, fim):
    y_r = y_real[inicio:fim]
    y_p = y_prev[inicio:fim]
    if len(y_r) == 0 or len(y_p) == 0:
        return None, None, None
    mae = mean_absolute_error(y_r, y_p)
    rmse = np.sqrt(mean_squared_error(y_r, y_p))
    mape = np.mean(np.abs((y_r - y_p) / y_r)) * 100
    return mae, rmse, mape

def gerar_metricas_por_intervalo(y_real, y_prev, tamanho_bloco=30):
    resultados = []
    n = len(y_real)
    for i in range(0, n, tamanho_bloco):
        fim = min(i + tamanho_bloco, n)
        mae, rmse, mape = calcular_metricas_intervalo(y_real, y_prev, i, fim)
        if mae is not None:
            resultados.append([
                f"Dias {i+1}–{fim} ({fim-i} amostras)",
                round(mae,3),
                round(rmse,3),
                round(mape,3)
            ])
    return pd.DataFrame(resultados, columns=["Intervalo", "MAE", "RMSE", "MAPE (%)"])

def main(args):
    modelo_path = args.modelo
    ticker = args.ticker  # só para coletar dados atuais
    print(f"Carregando modelo de {modelo_path} e avaliando {ticker}")

    # Carregar modelo
    modelo = tf.keras.models.load_model(modelo_path)

    # Coletar dados recentes
    dados = yf.download(ticker, start="2025-01-01", end="2025-12-31")
    precos = dados[['Close']].values

    # Normalizar
    scaler = MinMaxScaler(feature_range=(0,1))
    precos_normalizados = scaler.fit_transform(precos)

    # Criar sequências (janela fixa de 90 dias)
    janela = 90
    X, y = [], []
    for i in range(janela, len(precos_normalizados)):
        X.append(precos_normalizados[i-janela:i, 0])
        y.append(precos_normalizados[i, 0])
    X = np.array(X)
    y = np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Previsão
    y_pred = modelo.predict(X)
    y_test_real = scaler.inverse_transform(y.reshape(-1,1))
    y_pred_real = scaler.inverse_transform(y_pred)

    # Métricas globais
    mae = mean_absolute_error(y_test_real, y_pred_real)
    rmse = np.sqrt(mean_squared_error(y_test_real, y_pred_real))
    mape = np.mean(np.abs((y_test_real - y_pred_real) / y_test_real)) * 100
    print(f"Métricas globais: MAE={mae:.3f}, RMSE={rmse:.3f}, MAPE={mape:.2f}%")

    # Gráfico
    plt.figure(figsize=(12,4))
    plt.plot(y_test_real, label="Preço Real")
    plt.plot(y_pred_real, label="Preço Previsto")
    plt.title(f"Previsão de preços com LSTM - {ticker}")
    plt.xlabel("Dias")
    plt.ylabel("Preço")
    plt.legend()
    plt.show()

    # Tabela detalhada
    tabela_resultados = pd.DataFrame({
        "Data_Preco_Real": dados.index[-len(y_test_real):],
        "Preco_Real": y_test_real.flatten(),
        "Data_Atual": datetime.today().strftime("%Y-%m-%d"),
        "Preco_Previsto": y_pred_real.flatten()
    })
    tabela_resultados["Diferenca_%"] = ((tabela_resultados["Preco_Real"] - tabela_resultados["Preco_Previsto"])
                                        / tabela_resultados["Preco_Real"]) * 100
    tabela_resultados = tabela_resultados.round(3)

    fig, ax = plt.subplots(figsize=(12,6))
    ax.axis('off')
    ax.table(cellText=tabela_resultados.head(20).values,
             colLabels=tabela_resultados.columns,
             loc='center')
    plt.title("Tabela detalhada - Preços reais vs previstos")
    plt.show()

    # Tabela agrupada
    tabela_metricas = gerar_metricas_por_intervalo(y_test_real, y_pred_real, tamanho_bloco=30)
    fig, ax = plt.subplots(figsize=(8,4))
    ax.axis('off')
    ax.table(cellText=tabela_metricas.values,
             colLabels=tabela_metricas.columns,
             loc='center')
    plt.title("Métricas por intervalo")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualizar resultados de um modelo salvo")
    parser.add_argument("--modelo", type=str, required=True, help="Caminho do modelo salvo (.keras)")
    parser.add_argument("--ticker", type=str, default="ITUB4.SA", help="Ticker para coletar dados atuais")
    args = parser.parse_args()

    main(args)