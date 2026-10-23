/* Registra una elaboracion: descuenta los insumos segun la receta del producto
   y suma la cantidad producida al stock. 22/10 */
DROP PROCEDURE IF EXISTS registrar_elaboracion;

DELIMITER //
CREATE PROCEDURE registrar_elaboracion(IN p_id_producto INT, IN p_cantidad INT)
BEGIN
    INSERT INTO elaboracion (fecha, cantidad_producida, id_producto)
    VALUES (CURDATE(), p_cantidad, p_id_producto);

    UPDATE insumos i
    JOIN recetas r ON r.id_insumo = i.id_insumo
    SET i.inventario = i.inventario - r.cantidad_elaboracion * p_cantidad
    WHERE r.id_producto = p_id_producto;

    UPDATE productos
    SET stock = stock + p_cantidad
    WHERE id_producto = p_id_producto;
END //
DELIMITER ;

/* Ejemplo de uso: elaborar 10 unidades del producto 1 */
/* CALL registrar_elaboracion(1, 10); */
