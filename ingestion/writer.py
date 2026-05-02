from typing import List, Dict, Any
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from ingestion.config import DATA_LAKE_BASE_PATH


class SparkParquetWriter:
    def __init__(self, base_path: str = DATA_LAKE_BASE_PATH) -> None:
        self.base_path = base_path
        self.spark = (
            SparkSession.builder
            .appName("portal-transparencia-ingestion")
            .master("local[*]")
            .config(
                "spark.sql.extensions",
                "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
            )
            .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
            .config("spark.sql.catalog.local.type", "hadoop")
            .config("spark.sql.catalog.local.warehouse", "/data/warehouse")
            .getOrCreate()
        )
        self.spark.sql(f"CREATE NAMESPACE IF NOT EXISTS local.bronze")
        
    def table_exists(self, database: str, table_name: str) -> bool:
        tables = self.spark.sql(f"SHOW TABLES IN local.{database}").collect()
        return any(row.tableName == table_name for row in tables)

    def write_bronze(
        self,
        table_name: str,
        data: List[Dict[str, Any]],
        pacote: str,
        endpoint: str,
        ingestion_id: str,
        ingestion_time: str,
        source: str = "Portal da Transparencia",
    ) -> None:
        if not data:
            return

        df = self.spark.createDataFrame(data)

        df = df.withColumn("pacote", lit(pacote))
        df = df.withColumn("__endpoint", lit(endpoint))
        df = df.withColumn("__ingestion_id", lit(ingestion_id))
        df = df.withColumn("__ingestion_time", lit(ingestion_time))
        df = df.withColumn("__source", lit(source))

        full_table_name = f"local.bronze.{table_name}"

        if self.table_exists("bronze", table_name):
            df.writeTo(full_table_name).append()
        else:
            (
                df.writeTo(full_table_name)
                .using("iceberg")
                .partitionedBy("ano")
                .tableProperty("format-version", "2")
                .create()
            )

        print(f"Inseridos {df.count()} registros em {full_table_name}", flush=True)

    def stop(self) -> None:
        self.spark.stop()
