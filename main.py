from fastapi import FastAPI
import psycopg2
import os

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Conexão com o PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API de Nicknames está rodando!"}

@app.get("/nicknames")
def get_nicknames():
    cur = conn.cursor()
    cur.execute("SELECT * FROM nicknames;")
    rows = cur.fetchall()
    cur.close()
    
    return [{"id": row[0], "nickname": row[1], "category": row[2], "popularity": row[3]} for row in rows]

