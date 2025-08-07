from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from elastic import search_media, search_media_for_infinite_scroll
from utils import build_media_url, DB_TYPE, SORT_ORDER


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins = ['*'], allow_methods =['*'], allow_headers = ['*'])

@app.get("/api")
def read_root():
    return {"message": "Hello World"}

@app.get('/api/media/search')
def search(query: str = Query(...), db: str = Query(None), page:int = Query(1), pagesize:int = Query(20), fotografen: str = Query(None), datefrom: str = Query(None), dateto: str = Query(None), datesort: str = Query(None), isscroll: bool = Query(False), scrollid: str = Query(None)):
    
    # If layput is infinite scroll and no scrollId, initialize a new scroll search
    isscroll = False  # Uncomment this line. As coding challenge user doesn't have persmission for scroll API set to False 
    if isscroll and not scrollid:
        # Call the function to fetch the first batch of data
        results, scroll_id = search_media(query,db, page, pagesize, is_fallback=False, fotografen=fotografen, date_from=datefrom, date_to=dateto, date_sort=datesort, is_scroll=isscroll)

    if isscroll and scrollid:
        results, scroll_id = search_media_for_infinite_scroll(scrollid)
    
    # If layout is pagination based with limited result window
    if not isscroll:
        results,total = search_media(query,db, page, pagesize, is_fallback=False, fotografen=fotografen, date_from=datefrom, date_to=dateto, date_sort=datesort, is_scroll=isscroll)
    
    formatted = []
    if_fallback = False

    if not results:
        if_fallback = True
        results,total = search_media(query,db, page, pagesize, is_fallback=True, fotografen=fotografen, date_from=datefrom, date_to=dateto, date_sort=datesort, is_scroll=isscroll)

    # formatting by adding thumbnail url using bildnummer
    for item in results:
        media_id = item.get("bildnummer", '')
        db = item.get("db", DB_TYPE.STOCK)
        if media_id:
            item["thumbnail_url"] = build_media_url(db, media_id)
        formatted.append(item)

    if isscroll and scroll_id is not None:
        return {"results": formatted, "page_size": pagesize, "scroll_id": scroll_id, "fallback_used": if_fallback}
    if isscroll and scroll_id is None:
        return {"results": formatted, "page_size": pagesize, "scroll_id": None, "fallback_used": if_fallback}
    else:
        return {"results": formatted,"total": total, "page": page, "page_size": pagesize, "fallback_used": if_fallback}