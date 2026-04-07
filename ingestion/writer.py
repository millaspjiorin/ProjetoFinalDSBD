import clickhouse_connect
from typing import List, Dict, Any
from .config import (
    CLICKHOUSE_HOST,
    CLICKHOUSE_PORT,
    CLICKHOUSE_USER,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_DATABASE,
)



class ClickHouseWriter:
    def __init__(
        self
    ):
        self.client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE
        )

    def insert_bronze(
        self,
        table: str,
        data: List[Dict[str, Any]],
        columns: List[str],
        pacote: str,
        endpoint: str,
        ingestion_id: str,
        source: str = "Portal da Transparencia",
    ) -> None:
        if not data:
            return

        extra_fields = {
            "pacote": pacote,
            "__endpoint": endpoint,
            "__ingestion_id": ingestion_id,
            "__source": source
        }

        rows = [
            [
                extra_fields[col] if col in extra_fields else record.get(col)
                for col in columns
            ]
            for record in data
        ]

        self.client.insert(
            table,
            rows,
            column_names=columns
        )

        print(f"Inseridos {len(rows)} registros em {table}")
        

    

