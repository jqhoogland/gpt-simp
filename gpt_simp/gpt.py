import openai


def simplify(article: str) -> str:
    response = openai.Completion.create(
        engine="davinci",
        prompt=article,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    return response.choices[0].text
