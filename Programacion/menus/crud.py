import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mysql.connector import Error, IntegrityError
from db.database import get_connection, existe
from utils.entrada import pedir_texto, pedir_entero, confirmar, pedir_opcion, ejecutar, Cancelado, AYUDA

ROLES = ["admin", "compras", "ventas", "elaboracion"]

# Cada entidad describe su tabla, su clave primaria y sus campos.
# Un campo es (columna, etiqueta, tipo). Tipos posibles:
#   "texto"    -> texto obligatorio
#   "unico"    -> texto obligatorio que no se puede repetir en la tabla
#   "opcional" -> texto que se puede dejar vacío
#   "entero" / "decimal" -> números mayores o iguales a 0
#   "rol"      -> uno de los ROLES
USUARIOS = {
    "titulo": "usuarios",
    "tabla": "usuarios",
    "id": "id_usuario",
    "campos": [
        ("email", "Email", "unico"),
        ("password", "Contraseña", "texto"),
        ("rol", f"Rol ({'/'.join(ROLES)})", "rol"),
    ],
}

CLIENTES = {
    "titulo": "clientes",
    "tabla": "clientes",
    "id": "id_cliente",
    "campos": [
        ("nombre", "Nombre", "texto"),
        ("telefono", "Teléfono", "opcional"),
        ("email", "Email", "opcional"),
    ],
}

PROVEEDORES = {
    "titulo": "proveedores",
    "tabla": "proveedores",
    "id": "id_proveedor",
    "campos": [
        ("nombre", "Nombre", "texto"),
        ("telefono", "Teléfono", "opcional"),
        ("email", "Email", "opcional"),
        ("domicilio", "Domicilio", "opcional"),
    ],
}

PRODUCTOS = {
    "titulo": "productos",
    "tabla": "productos",
    "id": "id_producto",
    "campos": [
        ("nombre", "Nombre", "texto"),
        ("precio", "Precio", "decimal"),
        ("stock", "Stock", "entero"),
    ],
}

INSUMOS = {
    "titulo": "insumos",
    "tabla": "insumos",
    "id": "id_insumo",
    "campos": [
        ("nombre", "Nombre", "texto"),
        ("unidad_medida", "Unidad de medida", "texto"),
        ("inventario", "Inventario", "decimal"),
    ],
}

def menu_crud(entidad):
    titulo = entidad["titulo"].upper()
    while True:
        print("\n" + "="*40)
        print(f"   GESTIÓN DE {titulo}")
        print("="*40)
        print("  1. Listar")
        print("  2. Agregar")
        print("  3. Modificar")
        print("  4. Eliminar")
        print("  0. Volver")
        print("-"*40)
        opcion = pedir_opcion()

        if opcion == "1":
            ejecutar(listar, entidad)
        elif opcion == "2":
            ejecutar(agregar, entidad)
        elif opcion == "3":
            ejecutar(modificar, entidad)
        elif opcion == "4":
            ejecutar(eliminar, entidad)
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

def listar(entidad):
    # La contraseña no se muestra en el listado
    columnas = [entidad["id"]] + [c[0] for c in entidad["campos"] if c[0] != "password"]
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute(f"SELECT {', '.join(columnas)} FROM {entidad['tabla']}")
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f"\n--- {entidad['titulo'].upper()} ---")
    if not filas:
        print("No hay registros.")
        return
    print(" | ".join(columnas))
    print("-" * 60)
    for fila in filas:
        print(" | ".join(str(v) for v in fila))

def buscar(entidad, id_registro):
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {entidad['tabla']} WHERE {entidad['id']} = %s", (id_registro,))
    fila = cursor.fetchone()
    cursor.close()
    conn.close()
    return fila

def guardar(sql, valores):
    """Ejecuta un INSERT, UPDATE o DELETE y confirma los cambios."""
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
    except Error:
        conn.rollback()
        raise
    finally:
        conn.close()

def pedir_valor(entidad, campo, actual=None):
    """Pide un campo. Si se está modificando (actual no es None), Enter deja el valor actual."""
    columna, etiqueta, tipo = campo
    mensaje = f"{etiqueta}: " if actual is None else f"{etiqueta} [{actual}]: "
    while True:
        texto = pedir_texto(mensaje, obligatorio=False)
        if texto == "":
            if actual is not None:
                return actual
            if tipo == "opcional":
                return None
            print("Este campo es obligatorio.")
            continue
        if tipo == "entero" or tipo == "decimal":
            try:
                numero = int(texto) if tipo == "entero" else float(texto.replace(",", "."))
            except ValueError:
                print("Ingresá un número válido.")
                continue
            if numero < 0:
                print("El valor no puede ser negativo.")
                continue
            return numero
        if tipo == "rol" and texto not in ROLES:
            print(f"Rol no válido. Opciones: {', '.join(ROLES)}")
            continue
        # Al modificar, se permite volver a escribir el mismo valor que ya tenía
        if tipo == "unico" and texto != actual and existe(entidad["tabla"], columna, texto):
            print(f"Ya existe un registro con ese {etiqueta.lower()}.")
            continue
        return texto

def agregar(entidad):
    print(f"\n--- AGREGAR A {entidad['titulo'].upper()} ---")
    print(AYUDA)
    columnas = [c[0] for c in entidad["campos"]]
    valores = [pedir_valor(entidad, c) for c in entidad["campos"]]
    if not confirmar("\n¿Guardar?"):
        raise Cancelado
    marcas = ", ".join(["%s"] * len(columnas))
    guardar(f"INSERT INTO {entidad['tabla']} ({', '.join(columnas)}) VALUES ({marcas})", valores)
    print("✔ Registro agregado correctamente.")

def pedir_registro(entidad, accion):
    """Lista la tabla y pide un ID hasta que exista. Devuelve (id, fila)."""
    listar(entidad)
    while True:
        id_registro = pedir_entero(f"\nID a {accion}: ", minimo=1)
        fila = buscar(entidad, id_registro)
        if fila:
            return id_registro, fila
        print("No existe un registro con ese ID.")

def modificar(entidad):
    print(f"\n--- MODIFICAR {entidad['titulo'].upper()} ---")
    print(AYUDA)
    id_registro, fila = pedir_registro(entidad, "modificar")
    print("Presioná Enter para dejar el valor actual (entre corchetes).")
    columnas = [c[0] for c in entidad["campos"]]
    valores = []
    for campo in entidad["campos"]:
        actual = fila[campo[0]]
        valores.append(pedir_valor(entidad, campo, "" if actual is None else actual))
    if not confirmar("\n¿Guardar cambios?"):
        raise Cancelado
    asignaciones = ", ".join(f"{col} = %s" for col in columnas)
    guardar(f"UPDATE {entidad['tabla']} SET {asignaciones} WHERE {entidad['id']} = %s", valores + [id_registro])
    print("✔ Registro modificado correctamente.")

def eliminar(entidad):
    print(f"\n--- ELIMINAR DE {entidad['titulo'].upper()} ---")
    print(AYUDA)
    id_registro, fila = pedir_registro(entidad, "eliminar")
    if not confirmar(f"¿Seguro que querés eliminar el registro {id_registro}?"):
        raise Cancelado
    try:
        guardar(f"DELETE FROM {entidad['tabla']} WHERE {entidad['id']} = %s", (id_registro,))
    except IntegrityError:
        # Falla por las FOREIGN KEY con ON DELETE RESTRICT (ej: un cliente con ventas)
        print("✘ No se puede eliminar: tiene ventas, compras o recetas asociadas.")
        return
    print("✔ Registro eliminado correctamente.")
