from os.path import join, dirname, abspath
from os import getenv
from dotenv import load_dotenv

dotenv_path = join(dirname(abspath(__file__)), '.env')
load_dotenv(dotenv_path)

SEARCH_MEDIA_BASE_URL = getenv('SEARCH_MEDIA_BASE_URL')
ELASTIC_SEARCH_HOST = getenv('ELASTIC_SEARCH_HOST')
ELASTIC_SEARCH_USER = getenv('ELASTIC_SEARCH_USER')
ELASTIC_SEARCH_PASSWORD = getenv('ELASTIC_SEARCH_PASSWORD')
INDEX_NAME = getenv('INDEX_NAME')
VERIFY_SSL = getenv('VERIFY_SSL', False)
