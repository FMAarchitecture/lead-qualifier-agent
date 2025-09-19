from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List, Optional
from agents import (
    researcher_agent,
    lead_analyst_agent,
    lead_scoring_specialist_agent,
    summarizer_agent
)
from email_sender import send_email

app = FastAPI()


# MODELOS ----------------------------------------------------------------------

class ColumnValue(BaseModel):
    title: str
    text: Optional[str] = None

class WebhookEvent(BaseModel):
    pulseName: str
    columnValues: List[ColumnValue]

class WebhookPayload(BaseModel):
    event: WebhookEvent

class ChallengeRequest(BaseModel):
    challenge: str


# MIDDLEWARE -------------------------------------------------------------------

@app.middleware("http")
async def add_ngrok_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response


# ENDPOINTS --------------------------------------------------------------------

@app.post("/")
async def root(payload: ChallengeRequest):
    print(f"[MONDAY] Desafio recebido: {payload.challenge}")
    return PlainTextResponse(content=payload.challenge, status_code=200)


@app.post("/webhook")
async def handle_webhook(payload: WebhookPayload, background_tasks: BackgroundTasks):
    print("✅ JSON recebido do Monday:\n", payload)

    try:
        event = payload.event
        lead_name = event.pulseName
        column_values = event.columnValues

        # Busca o tipo de projeto entre as colunas
        project_type = "não informado"
        for col in column_values:
            if col.title.lower() in ["segmento", "tipo de projeto"]:
                project_type = col.text or "não informado"

        # Monta os dados para os agentes
        lead_data = {
            "nome": lead_name,
            "segmento": project_type,
            "tipo_projeto": project_type
        }

        # Roda os agentes em background
        background_tasks.add_task(process_lead_flow, lead_data)

        # Responde rapidamente ao Make
        return {"status": "received"}

    except Exception as e:
        print("[❌ ERRO] Falha ao processar webhook:", e)
        raise HTTPException(status_code=422, detail=str(e))


# PROCESSAMENTO EM BACKGROUND --------------------------------------------------

def process_lead_flow(lead_data: dict):
    try:
        print("▶️ [AGENTES] Processando lead:", lead_data)

        research = researcher_agent(lead_data)
        analysis = lead_analyst_agent(lead_data, research)
        score = lead_scoring_specialist_agent(lead_data, research, analysis)
        summary = summarizer_agent(lead_data, research, analysis, score)

        print("📩 RESUMO FINAL:", summary)  # DEBUG extra

        send_email(
            subject=f"Lead qualificado: {lead_data['nome']}",
            body=summary.strip(),
            to_email="laura.bueno@fernandamarques.com.br"
        )

        print("✅ [EMAIL] Enviado com sucesso!")

    except Exception as e:
        print("❌ [ERRO NO PROCESSO COMPLETO]:", str(e))


# ENTRYPOINT -------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
