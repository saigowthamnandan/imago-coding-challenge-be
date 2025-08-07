# IMAGO Media Search Application

This repository contains **backend** components for a media search application that interacts with an Elasticsearch service. Backend is built with **FastAPI**.

The goal of the project is to retrieve media content stored in Elasticsearch and serve it to users in a user-friendly way, with the ability to filter, search, and paginate the media items.

---

## Backend (FastAPI)

### Description

The backend is built using **FastAPI** to handle the following tasks:

- Query the Elasticsearch server.
- Provide filtering, pagination, and sorting functionality.
- Handle both regular search and infinite scroll searches.

### LIVE HOISTED URL

### Prerequisites

1. **Python 3.8+**: Make sure you have Python installed on your machine.
2. **FastAPI**: The web framework used to build the backend API.
3. **ElasticSearch Client 7 or 8**: `elasticsearch` Python package to interact with Elasticsearch.

### Installation

1. Clone the repository:

```bash
   git clone https://github.com/saigowthamnandan/imago-coding-challenge-be.git
   cd imago-coding-challenge-be
```

2. Create a virtual environment:

```bash
    python -m venv .venv
    source .venv/bin/activate
```

3. Install Dependencies

```bash
    python -m pip install -r requirements.txt
```

4. Add ENV VARIABLES in the .env file as shown

```bash
    ELASTIC_SEARCH_HOST=your-elasticsearch-host
    ELASTIC_SEARCH_USER=your-username
    ELASTIC_SEARCH_PASSWORD=your-password
    INDEX_NAME=your-index
```

5. Start the server

```bash
    uvicorn main:app --reload
```

The backend will be running at http://localhost:8000

### Endpoints

- GET /api/media/search: The main endpoint to fetch media items based on search criteria

### Query Parameters

query: (string) The search query.

db: (string) Database type (e.g., "stock", "sport").

page: (integer) The page number.

pagesize: (integer) The number of results per page.

fotografen: (string) Photographer name.

datefrom: (string) Start date for filtering.

dateto: (string) End date for filtering.

datesort: (string) Sort order for the date field (either "asc" or "desc").

isscroll: (boolean) Enable or disable infinite scrolling but disable due to user permissions.

scrollid: (string) Scroll ID for infinite scrolling.
