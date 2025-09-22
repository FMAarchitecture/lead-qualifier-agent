FROM ollama/ollama

EXPOSE 11434

# Copia o script para dentro da imagem
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
