/*Usado el 09/10*/
INSERT INTO productos (nombre, precio, stock) VALUES
	('Disco Empanadas Criolla 13 cm', 1500, 250)
    ;
INSERT INTO productos (nombre, precio, stock) VALUES
	('Disco Empanadas Criolla 11 cm', 1350, 100),
    ('Disco Empanadas Criolla 14 cm', 1650, 25),
    ('Disco Empanadas Criolla 16 cm', 2620, 10),
    ('Disco Empanadas Criolla 18 cm', 2800, 2),
    ('Disco Empanadas Criolla 22 cm', 3900, 4),
    ('Pascualinas Criollas ', 1600, 20);
/*Insertado el dia 15/10 */
/*Insumos*/
INSERT INTO insumos (nombre, unidad_medida, inventario) VALUES
	('Harina 0000', 'Kg', 50),
    ('Harina 000', 'Kg', 3), 
    ('Grasa', 'Kg', 130),
    ('Sal', 'Kg', 65),
    ('Bolsa 25x35', 'Rollo', 5);
/*Proveedores*/
INSERT INTO proveedores (nombre, telefono, email, domicilio) VALUES
	('Luis', 2615366951, 'luisharina@gmail.com', 'Gobernador Gonzalez 2658 - Ciudad'),
	('Ferro', 2616574215, 'grasaferro@gmail.com', 'Godoy Cruz 3365 - Guaymallen'),
	('Red Globo', 2612754125, 'redglobo@gmail.com', 'San Martin 2675 - Las Heras'), 
	('La Piramide', 2613547865, 'lapiramide@gmail.com', 'Independencia 265 - Las Heras');

/*Cargar compras 16/10 */
INSERT INTO compras (fecha, total, id_proveedor) VALUES
	('26-10-09', 1126000, 1),
    ('26-10-10', 420000, 2),
    ('26-10-10', 32700, 4),
    ('26-10-11', 41500, 3);
/*Cargar detalle de compra, luego de cargar compras */    
INSERT INTO detalle_compra (id_compra, id_insumo, cantidad, precio_unitario) VALUES
	();
select * from compras
    