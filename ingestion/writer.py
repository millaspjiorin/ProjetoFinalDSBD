import clickhouse_connect
from typing import List, Dict
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
        data: List[Dict],
        pacote: str
    ):
        if not data:
            return

        columns = [
            "ano",
            "orgao",
            "codigoOrgao",
            "orgaoSuperior",
            "codigoOrgaoSuperior",
            "empenhado",
            "liquidado",
            "pago",
            "pacote"
        ]

        rows = [
            [
                record.get("ano"),
                record.get("orgao"),
                record.get("codigoOrgao"),
                record.get("orgaoSuperior"),
                record.get("codigoOrgaoSuperior"),
                record.get("empenhado"),
                record.get("liquidado"),
                record.get("pago"),
                pacote
            ]
            for record in data
        ]

        self.client.insert(
            table,
            rows,
            column_names=columns
        )

        print(f"Inseridos {len(rows)} registros")
        

    

