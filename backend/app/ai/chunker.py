from pathlib import PurePosixPath


SUPPORTED_EXTENSIONS = {"py", "js", "jsx", "ts", "tsx", "json", "md", "toml", "txt"}


def chunk_file(path: str, content: str, max_chars: int = 3500):
    extension = PurePosixPath(path).suffix.lower().lstrip(".")
    if extension not in SUPPORTED_EXTENSIONS:
        return []

    lines = content.splitlines()
    chunks = []
    current = []
    current_length = 0
    for line in lines:
        if current and current_length + len(line) + 1 > max_chars:
            chunks.append("\n".join(current))
            current = []
            current_length = 0
        current.append(line)
        current_length += len(line) + 1
    if current:
        chunks.append("\n".join(current))

    return [{
        "file": path,
        "language": extension,
        "chunk_index": index,
        "content": value
    } for index, value in enumerate(chunks)]