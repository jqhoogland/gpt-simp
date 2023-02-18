import wikipediaapi


def get_wiki_article(name: str) -> str:
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page_py = wiki_wiki.page(name)
    return page_py.text


def publish(name: str, article: str) -> None:
    page = wikipediaapi.Wikipedia('simple').page(name)
    page.text = article
    page.save("Simplified by GPT-3 (and checked by a human).")

