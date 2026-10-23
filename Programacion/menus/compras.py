import sys
import os
from datetime import date
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mysql.connector import Error
from db.database import get_connection, existe
from utils.entrada import (
    pedir_entero, pedir_decimal, confirmar, pedir_opcion, ejecutar, Cancelado, AYUDA
)
from menus.crud import menu_crud, PROVEEDORES, INSUMOS

def menu_compras(usuario):
    while True:
        print("\n" + "="*40)
        print("          MENÚ COMPRAS")
        print("="*40)
        print("  1. Gestión de proveedores")
        print("  2. Gestión de insumos")
        print("  3. Registrar compra")
        print("  4. Ver historial de compras")
        print("  5. Ver avisos de escasez")
        print("  0. Cerrar sesión")
        print("-"*40)
        opcion = pedir_opcion()

        if opcion == "1":
            menu_crud(PROVEEDORES)
        elif opcion == "2":
            menu_crud(INSUMOS)
        elif opcion == "3":
            ejecutar(registrar_compra)
        elif opcion == "4":
            ejecutar(historial_compras)
        elif opcion == "5":
            ejecutar(ver_avisos_escasez)
        elif opcion == "0":
            print("\nCerrando sesión...")
            break
        else:
            print("Opción no válida.")

def ver_proveedores():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id_proveedor, nombre, telefono, email, domicilio FROM proveedores")
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- PROVEEDORES ---")
    print(f"{'ID':<5} {'Nombre':<25} {'Teléfono':<15} {'Email':<30} {'Domicilio'}")
    print("-" * 90)
    for f in filas:
        print(f"{f[0]:<5} {f[1]:<25} {str(f[2]):<15} {str(f[3]):<30} {str(f[4])}")

def ver_insumos():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id_insumo, nombre, unidad_medida, inventario FROM insumos")
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- INSUMOS Y STOCK ---")
    print(f"{'ID':<5} {'Nombre':<25} {'Unidad':<12} {'Inventario'}")
    print("-" * 55)
    for f in filas:
        print(f"{f[0]:<5} {f[1]:<25} {str(f[2]):<12} {f[3]}")

def registrar_compra():
    print("\n--- REGISTRAR COMPRA ---")
    print(AYUDA)
    ver_proveedores()
    while True:
        id_proveedor = pedir_entero("\nID del proveedor: ", minimo=1)
        if existe("proveedores", "id_proveedor", id_proveedor):
            break
        print("No existe un proveedor con ese ID.")

    items = []
    total = 0.0
    print("\nAgregar insumos a la compra (escribí 0 en ID para terminar).")
    print("Si escribís 'c' en cantidad o precio, se descarta ese insumo y volvés al ID.")
    ver_insumos()
    while True:
        id_insumo = pedir_entero("\nID insumo: ", minimo=0)
        if id_insumo == 0:
            break
        if not existe("insumos", "id_insumo", id_insumo):
            print("No existe un insumo con ese ID.")
            continue
        try:
            cantidad = pedir_entero("Cantidad: ", minimo=1)
            precio_unitario = pedir_decimal("Precio unitario: ", minimo=0)
        except Cancelado:
            print("↩ Insumo descartado.")
            continue
        items.append((id_insumo, cantidad, precio_unitario))
        total += cantidad * precio_unitario

    if not items:
        print("No se agregaron insumos. Compra cancelada.")
        return

    print(f"\nResumen: {len(items)} insumo(s) | Total: ${total:.2f}")
    if not confirmar("¿Confirmar compra?"):
        raise Cancelado

    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        hoy = date.today()
        cursor.execute(
            "INSERT INTO compras (fecha, total, id_proveedor) VALUES (%s, %s, %s)",
            (hoy, total, id_proveedor)
        )
        id_compra = cursor.lastrowid
        for id_insumo, cantidad, precio_unitario in items:
            cursor.execute(
                "INSERT INTO detalle_compra (id_compra, id_insumo, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                (id_compra, id_insumo, cantidad, precio_unitario)
            )
            cursor.execute(
                "UPDATE insumos SET inventario = inventario + %s WHERE id_insumo = %s",
                (cantidad, id_insumo)
            )
        conn.commit()
        cursor.close()
    except Error:
        conn.rollback()
        raise
    finally:
        conn.close()
    print(f"\n✔ Compra registrada. ID: {id_compra} | Total: ${total:.2f}")

def historial_compras():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id_compra, c.fecha, p.nombre, c.total
        FROM compras c
        JOIN proveedores p ON c.id_proveedor = p.id_proveedor
        ORDER BY c.id_compra DESC
    """)
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- HISTORIAL DE COMPRAS ---")
    print(f"{'ID':<8} {'Fecha':<15} {'Proveedor':<25} {'Total'}")
    print("-" * 60)
    for f in filas:
        print(f"{f[0]:<8} {str(f[1]):<15} {f[2]:<25} ${f[3]}")
    if filas and confirmar("\n¿Ver el detalle de una compra?"):
        ver_detalle_compra()

def ver_detalle_compra():
    print(AYUDA)
    while True:
        id_compra = pedir_entero("\nID de la compra: ", minimo=1)
        if existe("compras", "id_compra", id_compra):
            break
        print("No existe una compra con ese ID.")

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.fecha, p.nombre, c.total
        FROM compras c
        JOIN proveedores p ON c.id_proveedor = p.id_proveedor
        WHERE c.id_compra = %s
    """, (id_compra,))
    fecha, proveedor, total = cursor.fetchone()
    cursor.execute("""
        SELECT i.nombre, i.unidad_medida, d.cantidad, d.precio_unitario,
               d.cantidad * d.precio_unitario AS subtotal
        FROM detalle_compra d
        JOIN insumos i ON d.id_insumo = i.id_insumo
        WHERE d.id_compra = %s
    """, (id_compra,))
    filas = cursor.fetchall()
    cursor.close()
    conn.close()

    print(f"\nCompra N° {id_compra} | Fecha: {fecha} | Proveedor: {proveedor}")
    print(f"{'Insumo':<20} {'Unidad':<8} {'Cantidad':<10} {'Precio unit.':<15} {'Subtotal'}")
    print("-" * 70)
    if not filas:
        print("Esta compra no tiene insumos cargados.")
    for f in filas:
        print(f"{f[0]:<20} {str(f[1]):<8} {f[2]:<10} ${str(f[3]):<14} ${f[4]}")
    print("-" * 70)
    print(f"{'TOTAL':<55} ${total}")

def ver_avisos_escasez():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.fecha, i.nombre, a.inventario, i.unidad_medida
        FROM avisos_escasez a
        JOIN insumos i ON a.id_insumo = i.id_insumo
        ORDER BY a.id_aviso DESC LIMIT 20
    """)
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- AVISOS DE ESCASEZ (últimos 20) ---")
    if not filas:
        print("No hay avisos.")
        return
    print(f"{'Fecha':<22} {'Insumo':<20} {'Quedaban'}")
    print("-" * 60)
    for f in filas:
        print(f"{str(f[0]):<22} {f[1]:<20} {f[2]} {f[3]}")
