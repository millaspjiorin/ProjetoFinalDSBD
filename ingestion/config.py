import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL", "https://api.portaldatransparencia.gov.br/api-de-dados")
TIMEOUT = 60

API_KEY_NAME = os.getenv("API_KEY_NAME")
API_KEY_VALUE = os.getenv("API_KEY_VALUE")

DATA_LAKE_BASE_PATH = os.getenv("DATA_LAKE_BASE_PATH", "/data")