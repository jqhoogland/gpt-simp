import os

import openai
import typer
from dotenv import load_dotenv

from gpt_simp.gpt import simplify
from gpt_simp.wiki import get_wiki_article, publish

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def edit(article: str) -> str:
    # Write to a txt file, let the user edit the text, then read it back once the user accepts.
    with open("article.txt", "w") as f:
        f.write(article)

    typer.launch("article.txt")
    typer.confirm("Do you want to publish this article?", abort=True)

    with open("article.txt", "r") as f:
        return f.read()


def main(name: str):
    article = get_wiki_article(name)
    typer.echo(article)

    simple_article = simplify(name, article)
    edited_article = edit(simple_article)

    publish(name, edited_article)


if __name__ == "__main__":
    typer.run(main)
