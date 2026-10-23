import sys
import os
sys.path.append(os.path.dirname(__file__))

from auth.login import login
from menus.admin import menu_admin
from menus.compras import menu_compras
from menus.ventas import menu_ventas
from menus.elaboracion import menu_elaboracion

MENUS = {
    "admin":       menu_admin,
    "compras":     menu_compras,
    "ventas":      menu_ventas,
    "elaboracion": menu_elaboracion,
}

def main():
    # Al cerrar sesión se vuelve al login; cancelar en el login sale de la aplicación
    while True:
        usuario = login()
        if not usuario:
            break
        rol = usuario["rol"]

        if rol in MENUS:
            MENUS[rol](usuario)
        else:
            print(f"Rol '{rol}' no tiene menú asignado.")

    print("\nHasta luego!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nHasta luego!\n")
