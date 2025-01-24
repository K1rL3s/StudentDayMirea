def format_answer(answer: str) -> set[str]:
    return set(answer.casefold().translate(str.maketrans("ё,.", "е  ")).split())
