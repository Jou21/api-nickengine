from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Carregar as variáveis de ambiente
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Log para verificar se as variáveis de ambiente estão carregando corretamente
print(f"DB_HOST: {DB_HOST}, DB_NAME: {DB_NAME}, DB_USER: {DB_USER}")

# Conexão com o PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    print("Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    raise

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API de Nicknames está rodando!"}

@app.get("/nicknames")
def get_nicknames():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM nicknames;")
        rows = cur.fetchall()
        cur.close()
        return [{"id": row[0], "nickname": row[1], "category": row[2], "popularity": row[3]} for row in rows]
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return {"error": "Erro ao buscar os nicknames"}
