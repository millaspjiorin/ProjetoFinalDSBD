
from .config import API_KEY_NAME,API_KEY_VALUE,BASE_URL
from .client import APIClient
from .fetcher import APIFetcher
from ingestion.params import PACOTES_ORGAOS, ANOS


def main():
    client = APIClient(
        base_url=BASE_URL,
        api_key_name=API_KEY_NAME,
        api_key_value=API_KEY_VALUE
    )

    fetcher = APIFetcher(client)

    all_results = []

    for pacote, orgaos in PACOTES_ORGAOS.items():
        print(f"\n📦 Procesando pacote: {pacote}")

        for ano in ANOS:
            for orgao in orgaos:
                print(f"➡️ Ano {ano} | Órgão {orgao}")

                data = fetcher.fetch_all(
                    endpoint="/api-de-dados/despesas/por-orgao",
                    base_params={
                        "ano": ano,
                        "orgaoSuperior": orgao
                    }
                )

                all_results.extend(data)
                print(data)

    return all_results


if __name__ == "__main__":
    main()