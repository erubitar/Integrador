"""
Script para crear la tabla de usuarios e insertar usuarios de prueba.
Ejecutar una sola vez: python db/seed.py
"""
from database import get_connection, existe

SQL_CREATE_USUARIOS = """
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(30) NOT NULL,
    password VARCHAR(20) NOT NULL,
    rol VARCHAR(20) NOT NULL
);
"""

USUARIOS_PRUEBA = [
    ("mrodrigo@tapitas.com",  "muysegura", "admin"),
    ("lbarrera@tapitas.com",  "masomenos", "compras"),
    ("mpacifico@tapitas.com", "regular",   "ventas"),
    ("ebitar@tapitas.com",    "insegura",  "elaboracion"),
]

def seed():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute(SQL_CREATE_USUARIOS)
    for email, password, rol in USUARIOS_PRUEBA:
        if existe("usuarios", "email", email):
            print(f"  Usuario '{email}' ya existe, se omite.")
            continue
        cursor.execute(
            "INSERT INTO usuarios (email, password, rol) VALUES (%s, %s, %s)",
            (email, password, rol)
        )
        print(f"  Usuario '{email}' ({rol}) creado.")
    conn.commit()
    cursor.close()
    conn.close()
    print("\nTabla de usuarios lista.")

if __name__ == "__main__":
    seed()
