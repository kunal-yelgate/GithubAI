def analyze_languages(language_data: dict):

    if not language_data:
        return {
            "languages": {},
            "primary_language": None
        }

    total_bytes = sum(language_data.values())

    languages = {}

    for language, bytes_count in language_data.items():

        percentage = (
            bytes_count / total_bytes
        ) * 100

        languages[language] = round(
            percentage,
            2
        )

    primary_language = max(
        languages,
        key=languages.get
    )

    return {
        "languages": languages,
        "primary_language": primary_language
    }