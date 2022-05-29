from transliterate import translit


async def translit_text(text: str) -> str:
	return translit(text, "ru", reversed=True)
