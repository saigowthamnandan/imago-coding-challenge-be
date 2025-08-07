from config import *
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from utils import DB_TYPE, SORT_ORDER
import urllib3
from typing import List, Dict, Tuple, Optional

urllib3.disable_warnings()

es = Elasticsearch(hosts=[ELASTIC_SEARCH_HOST], basic_auth=(ELASTIC_SEARCH_USER, ELASTIC_SEARCH_PASSWORD), verify_certs= False, ssl_show_warn=False,)
def search_media(query: str, db_filter: Optional[DB_TYPE] = None, page:int = 1, size:int = 20, fotografen: Optional[str] = None, date_from: Optional[str] = None, date_to: Optional[str] = None, is_fallback:bool=False, date_sort: Optional[SORT_ORDER] = None, is_scroll:bool=False)-> Tuple[List[Dict], int]:
    must_clauses = []
    sort_clauses = []
    if is_fallback:
        must_clauses.append({
            "match_all": {}
        })
    else:
        if query:
            must_clauses.append({
                "match": {
                    "suchtext": {
                        "query": query,
                        "fuzziness": "AUTO"
                    }
                }
            })

    if db_filter:
        must_clauses.append({
            "term": {
                "db": str(db_filter)
            }
        })

    if fotografen:
        must_clauses.append({
            "match": {
                "fotografen": {
                    "query": fotografen,
                    "fuzziness": "AUTO",
                    "operator": "and"
                }
            }
        })


    if date_from or date_to:
        date_range = {}
        if date_from:
            date_range["gte"] = date_from
        if date_to:
            date_range["lte"] = date_to

        must_clauses.append({
            "range": {
                "datum": date_range
            }
        })

    if date_sort and (str(date_sort) == 'desc' or str(date_sort) == 'asc'):
        sort_clauses.append({
            "datum": {
                "order": str(date_sort)
            }
        })
        
    print(sort_clauses, str(date_sort) == 'desc')
    search_body = {
        # "size": size,
        "query": {
            "bool": {
                "must": must_clauses
            }
        },
        "sort": sort_clauses
    }
    if not is_scroll:
        start = (page - 1) * size
        start = start if (start + size < 9970) else 9970
        search_body["from"] = start

    search_body["size"] = size
    
    print(search_body)
    

    try:
        total = 0
        scroll_id = None
        if is_scroll:
            scroll_time = "1m"
            res = es.search(index=INDEX_NAME, body=search_body, scroll=scroll_time)
        else:
            res = es.search(index=INDEX_NAME, body=search_body)
        results = []
        print(res)
        for hit in res["hits"]["hits"]:
            source = hit["_source"]
            results.append({
                "_id": hit["_id"],
                "bildnummer": source.get("bildnummer"),
                "suchtext": source.get("suchtext", ""),
                "db": source.get("db", "stock"),
                "datum": source.get("datum"),
                "fotografen": source.get("fotografen"),
            })

        if is_scroll:
            scroll_id = res["_scroll_id"]
            return results, scroll_id
        else:
            total = res["hits"]["total"]["value"]
            return results,total

    except TransportError as e:
        print(f"Error searching media: {e}")
        return [],0


def search_media_for_infinite_scroll(scroll_id: str)-> List[Dict]:
    try:
        scroll_time = "1m"
        response = es.scroll(scroll_id=scroll_id, scroll=scroll_time)
        new_scroll_id = response["_scroll_id"]
        results = []
        if not response["hits"]["hits"]:
            return [], None
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            results.append({
                "_id": hit["_id"],
                "bildnummer": source.get("bildnummer"),
                "suchtext": source.get("suchtext", ""),
                "db": source.get("db", "stock"),
                "datum": source.get("datum"),
                "fotografen": source.get("fotografen"),
            })
        return results, new_scroll_id
    except TransportError as e:
        print(f"Error searching media: {e}")
        return [], None