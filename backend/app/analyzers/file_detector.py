from pathlib import PurePosixPath


ENTRY_POINT_NAMES = {
    "main.py", "app.py", "manage.py", "server.py", "index.js", "main.js",
    "server.js", "app.js", "main.jsx", "main.tsx", "App.jsx", "App.tsx",
    "Application.java", "Main.java"
}

CONFIG_FILE_NAMES = {
    "requirements.txt", "pyproject.toml", "Pipfile", "package.json",
    "pom.xml", "build.gradle", "Cargo.toml", "go.mod", "Dockerfile",
    "docker-compose.yml", "docker-compose.yaml", ".env.example", "README.md"
}

SOURCE_EXTENSIONS = {"py", "js", "jsx", "ts", "tsx"}
MAX_ANALYSIS_FILES = 40


def detect_important_files(files: list[str]):
    entry_points = []
    config_files = []
    source_files = []

    for path in files:
        name = PurePosixPath(path).name
        if name in ENTRY_POINT_NAMES:
            entry_points.append(path)
        if name in CONFIG_FILE_NAMES or name.startswith("config."):
            config_files.append(path)
        if PurePosixPath(path).suffix.lower().lstrip(".") in SOURCE_EXTENSIONS:
            source_files.append(path)

    analysis_files = list(dict.fromkeys(entry_points + config_files + source_files))
    return {
        "entry_points": entry_points,
        "config_files": config_files,
        "source_files": source_files,
        "important_files": analysis_files[:MAX_ANALYSIS_FILES],
        "total_candidates": len(analysis_files)
    }