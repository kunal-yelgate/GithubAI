from pathlib import PurePosixPath


def _module_candidates(import_name: str, source_file: str):
    if not import_name.startswith("."):
        return []

    base = PurePosixPath(source_file).parent
    relative = import_name.lstrip(".").replace(".", "/")
    if import_name.startswith(".."):
        base = base.parent
    target = str(base / relative).replace("\\", "/").lstrip("./")
    return [
        target,
        *[f"{target}.{extension}" for extension in ("py", "js", "jsx", "ts", "tsx")],
        f"{target}/index.js",
        f"{target}/index.ts",
        f"{target}/__init__.py"
    ]


def _build_module_graph(source_analysis: list[dict]):
    known_files = {item["file"] for item in source_analysis}
    graph = []
    for item in source_analysis:
        for import_name in item.get("imports", []):
            target = next(
                (candidate for candidate in _module_candidates(import_name, item["file"])
                 if candidate in known_files),
                None
            )
            if target:
                graph.append({"from": item["file"], "to": target, "import": import_name})
    return graph[:100]


def analyze_architecture(
    files: list[str],
    technologies: list[str],
    source_analysis: list[dict] | None = None
):
    lower_files = [path.lower() for path in files]
    lower_technologies = {technology.lower() for technology in technologies}
    layers = []

    for layer, markers in {
        "Routes": ("routes/", "route", "api/"),
        "Services": ("services/", "service"),
        "Analyzers": ("analyzers/", "analyzer"),
        "Components": ("components/", "component", ".jsx", ".tsx"),
        "Models": ("models/", "model"),
        "Authentication": ("auth", "oauth", "login")
    }.items():
        if any(marker in path for path in lower_files for marker in markers):
            layers.append(layer)

    has_frontend = bool({"react", "vue", "angular", "next.js"} & lower_technologies) or any(
        "/src/" in path and path.endswith((".jsx", ".tsx")) for path in lower_files
    )
    has_backend = bool({"fastapi", "flask", "django", "python", "node.js"} & lower_technologies)

    if has_frontend and has_backend:
        architecture_type = "Frontend + Backend"
    elif has_frontend:
        architecture_type = "Frontend"
    elif has_backend:
        architecture_type = "Backend"
    else:
        architecture_type = "Unclassified"

    source_analysis = source_analysis or []
    module_graph = _build_module_graph(source_analysis)
    entry_points = [
        path for path in files
        if PurePosixPath(path).name.lower() in {
            "main.py", "app.py", "server.py", "index.js", "main.jsx", "main.tsx"
        }
    ]

    return {
        "architecture_type": architecture_type,
        "frontend": next((name for name in ("React", "Vue", "Angular", "Next.js") if name.lower() in lower_technologies), None),
        "backend": next((name for name in ("FastAPI", "Flask", "Django", "Node.js") if name.lower() in lower_technologies), None),
        "external_services": ["GitHub API"] if any("github" in path for path in lower_files) else [],
        "layers": layers,
        "entry_points": entry_points,
        "module_graph": module_graph,
        "module_relationships": len(module_graph),
        "analyzed_source_files": len(source_analysis),
        "analysis_note": (
            "Architecture is inferred from repository paths, detected technologies, "
            "and imports in the analyzed source files."
        )
    }