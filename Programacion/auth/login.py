import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mysql.connector import Error
from db.database import get_connection
from utils.entrada import pedir_texto, Cancelado

def login():
    """Devuelve el usuario logueado, o None si el usuario cancela."""
    print("\n" + "="*40)
    print("   TAPAS EMPANADAS - Sistema de Gestión")
    print("="*40)
    print("(escribí 'c' o presioná Ctrl+C para salir)")
    intentos = 3
    while intentos > 0:
        print(f"\nIntentos restantes: {intentos}")
        try:
            email = pedir_texto("Email: ")
            password = pedir_texto("Contraseña: ")
        except Cancelado:
            return None

        conn = get_connection()
        if not conn:
            print("No se puede conectar a la base de datos. Saliendo.")
            sys.exit(1)

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM usuarios WHERE email = %s AND password = %s",
                (email, password)
            )
            usuario = cursor.fetchone()
            cursor.close()
        except Error as e:
            print(f"[ERROR] No se pudo validar el usuario: {e}")
            return None
        finally:
            conn.close()

        if usuario:
            print(f"\n✔ Bienvenido/a, {usuario['email']}! (Rol: {usuario['rol']})")
            return usuario
        else:
            print("✘ Email o contraseña incorrectos.")
            intentos -= 1

    print("\nDemasiados intentos fallidos. Saliendo.")
    sys.exit(1)
