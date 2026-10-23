/* Creacion de Usuarios*/
CREATE USER 'ebitar'@'localhost' IDENTIFIED BY '1234';
CREATE USER 'mpacifico'@'localhost' IDENTIFIED BY '1234';
CREATE USER 'mrodrigo'@'localhost' IDENTIFIED BY '1234';
CREATE USER 'lbarrera'@'localhost' IDENTIFIED BY '1234';

/*Permisos de Ususarios (segun lo que hace cada rol en el programa)*/
/* ebitar - elaboracion: registra elaboraciones, no elimina */
GRANT SELECT, INSERT, UPDATE
ON integrador.* TO 'ebitar'@'localhost';
/* mpacifico - ventas: registra ventas y gestiona clientes */
GRANT SELECT, INSERT, UPDATE, DELETE
ON integrador.* TO 'mpacifico'@'localhost';
/* mrodrigo - admin: gestiona usuarios, clientes, proveedores, productos e insumos */
GRANT SELECT, INSERT, UPDATE, DELETE
ON integrador.* TO 'mrodrigo'@'localhost';
/* lbarrera - compras: registra compras y gestiona proveedores e insumos */
GRANT SELECT, INSERT, UPDATE, DELETE
ON integrador.* TO 'lbarrera'@'localhost';
SHOW GRANTS FOR 'lbarrera'@'localhost';