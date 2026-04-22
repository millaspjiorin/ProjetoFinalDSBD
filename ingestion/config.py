import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "https://api.portaldatransparencia.gov.br/api-de-dados")
TIMEOUT = 60

API_KEY_NAME = os.getenv("API_KEY_NAME")
API_KEY_VALUE = os.getenv("API_KEY_VALUE")

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 8123))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE")

DATA_LAKE_BASE_PATH = os.getenv("DATA_LAKE_BASE_PATH", "/data")