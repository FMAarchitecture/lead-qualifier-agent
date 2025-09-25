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
    fontes = "\n".join([
        f"{r.get('title')}\n{r.get('link')}\n{r.get('snippet')}"
        for r in search_results
    ])

    prompt = f"""
    Você é um pesquisador de mercado especializado em leads de arquitetura de alto padrão.

    A Fernanda Marques Arquitetura atua com:
    - Projetos residenciais únicos para clientes de alta renda (pessoa física).
    - Projetos de incorporação imobiliária de alto padrão (pessoa jurídica).

    Nome do lead: {nome}
    Tipo de projeto: {tipo}

    --- Fontes encontradas (site, LinkedIn, redes sociais, notícias) ---
    {fontes}

    Sua tarefa:
    - Identifique se o lead é uma pessoa física ou empresa.
    - Explique quem é, o que faz, e seu posicionamento no mercado.
    - Destaque indícios de capacidade financeira ou atuação em incorporação.
    - Use apenas informações baseadas nas fontes listadas.

    Responda em até 6 linhas.
    """
    return call_llm(prompt)


def lead_analyst_agent(data: dict, pesquisa: str) -> str:
    prompt = f"""
    Você é um analista de leads da Fernanda Marques Arquitetura.

    A empresa atua com projetos residenciais de alto padrão (clientes pessoa física) e com incorporação imobiliária (pessoa jurídica).
    Nosso foco é em clientes com perfil de alta renda ou empresas que desenvolvem empreendimentos sofisticados.

    --- DADOS DO LEAD ---
    Nome: {data.get('nome')}
    Segmento: {data.get('segmento')}
    Tipo de Projeto: {data.get('tipo_projeto')}

    --- PESQUISA DE MERCADO ---
    {pesquisa}

    Analise o POTENCIAL DE CONTRATAÇÃO deste lead, considerando:
    - Se o lead é PF ou PJ.
    - Alinhamento do perfil com clientes de alto padrão.
    - Indícios de capacidade financeira ou experiência em incorporação.
    - Coerência entre demanda (tipo de projeto) e serviços da Fernanda Marques Arquitetura.

    Seja técnico, direto e objetivo.
    """
    return call_llm(prompt)


def lead_scoring_specialist_agent(data: dict, pesquisa: str, analise: str) -> str:
    prompt = f"""
    Você é um especialista em qualificação de leads da Fernanda Marques Arquitetura.

    --- DADOS DO LEAD ---
    Nome: {data.get('nome')}
    Segmento: {data.get('segmento')}
    Tipo de Projeto: {data.get('tipo_projeto')}

    --- PESQUISA ---
    {pesquisa}

    --- ANÁLISE ---
    {analise}

    Sua tarefa:
    - Atribua uma nota de 0 a 100 para o potencial de contratação.
    - Considere: alinhamento com projetos residenciais de alto padrão (PF) ou incorporação (PJ).
    - Avalie capacidade financeira, perfil do lead e coerência da demanda.
    - Justifique a nota de forma clara e profissional.

    Formato:
    - Nota (0 a 100): ...
    - Justificativa: ...
    """
    return call_llm(prompt)


def summarizer_agent(data: dict, pesquisa: str, analise: str, score: str) -> str:
    prompt = f"""
    Você é um assistente de vendas da Fernanda Marques Arquitetura.

    A empresa é referência em projetos residenciais de alto padrão e em incorporação imobiliária.
    Nosso público-alvo inclui tanto clientes de alta renda (PF) quanto empresas de incorporação (PJ).

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

    Formate a resposta em **HTML estruturado** com os seguintes blocos:

    <h2>Resumo de Qualificação</h2>
    <p><strong>O lead [NOME]</strong> foi avaliado com nota <strong>[NOTA]</strong>.</p>

    <h3>Fatores que justificam a nota</h3>
    <p>[Texto explicativo]</p>

    <h3>Perfil e Relevância</h3>
    <p>[Se é PF ou PJ e a importância para a Fernanda Marques Arquitetura]</p>


    Use apenas tags HTML simples (<h2>, <h3>, <p>, <strong>, <br>). 
    """
    return call_llm(prompt)
