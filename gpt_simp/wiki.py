import json
from typing import Any, Dict, Optional

import requests
import wikipediaapi


def get_session() -> requests.Session:
    default_headers = dict()
    default_headers.setdefault(
        "User-Agent",
        "Wikipedia-API (https://github.com/martin-majlis/Wikipedia-API)",
    )
    session = requests.Session()
    session.headers.update(default_headers)
    return session


def fetch_wiki_article(name: str, params: Optional[Dict[str, Any]]=None, language="en", ) -> str:
    if params is None:
        params = dict()

    base_url = "https://" + language + ".wikipedia.org/w/api.php"
    params["format"] = "json"
    params["redirects"] = 1
    params["action"] = "query"
    params["prop"] =  "revisions"
    params["rvprop"] = "content"
    params["titles"] = name
    r = get_session().get(base_url, params=params, timeout=10)
    return r.json()


def get_wiki_article(name: str) -> str:
    article = fetch_wiki_article(name)
    return list(article["query"]["pages"].values())[0]["revisions"][0]["*"]


def publish(name: str, article: str) -> None:
    page = wikipediaapi.Wikipedia('simple').page(name)
    page.text = article
    page.save("Simplified by GPT-3 (and checked by a human).")

