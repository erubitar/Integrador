import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db.database import get_connection
from utils.entrada import pedir_opcion, ejecutar, confirmar
from menus.crud import menu_crud, USUARIOS, CLIENTES, PROVEEDORES, PRODUCTOS, INSUMOS
from menus.compras import ver_detalle_compra
from menus.ventas import ver_detalle_venta

def menu_admin(usuario):
    while True:
        print("\n" + "="*40)
        print("        MENÚ ADMINISTRADOR")
        print("="*40)
        print("  1. Gestión de usuarios")
        print("  2. Gestión de clientes")
        print("  3. Gestión de proveedores")
        print("  4. Gestión de productos")
        print("  5. Gestión de insumos")
        print("  6. Reportes de ventas")
        print("  7. Reportes de compras")
        print("  0. Cerrar sesión")
        print("-"*40)
        opcion = pedir_opcion()

        if opcion == "1":
            menu_crud(USUARIOS)
        elif opcion == "2":
            menu_crud(CLIENTES)
        elif opcion == "3":
            menu_crud(PROVEEDORES)
        elif opcion == "4":
            menu_crud(PRODUCTOS)
        elif opcion == "5":
            menu_crud(INSUMOS)
        elif opcion == "6":
            ejecutar(reporte_ventas)
        elif opcion == "7":
            ejecutar(reporte_compras)
        elif opcion == "0":
            print("\nCerrando sesión...")
            break
        else:
            print("Opción no válida.")

def reporte_ventas():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.id_venta, v.fecha, c.nombre AS cliente, v.total
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        ORDER BY v.id_venta DESC
    """)
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- VENTAS ---")
    print(f"{'ID':<8} {'Fecha':<15} {'Cliente':<25} {'Total'}")
    print("-" * 60)
    for f in filas:
        print(f"{f[0]:<8} {str(f[1]):<15} {f[2]:<25} ${f[3]}")
    if filas and confirmar("\n¿Ver el detalle de una venta?"):
        ver_detalle_venta()

def reporte_compras():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id_compra, c.fecha, p.nombre AS proveedor, c.total
        FROM compras c
        JOIN proveedores p ON c.id_proveedor = p.id_proveedor
        ORDER BY c.id_compra DESC
    """)
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    print("\n--- COMPRAS ---")
    print(f"{'ID':<8} {'Fecha':<15} {'Proveedor':<25} {'Total'}")
    print("-" * 60)
    for f in filas:
        print(f"{f[0]:<8} {str(f[1]):<15} {f[2]:<25} ${f[3]}")
    if filas and confirmar("\n¿Ver el detalle de una compra?"):
        ver_detalle_compra()
