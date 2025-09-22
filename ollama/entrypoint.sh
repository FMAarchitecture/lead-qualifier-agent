#!/bin/sh
set -e

# Inicia o servidor Ollama em background
ollama serve &

# Espera o servidor ficar pronto
sleep 5

# Puxa o modelo (se já tiver, ignora)
ollama pull llama3 || true

# Mantém o servidor em foreground
wait
