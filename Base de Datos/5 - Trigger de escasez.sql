/* Avisos de escasez de insumos 23/10
   Cuando baja el inventario de un insumo, el trigger llama al procedimiento
   verificar_escasez, que guarda un aviso si quedan menos de 30 de harina
   o menos de 10 de sal. */

CREATE TABLE IF NOT EXISTS avisos_escasez(
    id_aviso INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL,
    id_insumo INT NOT NULL,
    inventario DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_aviso_insumo
        FOREIGN KEY (id_insumo)
        REFERENCES insumos(id_insumo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP PROCEDURE IF EXISTS verificar_escasez;

DELIMITER //
CREATE PROCEDURE verificar_escasez(IN p_id_insumo INT, IN p_nombre VARCHAR(20), IN p_inventario DECIMAL(10,2))
BEGIN
    IF (p_nombre LIKE 'Harina%' AND p_inventario < 30)
       OR (p_nombre = 'Sal' AND p_inventario < 10) THEN
        INSERT INTO avisos_escasez (fecha, id_insumo, inventario)
        VALUES (NOW(), p_id_insumo, p_inventario);
    END IF;
END //
DELIMITER ;

DROP TRIGGER IF EXISTS tr_escasez_insumos;

DELIMITER //
CREATE TRIGGER tr_escasez_insumos
AFTER UPDATE ON insumos
FOR EACH ROW
BEGIN
    /* Solo cuando el inventario baja (elaboracion o correccion manual) */
    IF NEW.inventario < OLD.inventario THEN
        CALL verificar_escasez(NEW.id_insumo, NEW.nombre, NEW.inventario);
    END IF;
END //
DELIMITER ;

/* Para ver los avisos */
/* SELECT a.fecha, i.nombre, a.inventario FROM avisos_escasez a JOIN insumos i USING(id_insumo); */
