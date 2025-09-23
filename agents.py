import os
import google.generativeai as genai
from web_search import search_web

# Configura a chave do Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-1.5-flash"

def call_llm(prompt: str) -> str:
    try:
        print("🔁 [DEBUG] Chamando modelo Gemini com prompt:")
        print(prompt)

        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        return response.text.strip() if response and response.text else "[ERRO] Resposta vazia do Gemini."

    except Exception as e:
        print(f"❌ Erro ao chamar Gemini: {e}")
        return f"[ERRO] {str(e)}"


def researcher_agent(data: dict) -> str:
    nome = data.get("nome")
    tipo = data.get("tipo_projeto") or data.get("segmento")

    # Busca na web
    search_results = search_web(f"{nome} {tipo}")
    fontes = "\n".join([f"{r.get('title')}\n{r.get('link')}\n{r.get('snippet')}" for r in search_results])

    # Prompt adaptado para pessoa física ou empresa
    prompt = f"""
    Você é um pesquisador de mercado.

    Use as fontes abaixo para investigar quem é esse lead. O nome pode ser tanto de uma pessoa física quanto de uma empresa.

    Nome do lead: {nome}
    Tipo de projeto: {tipo}

    --- Fontes encontradas ---
    {fontes}

    Com base nessas fontes, escreva um parágrafo com até 6 linhas explicando quem é o lead, se é uma pessoa ou empresa, o que faz, e qual o potencial dele para contratar serviços de arquitetura de alto padrão.
    """
    return call_llm(prompt)


def lead_analyst_agent(data: dict, pesquisa: str) -> str:
    prompt = f"""
    Você é um analista de leads da Fernanda Marques Arquitetura.

    Abaixo estão os dados disponíveis de um lead, juntamente com uma pesquisa realizada sobre ele:

    --- DADOS DO LEAD ---
    Nome: {data.get('nome')}
    Segmento: {data.get('segmento')}
    Tipo de Projeto: {data.get('tipo_projeto')}

    --- PESQUISA DE MERCADO ---
    {pesquisa}

    Com base nesses dados limitados, avalie o POTENCIAL DE CONTRATAÇÃO do lead para serviços da Fernanda Marques Arquitetura.

    Considere o alinhamento com nosso público-alvo e portfólio. Seja técnico e direto.
    """
    return call_llm(prompt)


def lead_scoring_specialist_agent(data: dict, pesquisa: str, analise: str) -> str:
    prompt = f"""
    Você é um especialista em qualificação de leads da Fernanda Marques Arquitetura.

    Abaixo estão os dados limitados de um lead, uma pesquisa e uma análise prévia:

    --- DADOS DO LEAD ---
    Nome: {data.get('nome')}
    Segmento: {data.get('segmento')}
    Tipo de Projeto: {data.get('tipo_projeto')}

    --- PESQUISA ---
    {pesquisa}

    --- ANÁLISE ---
    {analise}

    Com base nisso, atribua uma nota de 0 a 100 representando o potencial de contratação do lead. Justifique sua nota com base na relevância do projeto, alinhamento com nosso portfólio e possíveis perfis do lead.

    Formato:
    - Nota (0 a 100): ...
    - Justificativa: ...
    """
    return call_llm(prompt)


def summarizer_agent(data: dict, pesquisa: str, analise: str, score: str) -> str:
    prompt = f"""
    Você é um assistente de vendas da Fernanda Marques Arquitetura.

    Sua tarefa é redigir um resumo profissional sobre um lead qualificado, com base nos dados disponíveis, pesquisa, análise e nota final.

    --- DADOS DO LEAD ---
    Nome: {data.get('nome')}
    Segmento: {data.get('segmento')}
    Tipo de Projeto: {data.get('tipo_projeto')}

    --- PESQUISA ---
    {pesquisa}

    --- ANÁLISE ---
    {analise}

    --- SCORE ---
    {score}

    Escreva um resumo claro, com até 10 linhas, destacando:
    - A nota final atribuída ao lead
    - Os principais fatores que justificam a nota
    - O perfil e atuação do lead (pessoa ou empresa)
    - A relevância do lead para a Fernanda Marques Arquitetura
    - A sugestão de próximo passo para abordagem

    Escreva em português, em tom profissional, e comece com:
    "O lead {data.get('nome')}, foi avaliado..."
    """
    return call_llm(prompt)
