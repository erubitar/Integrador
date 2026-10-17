/*Ejecutado 09/10*/
ALTER TABLE productos
	ADD activo INT NOT NULL;
    
ALTER TABLE productos 
MODIFY activo BOOLEAN NOT NULL;
