import requests

def query_local_llm(prompt, model="llama3:8b", temperature=0.7, max_tokens=512):
    url = "http://localhost:11434/api/chat"

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()["message"]["content"]
    else:
        raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")