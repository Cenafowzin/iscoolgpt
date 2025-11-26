# 🎓 IsCoolGPT - Assistente Virtual de Estudos

Um assistente inteligente para estudos que utiliza o Google Gemini AI para fornecer explicações, gerar perguntas, criar planos de estudo e muito mais.

## ✨ Funcionalidades

- **📚 Geração de Conteúdo**: Crie conteúdo educativo sobre qualquer tópico
- **💡 Explicações Detalhadas**: Obtenha explicações claras de conceitos complexos  
- **❓ Geração de Questões**: Gere perguntas para testar conhecimento
- **📋 Planos de Estudo**: Crie cronogramas personalizados de estudo
- **📝 Resumos**: Resuma textos longos de forma eficiente

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

## 🔗 Endpoints da API

- `POST /generate` - Gera conteúdo educativo
- `POST /explain` - Explica conceitos
- `POST /generate-question` - Gera perguntas
- `POST /study-plan` - Cria planos de estudo
- `POST /summarize` - Resume textos

Documentação interativa: `http://localhost:8000/docs`

## 🧪 Testes

### 🛡️ Testes Seguros (Sem Consumir Tokens)
Perfeito para CI/CD e desenvolvimento:
```bash
cd backend
python tests/test_safe.py
```

### ⚡ Testes Completos (Consome Tokens)  
Apenas quando necessário:
```bash
cd backend
python tests/test_safe.py full
```

### 📋 O que cada tipo testa:
- **Seguros**: Endpoints básicos, validação de dados, performance
- **Completos**: Integração real com Gemini AI (usa seus tokens)

## 📦 Deploy

### 🚀 Deploy Seguro (Recomendado)
O projeto está configurado para **NUNCA consumir tokens** durante CI/CD:

```bash
# GitHub Actions executa automaticamente
python tests/test_safe.py
```

### 🌐 Plataformas Suportadas
- **Heroku**: Configure `GOOGLE_API_KEY` nas variáveis de ambiente
- **Railway**: Faça deploy da pasta `backend/`
- **Vercel**: Configure como projeto Node.js/Python
- **AWS/Azure**: Use container Docker

### 🔧 Variáveis de Ambiente
```env
GOOGLE_API_KEY=sua_chave_aqui  # Obrigatório
PORT=8000                      # Opcional
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

---

Feito com ❤️ para estudantes que querem aprender mais e melhor!