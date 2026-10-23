from mysql.connector import Error

PALABRAS_CANCELAR = {"c", "cancelar", "volver"}
AYUDA = "(escribí 'c' o presioná Ctrl+C en cualquier momento para cancelar y volver)"


class Cancelado(Exception):
    """Se lanza cuando el usuario decide cancelar la operación actual."""


def pedir_texto(mensaje, obligatorio=True):
    while True:
        try:
            valor = input(mensaje).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            raise Cancelado
        if valor.lower() in PALABRAS_CANCELAR:
            raise Cancelado
        if valor or not obligatorio:
            return valor
        print("Este campo es obligatorio.")


def pedir_entero(mensaje, minimo=None):
    while True:
        try:
            numero = int(pedir_texto(mensaje))
        except ValueError:
            print("Ingresá un número entero válido.")
            continue
        if minimo is not None and numero < minimo:
            print(f"El valor debe ser mayor o igual a {minimo}.")
            continue
        return numero


def pedir_decimal(mensaje, minimo=None):
    while True:
        try:
            numero = float(pedir_texto(mensaje).replace(",", "."))
        except ValueError:
            print("Ingresá un número válido.")
            continue
        if minimo is not None and numero < minimo:
            print(f"El valor debe ser mayor o igual a {minimo}.")
            continue
        return numero


def confirmar(mensaje):
    while True:
        respuesta = pedir_texto(f"{mensaje} (s/n): ").lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("Respondé 's' o 'n'.")


def pedir_opcion():
    """Lee la opción de un menú. Cancelar equivale a elegir '0' (volver/salir)."""
    try:
        return pedir_texto("Seleccioná una opción: ", obligatorio=False)
    except Cancelado:
        return "0"


def ejecutar(accion, *args):
    """Ejecuta una opción de menú sin que una cancelación o un error de BD corten la aplicación."""
    try:
        accion(*args)
    except Cancelado:
        print("\n↩ Operación cancelada. No se guardaron cambios.")
    except Error as e:
        print(f"\n[ERROR] Falló la operación en la base de datos: {e}")
        print("No se guardaron cambios.")
