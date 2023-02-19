import re
from pprint import pp

import openai
import transformers
import wikitextparser


def get_prompt(title: str, article: str) -> str:
    return (
        f"Help a non-native English speaker understand this Wikipedia article on \"{title}\" by translating it into Simple English. "
        "Use a small vocabulary, the active voice, and simple sentences. "
        "Do not assume prior knowledge for complex topics and explain technical jargon when it is introduced. "
        "Don't leave out the details, and avoid oversimplifying. "
        "Please use wikitext and copy over any relevant wikilinks from the original.\n\n"
        # "I am a 16 year-old student, and I am trying to understand complex math with my limited knowledge. "
        # f"Currently, I'm trying to understand \"{title}\". "
        # "I will give you part of the Wikipedia page, and you will help me break it down, translate it to Simple English, and reword the text so that I can understand. "
        # "Also, I want the details. Please don't drop anything from the text I give you.\n\n"
        f"BEGIN\n{article}\nEND"
    )


def _simplify(title: str, article: str) -> str:
    print(f"\n\n{get_prompt(title, article)}\n\n")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=get_prompt(title, article),
        temperature=0.6,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text


def math_tag_to_latex(article: str) -> str:
    # """Converts <math> and <math display="block"> tags to LaTeX delimiters"""
    # Convert display="block" tags to double-dollar signs
    article = re.sub(r'<math\s+display="block">(.+?)</math>',
                     r'$$\1$$', article)
    # Convert all other math tags to single-dollar signs
    article = re.sub(r'<math>(.+?)</math>', r'$\1$', article)
    return article


def latex_to_math_tag(article: str) -> str:
    # """Converts LaTeX delimiters to <math> and <math display="block"> tags"""
    # Convert double-dollar signs to display="block" tags
    article = re.sub(r'\$\$(.+?)\$\$',
                     r'<math display="block">\1</math>', article)
    # Convert single-dollar signs to math tags
    article = re.sub(r'\$(.+?)\$', r'<math>\1</math>', article)
    return article


def simplify(title: str, article: str) -> str:
    article = math_tag_to_latex(article)
    sections = wikitextparser.parse(article).sections[:1]

    pp(sections)
    simplified_sections = [_simplify(title, section.contents.strip())
                           for section in sections]

    return "\n".join([latex_to_math_tag(section) for section in simplified_sections])
