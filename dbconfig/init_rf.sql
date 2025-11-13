-- Conectarse a la base de datos recién creada
\connect db_postgres;

-- ======================================
-- Tabla: facturas
-- ======================================
CREATE TABLE IF NOT EXISTS facturas (
    id BIGSERIAL PRIMARY KEY,
    cuf VARCHAR(50) NOT NULL UNIQUE,
    nit_emisor VARCHAR(20) NOT NULL,
    razon_social_emisor VARCHAR(100) NOT NULL,
    fecha_emision TIMESTAMP NOT NULL,
    nit_receptor VARCHAR(20) NOT NULL,
    monto_total NUMERIC(10,2) NOT NULL,
    monto_descuento NUMERIC(10,2) DEFAULT 0,
    codigo_metodo_pago INT NOT NULL,
    codigo_control VARCHAR(50),
    firma_digital TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- ======================================
-- Tabla: detalles
-- ======================================
CREATE TABLE IF NOT EXISTS detalles (
    id BIGSERIAL PRIMARY KEY,
    factura_id BIGINT NOT NULL REFERENCES facturas(id) ON DELETE CASCADE ON UPDATE CASCADE,
    descripcion VARCHAR(200) NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario NUMERIC(10,2) NOT NULL
);

-- ======================================
-- Índices
-- ======================================
CREATE INDEX IF NOT EXISTS idx_facturas_cuf ON facturas (cuf);
CREATE INDEX IF NOT EXISTS idx_detalles_factura_id ON detalles (factura_id);

-- ======================================
-- Datos de ejemplo
-- ======================================

-- 🔹 Factura 1: Venta de laptop
INSERT INTO facturas (cuf, nit_emisor, razon_social_emisor, fecha_emision, nit_receptor, monto_total, monto_descuento, codigo_metodo_pago, codigo_control, firma_digital)
VALUES (
    '3E4F56A7B9CDE1234567890123456789',
    '1234567011',
    'EMPRESA S.A.',
    NOW(),
    '9876543012',
    1500.50,
    0.00,
    1,
    'A1B2C3D4E5F6',
    'MIIC...QAB'
);

INSERT INTO detalles (factura_id, descripcion, cantidad, precio_unitario)
VALUES 
((SELECT id FROM facturas WHERE cuf = '3E4F56A7B9CDE1234567890123456789'), 'Laptop Lenovo', 1, 1500.50);

-- 🔹 Factura 2: Venta de artículos de oficina
INSERT INTO facturas (cuf, nit_emisor, razon_social_emisor, fecha_emision, nit_receptor, monto_total, monto_descuento, codigo_metodo_pago, codigo_control, firma_digital)
VALUES (
    '7A9B12C34D56E78F901234567890ABCD',
    '1234567011',
    'EMPRESA S.A.',
    NOW(),
    '9988776655',
    345.75,
    10.00,
    2,
    'Z9Y8X7W6V5U4',
    'MIIC...XYZ'
);

INSERT INTO detalles (factura_id, descripcion, cantidad, precio_unitario)
VALUES 
((SELECT id FROM facturas WHERE cuf = '7A9B12C34D56E78F901234567890ABCD'), 'Paquete de hojas A4 (500)', 2, 25.50),
((SELECT id FROM facturas WHERE cuf = '7A9B12C34D56E78F901234567890ABCD'), 'Impresora HP DeskJet 2700', 1, 295.00);

-- 🔹 Factura 3: Venta de mobiliario
INSERT INTO facturas (cuf, nit_emisor, razon_social_emisor, fecha_emision, nit_receptor, monto_total, monto_descuento, codigo_metodo_pago, codigo_control, firma_digital)
VALUES (
    'ABC123DEF456GHI789JKL012MNO345PQ',
    '1234567011',
    'EMPRESA S.A.',
    NOW(),
    '1112223334',
    1020.00,
    0.00,
    3,
    'CTRL987654321',
    'MIIC...LMN'
);

INSERT INTO detalles (factura_id, descripcion, cantidad, precio_unitario)
VALUES 
((SELECT id FROM facturas WHERE cuf = 'ABC123DEF456GHI789JKL012MNO345PQ'), 'Escritorio de madera', 1, 450.00),
((SELECT id FROM facturas WHERE cuf = 'ABC123DEF456GHI789JKL012MNO345PQ'), 'Silla ergonómica', 2, 285.00);