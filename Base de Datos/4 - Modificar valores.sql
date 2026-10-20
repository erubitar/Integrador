SELECT * FROM productos WHERE activo = TRUE;
/*Ejecutado 09/10*/
UPDATE productos set activo = 1 WHERE activo = 0; 
UPDATE productos set activo = TRUE WHERE activo = 1;

/* Compras mal cargadas, hacer UPDATE* Corregidos el 18/10 */
UPDATE detalle_compra set id_compra = 2 WHERE id_insumo = 3;
UPDATE detalle_compra set id_compra = 3 WHERE id_insumo = 4;
UPDATE detalle_compra set id_compra = 4 WHERE id_insumo = 5;
/*Borrado de un producto cargado dos veces por error 18/10 */
DELETE FROM productos WHERE id_producto = 8;