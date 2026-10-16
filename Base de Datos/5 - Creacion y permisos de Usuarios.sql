/* Creacion de Usuarios*/
CREATE USER 'ebitar'@'localhost' IDENTIFIED BY '1234';
CREATE USER 'mpacifico'@'localhost' IDENTIFIED BY '1234';
CREATE USER 'mrodrigo'@'localhost' IDENTIFIED BY '1234';
CREATE USER 'lbarrera'@'localhost' IDENTIFIED BY '1234';

/*Permisos de Ususarios*/
GRANT SELECT, INSERT, UPDATE, DELETE
ON integrador.* TO 'ebitar'@'localhost';
GRANT SELECT, INSERT, UPDATE
ON integrador.* TO 'mpacifico'@'localhost';
GRANT SELECT, INSERT, UPDATE
ON integrador.* TO 'mrodrigo'@'localhost';
GRANT SELECT
ON integrador.* TO 'lbarrera'@'localhost';
SHOW GRANTS FOR 'lbarrera'@'localhost';