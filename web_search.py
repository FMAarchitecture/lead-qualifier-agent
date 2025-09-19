from serpapi import GoogleSearch
import os

SERPAPI_API_KEY = "ee030efb32d31daacdb01e48cd0031a51ecd47466968330db758ad7557b2d3d8"


def search_web(query: str, num_results: int = 5) -> list:
    try:
        print(f"🔍 Pesquisando no SerpAPI: {query}")

        search = GoogleSearch({
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": num_results,
            "hl": "pt-br"
        })

        results = search.get_dict()
        return results.get("organic_results", [])

    except Exception as e:
        print(f"❌ Erro ao buscar dados no SerpAPI: {e}")
        return [{
            "title": f"[ERRO] Não foi possível buscar dados para: {query}",
            "link": "",
            "snippet": str(e)
        }]
