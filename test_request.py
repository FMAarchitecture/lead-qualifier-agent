import requests

url = "https://dc5e80d87149.ngrok-free.app/webhook"  # <--- atualizada

data = {
    "lead_name": "João Silva",
    "company": "Construtora XPTO",
    "project_type": "Residencial de alto padrão",
    "employees": "150"
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.text)
