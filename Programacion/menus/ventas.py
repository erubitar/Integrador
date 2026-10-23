import sys
import os
from datetime import date
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mysql.connector import Error
from db.database import get_connection, existe
from utils.entrada import pedir_entero, confirmar, pedir_opcion, ejecutar, Cancelado, AYUDA
from menus.crud import menu_crud, CLIENTES

def menu_ventas(usuario):
    while True:
        print("\n" + "="*40)
        print("          MENÚ VENTAS")
        print("="*40)
        print("  1. Gestión de clientes")
        print("  2. Ver productos y precios")
        print("  3. Registrar venta")
        print("  4. Ver historial de ventas")
        print("  0. Cerrar sesión")
        print("-"*40)
        opcion = pedir_opcion()

        if opcion == "1":
            menu_crud(CLIENTES)
        elif opcion == "2":
            ejecutar(ver_productos)
        elif opcion == "3":
            ejecutar(registrar_venta)
        elif opcion == "4":
            ejecutar(historial_ventas)
        elif opcion == "0":
            print("\nCerrando sesión...")
            break
        else:
            print("Opción no válida.")

def ver_clientes():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nombre, telefono, email FROM clientes")
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- CLIENTES ---")
    print(f"{'ID':<5} {'Nombre':<25} {'Teléfono':<15} {'Email'}")
    print("-" * 70)
    for f in filas:
        print(f"{f[0]:<5} {f[1]:<25} {str(f[2]):<15} {str(f[3])}")

def ver_productos():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, nombre, precio, stock FROM productos")
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- PRODUCTOS ---")
    print(f"{'ID':<5} {'Nombre':<30} {'Precio':<12} {'Stock'}")
    print("-" * 55)
    for f in filas:
        print(f"{f[0]:<5} {f[1]:<30} ${f[2]:<11} {f[3]}")

def registrar_venta():
    print("\n--- REGISTRAR VENTA ---")
    print(AYUDA)
    ver_clientes()
    while True:
        id_cliente = pedir_entero("\nID del cliente: ", minimo=1)
        if existe("clientes", "id_cliente", id_cliente):
            break
        print("No existe un cliente con ese ID.")

    items = []
    total = 0.0
    print("\nAgregar productos a la venta (escribí 0 en ID para terminar).")
    print("Si escribís 'c' en cantidad, se descarta ese producto y volvés al ID.")
    ver_productos()
    while True:
        id_producto = pedir_entero("\nID producto: ", minimo=0)
        if id_producto == 0:
            break
        try:
            cantidad = pedir_entero("Cantidad: ", minimo=1)
        except Cancelado:
            print("↩ Producto descartado.")
            continue

        conn = get_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT precio, stock FROM productos WHERE id_producto = %s", (id_producto,))
            prod = cursor.fetchone()
            cursor.close()
        finally:
            conn.close()

        if not prod:
            print("Producto no encontrado.")
            continue
        precio_unitario, stock = prod
        # Descontar lo que ya se cargó de este mismo producto en la venta
        reservado = sum(c for p, c, _ in items if p == id_producto)
        if cantidad > stock - reservado:
            print(f"Stock insuficiente. Stock disponible: {stock - reservado}")
            continue
        items.append((id_producto, cantidad, precio_unitario))
        total += cantidad * float(precio_unitario)

    if not items:
        print("No se agregaron productos. Venta cancelada.")
        return

    print(f"\nResumen: {len(items)} producto(s) | Total: ${total:.2f}")
    if not confirmar("¿Confirmar venta?"):
        raise Cancelado

    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        hoy = date.today()
        cursor.execute(
            "INSERT INTO ventas (fecha, total, id_cliente) VALUES (%s, %s, %s)",
            (hoy, total, id_cliente)
        )
        id_venta = cursor.lastrowid
        for id_producto, cantidad, precio_unitario in items:
            cursor.execute(
                "INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                (id_venta, id_producto, cantidad, precio_unitario)
            )
            cursor.execute(
                "UPDATE productos SET stock = stock - %s WHERE id_producto = %s",
                (cantidad, id_producto)
            )
        conn.commit()
        cursor.close()
    except Error:
        conn.rollback()
        raise
    finally:
        conn.close()
    print(f"\n✔ Venta registrada. ID: {id_venta} | Total: ${total:.2f}")

def historial_ventas():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.id_venta, v.fecha, c.nombre, v.total
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        ORDER BY v.id_venta DESC
    """)
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- HISTORIAL DE VENTAS ---")
    print(f"{'ID':<8} {'Fecha':<15} {'Cliente':<25} {'Total'}")
    print("-" * 60)
    for f in filas:
        print(f"{f[0]:<8} {str(f[1]):<15} {f[2]:<25} ${f[3]}")
    if filas and confirmar("\n¿Ver el detalle de una venta?"):
        ver_detalle_venta()

def ver_detalle_venta():
    print(AYUDA)
    while True:
        id_venta = pedir_entero("\nID de la venta: ", minimo=1)
        if existe("ventas", "id_venta", id_venta):
            break
        print("No existe una venta con ese ID.")

    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.fecha, c.nombre, v.total
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        WHERE v.id_venta = %s
    """, (id_venta,))
    fecha, cliente, total = cursor.fetchone()
    cursor.execute("""
        SELECT p.nombre, d.cantidad, d.precio_unitario,
               d.cantidad * d.precio_unitario AS subtotal
        FROM detalle_venta d
        JOIN productos p ON d.id_producto = p.id_producto
        WHERE d.id_venta = %s
    """, (id_venta,))
    filas = cursor.fetchall()
    cursor.close()
    conn.close()

    print(f"\nVenta N° {id_venta} | Fecha: {fecha} | Cliente: {cliente}")
    print(f"{'Producto':<32} {'Cantidad':<10} {'Precio unit.':<15} {'Subtotal'}")
    print("-" * 70)
    if not filas:
        print("Esta venta no tiene productos cargados.")
    for f in filas:
        print(f"{f[0]:<32} {f[1]:<10} ${str(f[2]):<14} ${f[3]}")
    print("-" * 70)
    print(f"{'TOTAL':<58} ${total}")
