# Guia de Deploy - API de Previsão de Ações

## 🐳 Deploy com Docker (Recomendado)

### Pré-requisitos
- Docker instalado (versão 20.10+)
- Docker Compose instalado (versão 2.0+)

### Passos para Deploy Local

1. **Clone o repositório**
```bash
git clone https://github.com/cabriotte/modelos_testes.git
cd modelos_testes
```

2. **Build e execução com Docker Compose**
```bash
docker-compose up -d --build
```

3. **Verificar se a API está rodando**
```bash
curl http://localhost:8000/health
```

4. **Acessar documentação interativa**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Comandos Úteis

**Ver logs**
```bash
docker-compose logs -f api
```

**Parar a API**
```bash
docker-compose down
```

**Reiniciar a API**
```bash
docker-compose restart
```

---

## ☁️ Deploy em Nuvem

### AWS (Amazon Web Services)

#### Opção 1: AWS ECS (Elastic Container Service)

1. **Criar repositório ECR**
```bash
aws ecr create-repository --repository-name lstm-stock-api
```

2. **Build e push da imagem**
```bash
# Login no ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <sua-conta>.dkr.ecr.us-east-1.amazonaws.com

# Build da imagem
docker build -t lstm-stock-api .

# Tag da imagem
docker tag lstm-stock-api:latest <sua-conta>.dkr.ecr.us-east-1.amazonaws.com/lstm-stock-api:latest

# Push da imagem
docker push <sua-conta>.dkr.ecr.us-east-1.amazonaws.com/lstm-stock-api:latest
```

3. **Criar task definition no ECS**
4. **Criar serviço ECS**
5. **Configurar Load Balancer**

#### Opção 2: AWS EC2

1. **Criar instância EC2** (recomendado: t3.medium ou superior)
2. **Instalar Docker na instância**
```bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
```

3. **Clonar repositório e executar**
```bash
git clone https://github.com/cabriotte/modelos_testes.git
cd modelos_testes
docker-compose up -d
```

4. **Configurar Security Group** (abrir porta 8000)

---

### Google Cloud Platform (GCP)

#### Cloud Run (Serverless)

1. **Build da imagem com Cloud Build**
```bash
gcloud builds submit --tag gcr.io/[PROJECT-ID]/lstm-stock-api
```

2. **Deploy no Cloud Run**
```bash
gcloud run deploy lstm-stock-api \
  --image gcr.io/[PROJECT-ID]/lstm-stock-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Google Kubernetes Engine (GKE)

1. **Criar cluster**
```bash
gcloud container clusters create lstm-cluster --num-nodes=2
```

2. **Deploy com kubectl**
```bash
kubectl create deployment lstm-api --image=gcr.io/[PROJECT-ID]/lstm-stock-api
kubectl expose deployment lstm-api --type=LoadBalancer --port=80 --target-port=8000
```

---

### Azure

#### Azure Container Instances

1. **Login no Azure**
```bash
az login
```

2. **Criar resource group**
```bash
az group create --name lstm-rg --location eastus
```

3. **Deploy do container**
```bash
az container create \
  --resource-group lstm-rg \
  --name lstm-stock-api \
  --image <sua-imagem> \
  --dns-name-label lstm-api \
  --ports 8000
```

---

## 🚀 Deploy em Plataformas Serverless

### Render

1. Conectar repositório GitHub no Render
2. Selecionar "Web Service"
3. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
4. Deploy automático a cada push

### Railway

1. Conectar repositório no Railway
2. Railway detecta automaticamente o Dockerfile
3. Deploy automático configurado

### Fly.io

1. **Instalar flyctl**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login**
```bash
fly auth login
```

3. **Launch app**
```bash
fly launch
```

4. **Deploy**
```bash
fly deploy
```

---

## 📊 Monitoramento em Produção

### Logs

**Docker Compose**
```bash
docker-compose logs -f api
```

**Cloud Run (GCP)**
```bash
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

### Métricas

A API expõe o header `X-Process-Time` em cada resposta para tracking de performance.

### Health Check

Endpoint disponível em `/health` para verificação de status.

---

## 🔐 Segurança

### Variáveis de Ambiente

Crie um arquivo `.env` para variáveis sensíveis:

```env
API_KEY=sua-chave-secreta
DEBUG=false
```

### HTTPS

Em produção, sempre use HTTPS:
- Configure certificado SSL/TLS
- Use serviços como Let's Encrypt
- Em cloud providers, use Load Balancers com SSL

---

## 🧪 Testando a API em Produção

### Health Check
```bash
curl https://sua-api.com/health
```

### Listar Modelos
```bash
curl https://sua-api.com/models
```

### Fazer Previsão
```bash
curl https://sua-api.com/predict/ITUB4.SA?janela=90
```

### Treinar Novo Modelo
```bash
curl -X POST https://sua-api.com/train_model \
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

---

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs: `docker-compose logs -f`
2. Verifique o health check: `curl http://localhost:8000/health`
3. Abra uma issue no GitHub
