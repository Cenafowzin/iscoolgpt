# 🎓 IsCoolGPT - Assistente Virtual de Estudos

Um assistente inteligente para estudos que utiliza o **Google Gemini AI** para fornecer explicações, gerar perguntas, criar planos de estudo e muito mais. Totalmente otimizado para **produção** com deploy automatizado na **AWS ECS**.

## ✨ Funcionalidades

- **📚 Geração de Conteúdo**: Crie conteúdo educativo sobre qualquer tópico
- **💡 Explicações Detalhadas**: Obtenha explicações claras de conceitos complexos  
- **❓ Geração de Questões**: Gere perguntas para testar conhecimento
- **📋 Planos de Estudo**: Crie cronogramas personalizados de estudo
- **📝 Resumos**: Resuma textos longos de forma eficiente
- **🔒 API Segura**: Health checks, validação e rate limiting
- **📊 Monitoramento**: Logs estruturados e métricas integradas

## 🚀 Como Usar

### Pré-requisitos
- Python 3.11+
- Chave da API do Google Gemini

### Instalação Rápida

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Cenafowzin/iscoolgpt.git
   cd iscoolgpt/backend
   ```

2. **Configure a chave da API:**
   ```bash
   copy .env.example .env
   ```
   Edite o arquivo `.env` e adicione sua chave:
   ```
   GOOGLE_API_KEY=sua_chave_aqui
   ```

3. **Instale as dependências:**
   ```bash
   # Produção
   pip install -r requirements.txt
   
   # Desenvolvimento (inclui ferramentas de teste)
   pip install -r requirements-dev.txt
   ```

4. **Execute a aplicação:**
   ```bash
   # Windows (script automatizado)
   .\start.bat

   # Manual (qualquer SO)
   uvicorn app.main:app --reload
   ```

A API estará disponível em: `http://localhost:8000`

## 🔗 API Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Página inicial com informações da API |
| `/health` | GET | Health check para monitoramento |
| `/generate` | POST | Gera conteúdo educativo personalizado |
| `/explain` | POST | Explica conceitos de forma didática |
| `/generate-question` | POST | Cria perguntas de estudo |
| `/study-plan` | POST | Monta planos de estudo estruturados |
| `/summarize` | POST | Resume textos longos |

**📖 Documentação Interativa:** `http://localhost:8000/docs`

## 🏗️ Arquitetura

### **Stack Técnico:**
- **Backend**: FastAPI (Python 3.11)
- **IA**: Google Gemini 2.0 Flash Lite
- **Deploy**: AWS ECS Fargate 
- **CI/CD**: GitHub Actions
- **Monitoring**: AWS CloudWatch
- **Security**: AWS Parameter Store

### **Estrutura do Projeto:**
```
iscoolgpt/
├── .github/workflows/     # CI/CD automático
│   ├── build.yml         # Build e testes
│   ├── test.yml          # Testes abrangentes  
│   └── deploy.yml        # Deploy AWS ECS
├── backend/              # Aplicação FastAPI
│   ├── app/
│   │   ├── main.py      # API principal
│   │   └── config.py    # Configurações
│   ├── tests/           # Testes automatizados
│   └── dockerfile       # Container Docker
├── deployment/          # Scripts de infraestrutura
│   ├── setup-ecs.ps1   # Setup automático AWS
│   └── ECS-README.md    # Guia detalhado
└── README.md           # Este arquivo
```

## 🧪 Testes

### 🛡️ CI/CD Otimizado (Zero Tokens)
O projeto usa **testes inteligentes** que nunca consomem tokens da API:
```bash
cd backend
python ci_test.py
```

### ⚡ Testes Locais Completos
Para testes com integração real:
```bash
cd backend  
pytest tests/
```

### 📋 Arquitetura de Testes:
- **CI/CD**: Valida estrutura, endpoints e lógica sem consumir API
- **Locais**: Integração completa com Gemini AI
- **GitHub Actions**: Executa automaticamente em cada push/PR

## 🚀 Deploy na AWS

### ☁️ **Produção (AWS ECS - Recomendado)**

**Configurado para deploy automático e escalável:**

#### **Setup Inicial (Uma vez só):**
```bash
# 1. Configure AWS CLI
aws configure

# 2. Execute script de configuração automática
cd deployment
./setup-ecs.ps1 -GoogleApiKey "SUA-GOOGLE-API-KEY"
```

#### **Deploy Automático:**
```bash
# Push para main = deploy automático!
git push origin main

# Monitorar deploy:
# GitHub: https://github.com/Cenafowzin/iscoolgpt/actions
# AWS: https://sa-east-1.console.aws.amazon.com/ecs/
```

### 🏗️ **Infraestrutura AWS:**
- **ECS Fargate**: Containers gerenciados (sem servidor)
- **ECR**: Registry privado para Docker images
- **CloudWatch**: Logs e monitoramento 
- **Parameter Store**: Secrets seguros
- **Auto Scaling**: Escala conforme demanda

### 🔧 **Secrets Necessários (GitHub):**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

*Demais configurações estão no workflow!*

### 💰 **Custo Estimado:**
- **Fargate**: ~$10-15/mês
- **CloudWatch**: ~$2-5/mês
- **Total**: ~$15-20/mês

## 📊 Monitoramento e Logs

### **Em Produção (AWS):**
```bash
# Ver logs em tempo real
aws logs tail /ecs/iscoolgpt --follow --region sa-east-1

# Status do service
aws ecs describe-services --cluster iscoolgpt-cluster --services iscoolgpt-service --region sa-east-1

# Métricas no console
# https://sa-east-1.console.aws.amazon.com/cloudwatch/
```

### **Desenvolvimento Local:**
```bash
# Logs detalhados
LOG_LEVEL=DEBUG uvicorn app.main:app --reload

# Health check
curl http://localhost:8000/health
```

## 🛠️ Desenvolvimento

### **Setup de Desenvolvimento:**
```bash
# Clone e configure
git clone https://github.com/Cenafowzin/iscoolgpt.git
cd iscoolgpt/backend
cp .env.example .env

# Instale dependências de desenvolvimento
pip install -r requirements-dev.txt

# Execute com hot reload
uvicorn app.main:app --reload

# Testes locais
pytest tests/
```

### **Contribuir para o Projeto:**
1. **Fork** o repositório
2. **Clone** seu fork: `git clone https://github.com/SEU-USUARIO/iscoolgpt.git`
3. **Branch** para feature: `git checkout -b feature/nova-funcionalidade`
4. **Desenvolva** e teste localmente
5. **Commit**: `git commit -m 'feat: adiciona nova funcionalidade'`
6. **Push**: `git push origin feature/nova-funcionalidade`
7. **Pull Request** no GitHub

## 🔗 Links Úteis

- **🚀 Deploy Status**: [GitHub Actions](https://github.com/Cenafowzin/iscoolgpt/actions)
- **☁️ AWS Console**: [ECS Dashboard](https://sa-east-1.console.aws.amazon.com/ecs/)
- **📊 Logs**: [CloudWatch](https://sa-east-1.console.aws.amazon.com/cloudwatch/)
- **🔑 Google AI**: [Obter API Key](https://makersuite.google.com/app/apikey)
- **📖 FastAPI Docs**: [Swagger UI](http://localhost:8000/docs)

## 📄 Licença

Este projeto está sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">

**🎓 IsCoolGPT**

*Feito com ❤️ para estudantes que querem aprender mais e melhor!*

[![Deploy Status](https://img.shields.io/github/actions/workflow/status/Cenafowzin/iscoolgpt/deploy.yml?branch=main&label=Deploy&logo=amazon-aws)](https://github.com/Cenafowzin/iscoolgpt/actions)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![AWS](https://img.shields.io/badge/AWS-ECS-orange?logo=amazon-aws)](https://aws.amazon.com/ecs/)

</div>
