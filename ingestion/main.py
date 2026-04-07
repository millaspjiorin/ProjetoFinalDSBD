import uuid
from typing import List, Dict
from .config import API_KEY_NAME, API_KEY_VALUE, BASE_URL
from .client import APIClient
from .fetcher import APIFetcher
from .writer import ClickHouseWriter
from .params import PACOTES_ORGAOS, ANOS, PACOTES_FUNCOES
from .schemas import COLS_DESPESAS_FUNCIONAL_PROGRAMATICA, COLS_DESPESAS_POR_ORGAO

def main() -> None:
    ingestion_id = str(uuid.uuid4())
    
    client = APIClient(
        base_url=BASE_URL,
        api_key_name=API_KEY_NAME,
        api_key_value=API_KEY_VALUE
    )

    fetcher = APIFetcher(client)

    writer = ClickHouseWriter()

    # ================================
    # Despesas por orgao
    # ================================
    total = run_despesas_pipeline(
        fetcher=fetcher,
        writer=writer,
        anos=ANOS,
        endpoint="/api-de-dados/despesas/por-orgao",
        param_name="orgaoSuperior",
        pacotes=PACOTES_ORGAOS,
        table="bronze.despesas_por_orgao",
        columns=COLS_DESPESAS_POR_ORGAO,
        ingestion_id=ingestion_id
    )
    
    print(f"Total de registros inseridos despesas por orgao: {total}")

    # ================================
    # Despesas por funcao
    # ================================
    total = run_despesas_pipeline(
        fetcher=fetcher,
        writer=writer,
        anos=ANOS,
        endpoint="/api-de-dados/despesas/por-funcional-programatica",
        param_name="funcao",
        pacotes=PACOTES_FUNCOES,
        table="bronze.despesas_funcional_programatica",
        columns=COLS_DESPESAS_FUNCIONAL_PROGRAMATICA,
        ingestion_id=ingestion_id
    )

    print(f"Total de registros inseridos despesas funcional programatica: {total}")


def run_despesas_pipeline(
    fetcher: APIFetcher,
    writer: ClickHouseWriter,
    anos: List[int],
    endpoint: str,
    param_name: str,
    pacotes: Dict[str, List[str]],
    table: str,
    columns: List[str],
    ingestion_id: str
):
    total = 0

    for pacote, valores in pacotes.items():
        print(f"\n Pacote: {pacote}")

        for ano in anos:
            for valor in valores:
                print(f"Ano {ano} | {param_name} {valor}")

                data = fetcher.fetch_all(
                    endpoint=endpoint,
                    base_params={
                        "ano": ano,
                        param_name: valor
                    }
                )

                if not data:
                    continue

                writer.insert_bronze(
                    table=table,
                    data=data,
                    columns=columns,
                    pacote=pacote,
                    endpoint=endpoint,
                    ingestion_id=ingestion_id
                )

                total += len(data)

    return total




if __name__ == "__main__":
    main()