import os
from dotenv import load_dotenv

load_dotenv()  # carga el .env

BASE_URL = os.getenv("API_BASE_URL", "https://api.portaldatransparencia.gov.br/api-de-dados")
TIMEOUT = 60

API_KEY_NAME = os.getenv("API_KEY_NAME")
API_KEY_VALUE = os.getenv("API_KEY_VALUE")
