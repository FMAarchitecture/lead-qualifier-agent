# lead-qualifier-agent-fma

Agente de **qualificação de leads residenciais** da **Fernanda Marques Arquitetura**, construído em **FastAPI** e orquestrado via **Docker/Portainer**, integrado com **Gemini (Google Generative AI)** para análise textual e com **SerpAPI** para busca na web.  
O agente recebe eventos do **Monday.com** (via **Make**), pesquisa a fundo *quem é a pessoa física*, analisa o potencial, atribui um **score** e gera um **resumo em HTML** pronto para e-mail.

---

## Objetivo

- Focar exclusivamente em **leads residenciais (pessoa física)**.  
- Não qualificar **incorporadoras/construtoras/imobiliárias**.  
- Pesquisar profundamente o lead PF (indícios em redes sociais, notícias, menções, contexto).  
- Retornar **pesquisa**, **análise**, **nota (0–100)** e **resumo HTML** para uso interno/CRM/e-mail.

---

## Visão geral de arquitetura

```
Monday.com → Make (filtro Segmento=Residencial) → HTTP POST → FastAPI (/webhook)
│
├─ web_search.py (SerpAPI)
├─ agents.py (prompts + Gemini)
└─ resposta JSON (pesquisa/analise/score/resumo_html)
```

**Deploy**: imagem Docker publicada em `tifma/lead-qualifier-agent:latest`  
**Orquestração**: Portainer (stack com `docker-compose`)  
**Domínio**: https://agente.fernandamarques.com.br  
**Swagger**: `/docs`

---

## Tech stack

- Python 3.11  
- FastAPI  
- Uvicorn  
- google-generativeai (Gemini: `models/gemini-2.5-flash`)  
- requests (integrações HTTP/SerpAPI)  
- Docker e Portainer  
- SerpAPI  
- Make.com + Monday.com

---

## Estrutura do repositório

```
├─ agents.py # Orquestra prompts e chamadas ao Gemini
├─ web_search.py # Função search_web() via SerpAPI
├─ main.py # App FastAPI: rotas / e /webhook
├─ requirements.txt # Dependências Python
├─ Dockerfile # Build da imagem
├─ docker-compose.yml # Stack de produção (Portainer)
└─ README.md # Este documento
```


### agents.py

- `MODEL_NAME = "models/gemini-2.5-flash"`  
- `call_llm(prompt)`: camada de chamada ao Gemini (com logs de debug).  
- `researcher_agent(data)`:  
  - Busca web focada em residencial, evitando “incorporadora|construtora|imobiliária”.  
  - Prompt investigativo para PF (nome completo, cidade, profissão, redes, menções, lifestyle).  
  - Retorna resumo de pesquisa de até 8 linhas.  
- `lead_analyst_agent(data, pesquisa)`:  
  - Confirma se o lead é PF.  
  - Avalia alinhamento ao público de alta renda e capacidade financeira.  
  - Rejeita perfis ligados à incorporação.  
- `lead_scoring_specialist_agent(data, pesquisa, analise)`:  
  - Atribui nota de 0–100 com justificativa clara.  
  - Pesa mais sinais de PF de alta renda e estilo de vida compatível.  
- `summarizer_agent(data, pesquisa, analise, score)`:  
  - Gera HTML limpo, pronto para envio por e-mail.

### web_search.py

- `search_web(query: str)` utilizando **SERPAPI_API_KEY**.  
- Retorna resultados com `title`, `link`, `snippet`.  
- Importante: **não incluir** `from web_search import search_web` no topo (evita import circular).

### main.py

- `GET /` → healthcheck.  
- `POST /webhook` → recebe payload do Monday/Make, executa pipeline de agentes e retorna:
  ```json
  {
    "pesquisa": "...",
    "analise": "...",
    "score": "Nota (0 a 100): ...\nJustificativa: ...",
    "resumo_html": "<h2>...</h2>..."
  }
- Swagger em /docs.

---

## Variáveis de ambiente

Configurar no .env local ou nas variáveis do Portainer:
```
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
SERPAPI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxx
PORT=5000
```

---

## Rodando localmente
```
python -m venv .venv
. .venv/Scripts/activate   # Windows
# ou source .venv/bin/activate (Linux/Mac)
pip install -r requirements.txt
```

---

## Docker (build e push)
```
docker build -t tifma/lead-qualifier-agent:latest .
docker push tifma/lead-qualifier-agent:latest
```

## Deploy no Portainer

Exemplo de stack (docker-compose.yml):
```
version: "3.9"
services:
  lead-qualifier-agent-fma:
    image: tifma/lead-qualifier-agent:latest
    container_name: lead-qualifier-agent-fma
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - SERPAPI_API_KEY=${SERPAPI_API_KEY}
      - PORT=5000
    ports:
      - "5000:5000"
    restart: unless-stopped
```

Atualização:
- Stacks → lead-qualifier-agent-fma → Recreate → Pull latest image → Recreate.

## Integração Make + Monday
### Fluxo:
monday.com (Get an Item) → Filtro (Limitação de Segmento) → HTTP (Make a request).

### Filtro (somente Residencial):
- Campo: Segmento → Text
- Operador: Contains
- Valor: residencial

### Módulo HTTP:
- Método: POST
- URL: https://agente.fernandamarques.com.br/webhook
- Body:
  ```
  {
  "event": {
    "pulseName": "João Mendes",
    "columnValues": [
      { "id": "text", "text": "João Mendes" },
      { "id": "lead_company", "text": "Particular" },
      { "id": "text_mkt34gy1", "text": "Residencial" },
      { "id": "text_mkt3fj76", "text": "Casa de alto padrão" },
      { "id": "text_mkt3nf19", "text": "3 a 5 funcionários" }
    ]
  }
}```

## Endpoints:
GET /
  Retorna status do serviço.

POST /webhook
  Executa pipeline de qualificação.

Resposta:
```
{
  "pesquisa": "string",
  "analise": "string",
  "score": "Nota (0 a 100): 85\nJustificativa: ...",
  "resumo_html": "<h2>Resumo de Qualificação</h2>..."
}
```

## Regras de Qualificação:
- Apenas leads residenciais (PF).
- Ignora incorporadoras, construtoras, imobiliárias.
- Busca investigativa PF (nome, cidade, profissão, redes, notícias, blogs, eventos, registros públicos).
- Faz inferências contextuais quando há poucos dados.
- Score de 0–100 pondera alta renda e estilo de vida compatível.

## Segurança:
- Não expor chaves (GEMINI_API_KEY, SERPAPI_API_KEY).
- Não registrar dados sensíveis nos logs.
- Respostas HTML são apenas para uso interno.

## Troubleshooting:

1. Docker Engine não rodando (Windows)
  ```
  open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified
  ```
  - Abra Docker Desktop e aguarde “Docker is running”.

2. Import circular
   ```
   ImportError: cannot import name 'search_web'
   ```
  - Remover from web_search import search_web de dentro do arquivo web_search.py.

3. Modelo Gemini inválido
   ```
   404 models/gemini-1.5-flash-latest not found
   ```
  - Usar models/gemini-2.5-flash.

4. Porta inacessível
   - Confirmar ports: "5000:5000" no compose.
   - Acessar via http://<IP_SERVIDOR>:5000/docs ou domínio configurado.
  
5. Filtro Make não aciona:
   - Campo correto: Segmento → Text com Contains = residencial.

## Testes:
### Swagger:
https://agente.fernandamarques.com.br/docs

Curl:
```
curl -X POST "https://agente.fernandamarques.com.br/webhook" \
  -H "Content-Type: application/json" \
  -d '{"event":{"pulseName":"João Mendes","columnValues":[{"id":"text","text":"João Mendes"},{"id":"text_mkt34gy1","text":"Residencial"},{"id":"text_mkt3fj76","text":"Casa de alto padrão"}]}}'
```

