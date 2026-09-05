import json


def analyze_package_json(content: str):

    data = json.loads(content)

    dependencies = {}

    dependencies.update(
        data.get("dependencies", {})
    )

    dependencies.update(
        data.get("devDependencies", {})
    )

    technologies = set()

    for dependency in dependencies:

        technology = FRAMEWORK_DEPENDENCIES.get(
            dependency.lower()
        )

        if technology:
            technologies.add(technology)

    return {
        "dependencies": dependencies,
        "technologies": sorted(technologies)
    }

TECHNOLOGY_FILES = {

    "package.json": ["Node.js"],

    "requirements.txt": ["Python"],

    "pyproject.toml": ["Python"],

    "Pipfile": ["Python"],

    "pom.xml": ["Java", "Maven"],

    "build.gradle": ["Java", "Gradle"],

    "Cargo.toml": ["Rust"],

    "go.mod": ["Go"],

    "composer.json": ["PHP"],

    "Gemfile": ["Ruby"],

    "Dockerfile": ["Docker"],

    "docker-compose.yml": ["Docker"],

    "docker-compose.yaml": ["Docker"],

    "next.config.js": ["Next.js"],

    "next.config.mjs": ["Next.js"],

    "vite.config.js": ["Vite"],

    "vite.config.ts": ["Vite"]
}


def detect_technologies(files: list[str]):

    technologies = set()

    file_names = {
        file.split("/")[-1]
        for file in files
    }

    for file_name, techs in TECHNOLOGY_FILES.items():

        if file_name in file_names:

            technologies.update(techs)

    return sorted(technologies)

def analyze_requirements(content: str):

    dependencies = []
    technologies = set()

    for line in content.splitlines():

        line = line.strip()

        if not line or line.startswith("#"):
            continue

        package = line.split(
            "=="
        )[0].split(
            ">="
        )[0].split(
            "<="
        )[0].strip()

        dependencies.append(package)

        technology = FRAMEWORK_DEPENDENCIES.get(
            package.lower()
        )

        if technology:
            technologies.add(technology)

    return {
        "dependencies": dependencies,
        "technologies": sorted(technologies)
    }