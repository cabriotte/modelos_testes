# Previsão de Preços com LSTM

Este projeto utiliza **redes neurais recorrentes (LSTM)** para prever preços de ativos financeiros com base em dados históricos coletados via **Yahoo Finance**.

---

## 📌 Etapa 1: Coleta e Pré-processamento dos Dados

### Bibliotecas utilizadas
- **yfinance** → coleta de dados financeiros (ações, índices, moedas).
- **pandas** → manipulação de dados em tabelas (DataFrames).
- **numpy** → operações matemáticas e manipulação de arrays.
- **matplotlib.pyplot** → visualização gráfica dos dados.
- **MinMaxScaler (scikit-learn)** → normalização dos valores para uma escala entre 0 e 1.

### Coleta de dados
- `yf.download()` baixa os preços históricos da ação escolhida.
- **Parâmetros**:
  - `ticker`: código da ação (ex.: `"AAPL"`, `"ITUB4.SA"`, `"PETR4.SA"`).
  - `start` e `end`: intervalo de datas.
- Resultado: DataFrame com colunas `Open`, `High`, `Low`, `Close`, `Volume`.

Selecionamos apenas o **preço de fechamento (Close)**, transformado em array NumPy (`.values`).

### Normalização
- O **MinMaxScaler** ajusta os valores para a faixa entre 0 e 1.
- Isso evita que valores muito grandes ou pequenos prejudiquem o treinamento.
- `fit_transform` aplica a normalização sobre os preços coletados.

📊 Um gráfico é gerado mostrando a evolução dos preços normalizados.

---

## 📌 Etapa 2: Criação das Sequências

### Função `criar_sequencias`
- Recebe os dados normalizados e o tamanho da janela (número de dias usados como histórico).
- Para cada posição `i`:
  - `X.append(dados[i-janela:i, 0])` → últimos **XX dias** como entrada.
  - `y.append(dados[i, 0])` → preço do dia seguinte como saída.
- Retorna:
  - `X` → conjunto de sequências (inputs).
  - `y` → valores alvo (outputs).

### Ajuste de formato para LSTM
O LSTM espera os dados no formato:
- **samples** → número de sequências criadas.
- **timesteps** → tamanho da janela (XX dias).
- **features** → número de variáveis por dia (nesse caso, apenas 1: preço de fechamento).

Exemplo:  
`X: (3000, 90, 1)` → 3000 amostras, cada uma com 90 dias e 1 feature.  
`y: (3000,)`

---

## 📌 Etapa 3: Construção e Treinamento do Modelo

### Arquitetura
- **Sequential** → modelo sequencial.
- **Input** → formato da entrada (janela, 1 feature).
- **LSTM (50 neurônios)** → primeira camada, retorna sequências.
- **Dropout (0.2)** → desliga 20% dos neurônios aleatoriamente.
- **LSTM (50 neurônios)** → segunda camada, retorna apenas o último estado.
- **Dense (1)** → camada de saída, gera o preço previsto.

### Configuração
- **Otimizador**: Adam  
- **Loss**: MSE (erro quadrático médio)  
- **Divisão dos dados**:  
  - 80% treino  
  - 20% teste  

### Treinamento
- `epochs=XX` → número de vezes que o modelo percorre todo o conjunto de treino.  
- `batch_size=XX` → número de amostras processadas por vez.  
- `validation_data` → avalia desempenho em dados de teste.  
- `EarlyStopping` → interrompe treino se não houver melhora.

---

## 📌 Etapa 4: Avaliação do Modelo

### Previsões
- `y_pred` → previsões do modelo.
- `inverse_transform` → reverte normalização para comparar com preços reais.

### Métricas
- **MAE (Mean Absolute Error)** → erro médio absoluto.  
- **RMSE (Root Mean Squared Error)** → raiz do erro quadrático médio.  
- **MAPE (Mean Absolute Percentage Error)** → erro percentual médio.  

#### Interpretação
- **MAE** → erro médio em reais, fácil de interpretar.  
- **RMSE** → dá mais peso a erros grandes.  
- **MAPE** → mostra erro percentual médio, intuitivo para análise.  

---

## 📊 Resultados
- Gráfico comparando preços reais vs previstos.  
- Tabela detalhada com valores reais, previstos e diferença percentual.  
- Tabela agrupada por intervalos de dias com métricas (MAE, RMSE, MAPE).  

---

## ⚙️ Dependências
- TensorFlow  
- NumPy  
- Pandas  
- Scikit-learn  
- Matplotlib  
- yfinance  
- tabulate  

---

## 🚀 Como usar
1. **Treinar modelo**:
   ```bash
   python src/train_prev_acoes.py --ticker ITUB4.SA --start 2024-01-01 --end 2025-12-31 --janela 90 --epochs 40 --batch 32
   ```

2. **Fazer previsões**:
   ```bash
   python src/predict_prev_acoes.py
   ```

3. **Executar API**:
   ```bash
   # Localmente
   uvicorn api.main:app --reload
   
   # Com Docker
   docker-compose up -d
   ```

4. **Acessar documentação da API**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

## 🌐 Usando a API

### Exemplos com curl

**Health Check**
```bash
curl http://localhost:8000/health
```

**Listar modelos disponíveis**
```bash
curl http://localhost:8000/models
```

**Obter previsões**
```bash
curl http://localhost:8000/predict/ITUB4.SA?janela=90
```

**Treinar novo modelo**
```bash
curl -X POST http://localhost:8000/train_model \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "start": "2024-01-01",
    "end": "2025-12-31",
    "janela": 90,
    "epochs": 40,
    "batch": 32,
    "patience": 4
  }'
```

### Exemplo com Python

```python
import requests

# Fazer previsão
response = requests.get("http://localhost:8000/predict/ITUB4.SA?janela=90")
print(response.json())

# Treinar modelo
data = {
    "ticker": "PETR4.SA",
    "start": "2024-01-01",
    "end": "2025-12-31",
    "janela": 90,
    "epochs": 40,
    "batch": 32,
    "patience": 4
}
response = requests.post("http://localhost:8000/train_model", json=data)
print(response.json())
```

---

## 📚 Documentação Adicional

- **[AVALIACAO.md](AVALIACAO.md)** - Avaliação completa do projeto (Nota: 84/90)
- **[DEPLOY.md](DEPLOY.md)** - Guia completo de deploy (Local, AWS, GCP, Azure)

---

## 🐳 Deploy com Docker

```bash
# Build e executar
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

---

## 📊 Estrutura do Projeto

```
modelos_testes/
├── api/                    # API FastAPI
│   ├── main.py            # Endpoints da API
│   └── schemas/           # Schemas Pydantic
├── src/                   # Scripts de treinamento e previsão
│   ├── train_prev_acoes.py
│   └── predict_prev_acoes.py
├── models/                # Modelos treinados (.keras)
├── videos/                # Vídeo demonstrativo
├── Dockerfile            # Container da API
├── docker-compose.yml    # Orquestração
├── requirements.txt      # Dependências Python
├── README.md            # Este arquivo
├── AVALIACAO.md         # Avaliação do projeto
└── DEPLOY.md            # Guia de deploy
```