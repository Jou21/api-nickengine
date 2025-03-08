from flask import Flask, jsonify
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

# Inicializar o Flask
app = Flask(__name__)

@app.route('/')
def read_root():
    return jsonify({"message": "API de Nicknames está rodando!"})

@app.route('/nicknames')
def get_nicknames():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM nicknames;")
        rows = cur.fetchall()
        cur.close()
        # Retorna os resultados como um JSON
        return jsonify([{"id": row[0], "nickname": row[1], "category": row[2], "popularity": row[3]} for row in rows])
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return jsonify({"error": "Erro ao buscar os nicknames"})

if __name__ == '__main__':
    app.run(debug=True)
