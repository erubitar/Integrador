CREATE TABLE clientes(
	id_cliente INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100)
    );
CREATE TABLE proveedores(
	id_proveedor INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    domicilio VARCHAR(50)
);
CREATE TABLE insumos(
	id_insumo INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    unidad_medida VARCHAR(10),
    inventario DECIMAL(10,2) 
);
CREATE TABLE productos(
	id_producto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    precio DECIMAL(10,2),
    stock INT,
    activo BOOLEAN NOT NULL DEFAULT 1
);
CREATE TABLE ventas(
	id_venta INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    total DECIMAL(12,2),
    id_cliente INT NOT NULL,
    CONSTRAINT fk_venta_cliente 
        FOREIGN KEY (id_cliente) 
        REFERENCES clientes(id_cliente)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
CREATE TABLE detalle_venta(
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    
    PRIMARY KEY (id_venta, id_producto),
 
    CONSTRAINT fk_detalle_venta
        FOREIGN KEY (id_venta) 
        REFERENCES ventas(id_venta) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
        
    CONSTRAINT fk_detalle_producto 
        FOREIGN KEY (id_producto) 
        REFERENCES productos(id_producto) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);
CREATE TABLE compras(
	id_compra INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    total DECIMAL(12,2),
    id_proveedor INT NOT NULL,
    CONSTRAINT fk_compra_proveedor 
        FOREIGN KEY (id_proveedor) 
        REFERENCES proveedores(id_proveedor)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
CREATE TABLE detalle_compra(
    id_compra INT NOT NULL,
    id_insumo INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    
    PRIMARY KEY (id_compra, id_insumo),
 
    CONSTRAINT fk_detalle_compra 
        FOREIGN KEY (id_compra) 
        REFERENCES compras(id_compra) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
        
    CONSTRAINT fk_detalle_insumo 
        FOREIGN KEY (id_insumo) 
        REFERENCES insumos(id_insumo) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);
CREATE TABLE recetas (
    id_producto INT NOT NULL,
    id_insumo INT NOT NULL,
    cantidad_elaboracion DECIMAL(10, 4) NOT NULL,
    
    PRIMARY KEY (id_producto, id_insumo),
    
    CONSTRAINT fk_receta_producto
        FOREIGN KEY (id_producto) 
        REFERENCES productos(id_producto) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
        
    CONSTRAINT fk_receta_insumo 
        FOREIGN KEY (id_insumo) 
        REFERENCES insumos(id_insumo) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);
CREATE TABLE elaboracion(
	id_elaboracion INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    cantidad_producida INT NOT NULL,
    id_producto INT NOT NULL,
    
    CONSTRAINT fk_elaboracion_producto
        FOREIGN KEY (id_producto) 
        REFERENCES productos(id_producto) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
    );
CREATE TABLE usuarios(
	id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(30) NOT NULL,
    password VARCHAR(20) NOT NULL,
    rol VARCHAR(20) NOT NULL
);
