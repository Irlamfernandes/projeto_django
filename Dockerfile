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

# Porta do Django
EXPOSE 8000

# Comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
