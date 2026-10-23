/*Usado el 09/10*/
INSERT INTO productos (nombre, precio, stock) VALUES
	('Disco Empanadas Criolla 13 cm', 1500, 250),
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
    (2, 3, 2, 210000 ),
    (3, 4, 3, 10900 ),
    (4, 5, 5, 8300 );
/*Carga de recetas 18/10. Actualizado 23/10: cantidades por paquete de una docena
  (cantidad de la tanda / docenas que rinde la tanda) */
INSERT INTO recetas (id_producto, id_insumo, cantidad_elaboracion) VALUES
	(1, 1, 25 / 60), /* 13 cm: una tanda rinde 60 docenas */
    (1, 2, 1 / 60),
    (1, 3, 0.5 / 60),
    (1, 4, 0.45 / 60),
    (1, 5, 0.15 / 60),
    (2, 1, 25 / 70), /* 11 cm: una tanda rinde 70 docenas */
    (2, 2, 1 / 70),
    (2, 3, 0.5 / 70),
    (2, 4, 0.45 / 70),
    (2, 5, 0.11 / 70),
    (3, 1, 25 / 50), /* 14 cm: una tanda rinde 50 docenas */
    (3, 2, 1 / 50),
    (3, 3, 0.5 / 50),
    (3, 4, 0.45 / 50),
    (3, 5, 0.15 / 50),
    (4, 1, 25 / 35), /* 16 cm: una tanda rinde 35 docenas */
    (4, 2, 1 / 35),
    (4, 3, 0.5 / 35),
    (4, 4, 0.45 / 35),
    (4, 5, 0.14 / 35),
    (5, 1, 25 / 30), /* 18 cm: una tanda rinde 30 docenas */
    (5, 2, 1 / 30),
    (5, 3, 0.5 / 30),
    (5, 4, 0.45 / 30),
    (5, 5, 0.11 / 30),
    (6, 1, 25 / 25), /* 22 cm: una tanda rinde 25 docenas */
    (6, 2, 1 / 25),
    (6, 3, 0.5 / 25),
    (6, 4, 0.45 / 25),
    (6, 5, 0.15 / 25),
    (7, 1, 25 / 24), /* Pascualina: una tanda rinde 24 docenas */
    (7, 2, 1 / 24),
    (7, 3, 0.5 / 24),
    (7, 4, 0.45 / 24),
    (7, 5, 0.12 / 24);
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
INSERT INTO usuarios (email, password, rol) VALUES
	('mrodrigo@tapitas.com', 'muysegura', 'admin'),
    ('lbarrera@tapitas.com', 'masomenos', 'compras'),
    ('mpacifico@tapitas.com', 'regular', 'ventas'),
    ('ebitar@tapitas.com', 'insegura', 'elaboracion');

select * from usuarios;
select * from recetas;
    