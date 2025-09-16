from serpapi import GoogleSearch
import os

SERPAPI_API_KEY = "ee030efb32d31daacdb01e48cd0031a51ecd47466968330db758ad7557b2d3d8" 

# def search_web(query: str, num_results: int = 5) -> list:
#     search = GoogleSearch({
#         "q": query,
#         "api_key": SERPAPI_API_KEY,
#         "num": num_results,
#         "hl": "pt-br"
#     })
#     results = search.get_dict()
#     return results.get("organic_results", [])

def search_web(query: str, num_results: int = 5) -> list:
    # MOCK temporário para evitar uso do SerpAPI
    print(f"[DEBUG] SerpAPI desativado. Simulando busca para: {query}")
    return [
        {
            "title": f"Simulação de resultado para {query}",
            "link": "https://www.exemplo.com/simulacao",
            "snippet": f"Este é um resumo fictício sobre {query}, usado para testes locais sem consumir tokens da SerpAPI."
        }
    ]
