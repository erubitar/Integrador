import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mysql.connector import Error
from db.database import get_connection, existe
from utils.entrada import pedir_entero, confirmar, pedir_opcion, ejecutar, Cancelado, AYUDA

def menu_elaboracion(usuario):
    while True:
        print("\n" + "="*40)
        print("        MENÚ ELABORACIÓN")
        print("="*40)
        print("  1. Ver productos y stock")
        print("  2. Ver insumos disponibles")
        print("  3. Ver recetas")
        print("  4. Registrar elaboración")
        print("  5. Ver historial de elaboraciones")
        print("  0. Cerrar sesión")
        print("-"*40)
        opcion = pedir_opcion()

        if opcion == "1":
            ejecutar(ver_productos)
        elif opcion == "2":
            ejecutar(ver_insumos)
        elif opcion == "3":
            ejecutar(ver_recetas)
        elif opcion == "4":
            ejecutar(registrar_elaboracion)
        elif opcion == "5":
            ejecutar(historial_elaboraciones)
        elif opcion == "0":
            print("\nCerrando sesión...")
            break
        else:
            print("Opción no válida.")

def ver_productos():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, nombre, precio, stock FROM productos")
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- PRODUCTOS Y STOCK ---")
    print(f"{'ID':<5} {'Nombre':<30} {'Precio':<12} {'Stock'}")
    print("-" * 55)
    for f in filas:
        print(f"{f[0]:<5} {f[1]:<30} ${f[2]:<11} {f[3]}")

def ver_insumos():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id_insumo, nombre, unidad_medida, inventario FROM insumos")
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- INSUMOS DISPONIBLES ---")
    print(f"{'ID':<5} {'Nombre':<25} {'Unidad':<12} {'Inventario'}")
    print("-" * 55)
    for f in filas:
        print(f"{f[0]:<5} {f[1]:<25} {str(f[2]):<12} {f[3]}")

def ver_recetas():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre AS producto, i.nombre AS insumo,
               r.cantidad_elaboracion, i.unidad_medida
        FROM recetas r
        JOIN productos p ON r.id_producto = p.id_producto
        JOIN insumos i ON r.id_insumo = i.id_insumo
        ORDER BY p.nombre
    """)
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- RECETAS ---")
    print(f"{'Producto':<30} {'Insumo':<25} {'Cantidad':<12} {'Unidad'}")
    print("-" * 75)
    for f in filas:
        print(f"{f[0]:<30} {f[1]:<25} {f[2]:<12} {f[3]}")

def registrar_elaboracion():
    print("\n--- REGISTRAR ELABORACIÓN ---")
    print(AYUDA)
    ver_productos()
    while True:
        id_producto = pedir_entero("\nID del producto a elaborar: ", minimo=1)
        if existe("productos", "id_producto", id_producto):
            break
        print("No existe un producto con ese ID.")
    cantidad = pedir_entero("Cantidad a producir: ", minimo=1)

    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()

        # Verificar insumos necesarios según receta
        cursor.execute("""
            SELECT r.id_insumo, i.nombre, r.cantidad_elaboracion, i.inventario, i.unidad_medida
            FROM recetas r
            JOIN insumos i ON r.id_insumo = i.id_insumo
            WHERE r.id_producto = %s
        """, (id_producto,))
        receta = cursor.fetchall()

        if not receta:
            print("No hay receta definida para este producto.")
            return

        print("\n--- Verificando insumos necesarios ---")
        falta_insumo = False
        for id_insumo, nombre, cant_x_unidad, inventario, unidad in receta:
            necesario = float(cant_x_unidad) * cantidad
            print(f"  {nombre}: necesario={round(necesario, 4)} {unidad} | disponible={inventario} {unidad}", end="")
            if float(inventario) < necesario:
                print("  ✘ INSUFICIENTE")
                falta_insumo = True
            else:
                print("  ✔")

        if falta_insumo:
            print("\nNo hay suficientes insumos para esta elaboración.")
            return

        if not confirmar("\n¿Confirmar elaboración?"):
            raise Cancelado

        # Último aviso antes de elaborar, para mostrar después solo los nuevos
        cursor.execute("SELECT COALESCE(MAX(id_aviso), 0) FROM avisos_escasez")
        ultimo_aviso = cursor.fetchone()[0]

        # El procedimiento almacenado registra la elaboración, descuenta insumos y suma stock.
        # Al bajar los insumos, el trigger tr_escasez_insumos guarda los avisos de escasez.
        cursor.callproc("registrar_elaboracion", (id_producto, cantidad))

        conn.commit()
        cursor.execute("""
            SELECT i.nombre, a.inventario, i.unidad_medida
            FROM avisos_escasez a
            JOIN insumos i ON a.id_insumo = i.id_insumo
            WHERE a.id_aviso > %s
        """, (ultimo_aviso,))
        avisos = cursor.fetchall()
        cursor.close()
    except Error:
        conn.rollback()
        raise
    finally:
        conn.close()
    print(f"\n✔ Elaboración registrada. {cantidad} unidades producidas.")
    for nombre, inventario, unidad in avisos:
        print(f"⚠ AVISO DE ESCASEZ: quedan {inventario} {unidad} de {nombre}. Avisar a compras.")

def historial_elaboraciones():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id_elaboracion, e.fecha, p.nombre, e.cantidad_producida
        FROM elaboracion e
        JOIN productos p ON e.id_producto = p.id_producto
        ORDER BY e.fecha DESC LIMIT 20
    """)
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- HISTORIAL DE ELABORACIONES ---")
    print(f"{'ID':<8} {'Fecha':<15} {'Producto':<30} {'Cantidad'}")
    print("-" * 65)
    for f in filas:
        print(f"{f[0]:<8} {str(f[1]):<15} {f[2]:<30} {f[3]}")
