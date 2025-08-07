from config import SEARCH_MEDIA_BASE_URL
from enum import Enum

class DB_TYPE(Enum):
    STOCK = "stock"
    SPORT = "sport"

class SORT_ORDER(Enum):
    ASC = "asc"
    DESC = "desc"

def format_bildnummer(bildnummer: str) -> str:
    return bildnummer.zfill(10)

def build_media_url(db: DB_TYPE, bildnummer: str) -> str:
    padded = format_bildnummer(bildnummer)
    return f"{SEARCH_MEDIA_BASE_URL}/{db}/{padded}/s.jpg"
