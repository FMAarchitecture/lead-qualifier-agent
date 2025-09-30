import google.generativeai as genai

# COLOQUE SUA CHAVE DIRETA AQUI
genai.configure(api_key="AIzaSyAZX8mxW2JI5YUNMpfL0prnLKNgYP18BYI")

print("\n🔎 Modelos disponíveis:")
for m in genai.list_models():
    print("-", m.name)
