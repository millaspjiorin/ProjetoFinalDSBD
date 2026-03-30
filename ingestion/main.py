from .config import API_KEY_NAME, API_KEY_VALUE, BASE_URL
from .client import APIClient
from .fetcher import APIFetcher
from .writer import ClickHouseWriter
from .params import PACOTES_ORGAOS, ANOS


def main():
    client = APIClient(
        base_url=BASE_URL,
        api_key_name=API_KEY_NAME,
        api_key_value=API_KEY_VALUE
    )

    fetcher = APIFetcher(client)

    writer = ClickHouseWriter()

    total_insertados = 0

    for pacote, orgaos in PACOTES_ORGAOS.items():
        print(f"Processando pacote: {pacote}")

        for ano in ANOS:
            for orgao in orgaos:
                print(f"Ano {ano} | Órgão {orgao}")

                data = fetcher.fetch_all(
                    endpoint="/api-de-dados/despesas/por-orgao",
                    base_params={
                        "ano": ano,
                        "orgaoSuperior": orgao
                    }
                )

                if not data:
                    print("Sem dados")
                    continue

                writer.insert_bronze(
                    table="despesas_bronze",
                    data=data,
                    pacote=pacote
                )

                total_insertados += len(data)

    print(f"Total de registros inseridos: {total_insertados}")


if __name__ == "__main__":
    main()