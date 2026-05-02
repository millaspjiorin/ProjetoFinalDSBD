INSTALL iceberg;
LOAD iceberg;

CREATE SCHEMA IF NOT EXISTS bronze;

CREATE OR REPLACE VIEW bronze.despesas_por_orgao AS
SELECT *
FROM iceberg_scan(
    '/data/warehouse/bronze/despesas_por_orgao',
    allow_moved_paths = true
);

CREATE OR REPLACE VIEW bronze.despesas_funcional_programatica AS
SELECT *
FROM iceberg_scan(
    '/data/warehouse/bronze/despesas_funcional_programatica',
    allow_moved_paths = true
);