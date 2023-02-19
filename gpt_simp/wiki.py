import json
import os
from typing import Any, Dict, Optional

import requests
import typer
import wikipediaapi


def get_session() -> requests.Session:
    default_headers = dict()
    default_headers.setdefault(
        "User-Agent",
        "Wikipedia-API (https://github.com/jqhoogland/gpt-simp)",
    )
    session = requests.Session()
    session.headers.update(default_headers)
    return session


def fetch_wiki_article(name: str, params: Optional[Dict[str, Any]] = None, language="en", ) -> str:
    if params is None:
        params = dict()

    base_url = "https://" + language + ".wikipedia.org/w/api.php"
    params["format"] = "json"
    params["redirects"] = 1
    params["action"] = "query"
    params["prop"] = "revisions"
    params["rvprop"] = "content"
    params["titles"] = name
    r = get_session().get(base_url, params=params, timeout=10)
    return r.json()


def get_wiki_article(name: str) -> str:
    article = fetch_wiki_article(name)
    return list(article["query"]["pages"].values())[0]["revisions"][0]["*"]


def get_login_token(language: str, session: requests.Session) -> str:
    # Define the base URL for the Wikipedia API
    base_url = "https://" + language + ".wikipedia.org/w/api.php"

    # Set the parameters for the API request
    params = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json",
    }

    # Make the API request
    response = session.get(base_url, params=params)

    # Return the login token
    return response.json()["query"]["tokens"]["logintoken"]


def login(language: str, session: requests.Session) -> None:
    # Define the base URL for the Wikipedia API
    base_url = "https://" + language + ".wikipedia.org/w/api.php"

    # Set the parameters for the API request
    data = {
        "action": "login",
        "lgname": os.getenv("WIKIPEDIA_BOT_USER"),
        "lgpassword": os.getenv("WIKIPEDIA_BOT_PASSWORD"),
        "format": "json",
        # You need to implement get_login_token to retrieve the login token
        "lgtoken": get_login_token(language, session),
    }

    # Make the API request
    response = session.post(base_url, data=data)

    # Return the response as a JSON object
    return response.json()


def get_edit_token(language: str, session: requests.Session) -> str:
    # Define the base URL for the Wikipedia API
    base_url = "https://" + language + ".wikipedia.org/w/api.php"

    # Set the parameters for the API request
    params = {
        "action": "query",
        "meta": "tokens",
        "type": "csrf",
        "format": "json",
    }

    # Make the API request
    login(language, session)
    response = session.get(base_url, params=params)

    # Return the edit token
    return response.json()["query"]["tokens"]["csrftoken"]


def create_wiki_article(name: str, content: str, summary: Optional[str] = None, language: str = "simple") -> Dict[str, Any]:
    # Define the base URL for the Wikipedia API
    base_url = "https://" + language + ".wikipedia.org/w/api.php"

    session = requests.Session()

    # Set the parameters for the API request
    data = {
        "action": "edit",
        "title": name,
        "text": content,
        "summary": summary,
        "format": "json",
        # You need to implement get_edit_token to retrieve the edit token
        "token": get_edit_token(language, session),
    }

    # Make the API request
    response = session.post(base_url, data=data)

    # Return the response as a JSON object
    return response.json()


def publish(name: str, article: str) -> None:
    # Check that it doesn't already exist
    wiki = wikipediaapi.Wikipedia(language="simple")
    if wiki.page(name).exists():
        # Ask the user if they want to overwrite it
        if not typer.confirm("This article already exists. Do you want to overwrite it?"):
            return

    # Create the article
    response = create_wiki_article(name, article)

    typer.echo(json.dumps(response, indent=4))
