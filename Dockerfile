# Usar imagem oficial do Python
FROM python:3.12-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar dependências
COPY requirements.txt /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código
COPY . /app/

# Copiar o entrypoint
COPY entrypoint.sh /app/entrypoint.sh

# Garantir permissão de execução
RUN chmod +x /app/entrypoint.sh

# Porta do Django
EXPOSE 8000

# Definir entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
