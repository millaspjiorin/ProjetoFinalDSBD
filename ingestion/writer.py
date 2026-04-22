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
            .getOrCreate()
        )

    def write_bronze(
        self,
        dataset: str,
        data: List[Dict[str, Any]],
        pacote: str,
        endpoint: str,
        ingestion_id: str,
        source: str = "Portal da Transparencia",
    ) -> None:
        if not data:
            return

        df = self.spark.createDataFrame(data)

        df = df.withColumn("pacote", lit(pacote))
        df = df.withColumn("__endpoint", lit(endpoint))
        df = df.withColumn("__ingestion_id", lit(ingestion_id))
        df = df.withColumn("__source", lit(source))

        output_path = f"{self.base_path}/bronze/{dataset}"

        writer = df.write.mode("append")
        writer = writer.partitionBy("ano")
        writer.parquet(output_path)

        print(f"Inseridos {df.count()} registros em {output_path}", flush=True)

    def stop(self) -> None:
        self.spark.stop()
