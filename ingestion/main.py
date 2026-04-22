import uuid
from typing import List, Dict

from ingestion.config import API_KEY_NAME, API_KEY_VALUE, BASE_URL
from ingestion.client import APIClient
from ingestion.fetcher import APIFetcher
from ingestion.writer import SparkParquetWriter
from ingestion.params import PACOTES_ORGAOS, ANOS, PACOTES_FUNCOES

def main() -> None:
    ingestion_id = str(uuid.uuid4())

    print(f"Iniciando ingestao {ingestion_id}", flush=True)

    client = APIClient(
        base_url=BASE_URL,
        api_key_name=API_KEY_NAME,
        api_key_value=API_KEY_VALUE
    )

    fetcher = APIFetcher(client)
    writer = SparkParquetWriter()

    try:
        total = run_despesas_pipeline(
            fetcher=fetcher,
            writer=writer,
            anos=ANOS,
            endpoint="/api-de-dados/despesas/por-orgao",
            param_name="orgaoSuperior",
            pacotes=PACOTES_ORGAOS,
            table_name="despesas_por_orgao",
            ingestion_id=ingestion_id
        )

        print(f"Total de registros escritos despesas por orgao: {total}", flush=True)

        total = run_despesas_pipeline(
            fetcher=fetcher,
            writer=writer,
            anos=ANOS,
            endpoint="/api-de-dados/despesas/por-funcional-programatica",
            param_name="funcao",
            pacotes=PACOTES_FUNCOES,
            table_name="despesas_funcional_programatica",
            ingestion_id=ingestion_id
        )

        print(f"Total de registros escritos despesas funcional programatica: {total}", flush=True)

    finally:
        writer.stop()


def run_despesas_pipeline(
    fetcher: APIFetcher,
    writer: SparkParquetWriter,
    anos: List[int],
    endpoint: str,
    param_name: str,
    pacotes: Dict[str, List[str]],
    table_name: str,
    ingestion_id: str
) -> int:
    total = 0

    for pacote, valores in pacotes.items():
        print(f"\nPacote: {pacote}", flush=True)

        for ano in anos:
            for valor in valores:
                print(f"Ano {ano} | {param_name} {valor}", flush=True)

                data = fetcher.fetch_all(
                    endpoint=endpoint,
                    base_params={
                        "ano": ano,
                        param_name: valor
                    }
                )

                if not data:
                    continue

                writer.write_bronze(
                    table_name=table_name,
                    data=data,
                    pacote=pacote,
                    endpoint=endpoint,
                    ingestion_id=ingestion_id
                )

                total += len(data)

    return total


if __name__ == "__main__":
    main()
