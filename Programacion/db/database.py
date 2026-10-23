import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "database": "integrador",
    "user": "root",
    "password": "root"
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"\n[ERROR] No se pudo conectar a la base de datos: {e}")
        return None

def existe(tabla, columna, valor):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM {tabla} WHERE {columna} = %s", (valor,))
        encontrado = cursor.fetchone() is not None
        cursor.close()
        return encontrado
    finally:
        conn.close()
