from fastapi import FastAPI, Request
from llm.local_llm import query_local_llm

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    
    # Aqui você adapta para os campos reais que o Make envia
    lead_name = data.get("lead_name", "")
    company = data.get("company", "")
    project_type = data.get("project_type", "")
    employees = data.get("employees", "")

    prompt = f"""
    Nome do lead: {lead_name}
    Tipo de projeto: {project_type}

    Com base nesses dados, qualifique esse lead para serviços de arquitetura de alto padrão da Fernanda Marques Arquitetura.
    """

    response = query_local_llm(prompt)

    return {"qualificacao": response}
