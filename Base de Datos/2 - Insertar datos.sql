/*Usado el 09/10*/
INSERT INTO productos (nombre, precio, stock, activo) VALUES
	('Disco Empanadas Criolla 13 cm', 1500, 250, 1);
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
/*Carga de detalle_compra*/   
INSERT INTO detalle_compra (id_compra, id_insumo, cantidad, precio_unitario) VALUES
	(1, 1, 50, 21500 ),
    (1, 2, 3, 17000 ),
    (1, 3, 2, 210000 ),
    (1, 4, 3, 10900 ),
    (1, 5, 8, 8300 );
/*Carga de recetas 18/10 */
INSERT INTO recetas (id_producto, id_insumo, cantidad_elaboracion) VALUES
	(1, 1, 25),
    (1, 2, 1),
    (1, 3, 0.5),
    (1, 4, 0.45),
    (1, 5, 0.15),
    (2, 1, 25),
    (2, 2, 1),
    (2, 3, 0.5),
    (2, 4, 0.45),
    (2, 5, 0.11),
    (3, 1, 25),
    (3, 2, 1),
    (3, 3, 0.5),
    (3, 4, 0.45),
    (3, 5, 0.15),
    (4, 1, 25),
    (4, 2, 1),
    (4, 3, 0.5),
    (4, 4, 0.45),
    (4, 5, 0.14),
    (5, 1, 25),
    (5, 2, 1),
    (5, 3, 0.5),
    (5, 4, 0.45),
    (5, 5, 0.11),
    (6, 1, 25),
    (6, 2, 1),
    (6, 3, 0.5),
    (6, 4, 0.45),
    (6, 5, 0.5);
INSERT INTO recetas (id_producto, id_insumo, cantidad_elaboracion) VALUES
	(7, 1, 25),
    (7, 2, 1),
    (7, 3, 0.5),
    (7, 4, 0.45),
    (7, 5, 0.12);
/*Carga de Elaboracion 18/10 */
INSERT INTO elaboracion (fecha, cantidad_producida, id_producto) VALUES
	('26-10-12', 100, 1),
    ('26-10-12', 25, 2),
    ('26-10-12', 10, 3),
    ('26-10-12', 2, 4),
    ('26-10-12', 4, 5),
    ('26-10-12', 20, 6),
    ('26-10-12', 250, 7);
/*Carga de Elaboracion 18/10 */
INSERT INTO elaboracion (fecha, cantidad_producida, id_producto) VALUES
	('26-10-13', 50, 1),
    ('26-10-13', 25, 2),
    ('26-10-13', 4, 3),
    ('26-10-13', 12, 6),
    ('26-10-13', 320, 7);
/*Carga de Clientes 18/10 */
INSERT INTO clientes (nombre, telefono, email) VALUES
('Juan Pérez', '+54 9 11 4567-8901', 'juan.perez@email.com'),
('María González', '+54 9 261 345-6789', 'maria.gonzalez@email.com'),
('Lucas Rodríguez', '+54 9 351 234-5678', 'lucas.rodriguez@email.com'),
('Sofia López', '+54 9 11 9876-5432', 'sofia.lopez@email.com'),
('Carlos Gómez', '+54 9 261 876-5432', 'carlos.gomez@email.com');
/*Carga de usuarios 19/10 */
INSERT INTO usuarios (email, contrasenia, rol) VALUES
	('mrodrigo@tapitas.com', 'muysegura', 'admin'),
    ('lbarrera@tapitas.com', 'masomenos', 'compras'),
    ('mpacifico@tapitas.com', 'regular', 'ventas'),
    ('ebitar@tapitas.com', 'insegura', 'elaboracion');

select * from usuarios;
select * from recetas;
    