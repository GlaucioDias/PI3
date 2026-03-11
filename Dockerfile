FROM python:3.11-slim

# diretório da aplicação
WORKDIR /app

# copiar requirements primeiro (cache do docker)
COPY requirements.txt .

# instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# copiar projeto
COPY . .

# criar pasta uploads
RUN mkdir -p static/uploads

# expor porta
EXPOSE 5000

# iniciar aplicação
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
CMD ["flask", "run", "--host=0.0.0.0", "--reload", "--debugger"]
