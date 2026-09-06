def analyze_architecture(files: list[str], technologies: list[str]):
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

    return {
        "architecture_type": architecture_type,
        "frontend": next((name for name in ("React", "Vue", "Angular", "Next.js") if name.lower() in lower_technologies), None),
        "backend": next((name for name in ("FastAPI", "Flask", "Django", "Node.js") if name.lower() in lower_technologies), None),
        "external_services": ["GitHub API"] if any("github" in path for path in lower_files) else [],
        "layers": layers
    }