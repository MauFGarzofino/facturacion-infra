-- Conectarse a la base de datos recién creada
\connect db_postgres;

CREATE TYPE estado_factura AS ENUM ('ACTIVO', 'ANULADO');
-- ======================================
-- Tabla: facturas
-- ======================================
CREATE TABLE IF NOT EXISTS facturas (
    id BIGSERIAL PRIMARY KEY,
    cuf VARCHAR(100) NOT NULL UNIQUE,
    cufd VARCHAR(100) NOT NULL UNIQUE,
    nit_emisor VARCHAR(100) NOT NULL,
    codigo_sucursal VARCHAR(100) NOT NULL,
    codigo_pv VARCHAR(100) NOT NULL,
    razon_social_emisor VARCHAR(100) NOT NULL,
    fecha_emision TIMESTAMP NOT NULL,
    nit_empresa VARCHAR(20) NOT NULL,
    monto_total NUMERIC(10,2) NOT NULL,
    codigo_control VARCHAR(50),
    estado estado_factura NOT NULL,
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

INSERT INTO facturas (
    cuf, cufd, nit_emisor, codigo_sucursal, codigo_pv,
    razon_social_emisor, fecha_emision, nit_empresa,
    monto_total, codigo_control, estado
) VALUES
(
    'CUF0001', 'CUFD0001', '1234567011', '001', '001',
    'Empresa Alfa SRL', '2025-01-10 10:25:00', '78945601',
    1500.50, 'CTRL-A1', 'ACTIVO'
),
(
    'CUF0002', 'CUFD0002', '1234567011', '001', '002',
    'Empresa Alfa SRL', '2025-01-11 08:40:00', '78945601',
    850.00, 'CTRL-A2', 'ACTIVO'
),
(
    'CUF0003', 'CUFD0003', '9876543219', '002', '001',
    'Distribuidora Beta SA', '2025-01-15 15:10:00', '45678912',
    2300.75, 'CTRL-B1', 'ANULADO'
),
(
    'CUF0004', 'CUFD0004', '9876543219', '002', '002',
    'Distribuidora Beta SA', '2025-01-20 12:00:00', '45678912',
    120.99, 'CTRL-B2', 'ACTIVO'
);

INSERT INTO detalles (factura_id, descripcion, cantidad, precio_unitario) VALUES
-- Factura 1
(1, 'Producto A', 2, 300.00),
(1, 'Producto B', 1, 900.50),
(1, 'Servicio X', 1, 300.00),

-- Factura 2
(2, 'Producto C', 2, 200.00),
(2, 'Producto D', 1, 450.00),

-- Factura 3 (ANULADA)
(3, 'Artículo Z', 3, 500.25),
(3, 'Servicio Y', 1, 800.00),

-- Factura 4
(4, 'Producto Q', 1, 120.99);