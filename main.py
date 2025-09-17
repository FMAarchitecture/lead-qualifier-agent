from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from agents import researcher_agent, lead_analyst_agent, lead_scoring_specialist_agent, summarizer_agent
from email_sender import send_email

app = FastAPI()

# Middleware para remover aviso de segurança do ngrok
@app.middleware("http")
async def add_ngrok_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

# Responde ao desafio do Monday.com com logs detalhados
@app.post("/")
async def root(request: Request):
    raw_body = await request.body()
    print("[MONDAY] RAW body:\n", raw_body.decode())

    try:
        json_body = await request.json()
        challenge = json_body.get("challenge")
        if challenge:
            print(f"[MONDAY] Desafio recebido: {challenge}")
            return PlainTextResponse(content=challenge, status_code=200)
    except Exception as e:
        print(f"[MONDAY] Erro ao decodificar JSON: {e}")

    return {"status": "ok"}

# Processa novos leads vindos do Monday.com
@app.post("/webhook")
async def handle_webhook(request: Request):
    body = await request.json()
    print("JSON recebido do Monday:\n", body)

    event = body.get("event", {})
    lead_name = event.get("pulseName", "Nome não encontrado")
    column_values = event.get("columnValues", [])

    # Busca o tipo de projeto entre as colunas
    project_type = "não informado"
    for col in column_values:
        if col.get("title", "").lower() in ["segmento", "tipo de projeto"]:
            project_type = col.get("text", "") or "não informado"

    # Monta os dados para os agentes
    lead_data = {
        "nome": lead_name,
        "segmento": project_type,
        "tipo_projeto": project_type
    }

    # Executa os agentes
    research = researcher_agent(lead_data)
    analysis = lead_analyst_agent(lead_data, research)
    score = lead_scoring_specialist_agent(lead_data, research, analysis)
    summary = summarizer_agent(lead_data, research, analysis, score)

    # Envia e-mail
    send_email(
        subject=f"Lead qualificado: {lead_data['nome']}",
        body=summary.strip(),
        to_email="laura.bueno@fernandamarques.com.br"
    )

    return {
        "pesquisa": research,
        "analise": analysis,
        "score": score,
        "resumo": summary.strip()
    }

# 🚀 Inicia o servidor no Railway
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
