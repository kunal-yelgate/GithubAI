import re


SECTION_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


def analyze_readme(content: str | None):
    if not content:
        return {
            "exists": False,
            "length": 0,
            "sections": [],
            "has_installation": False,
            "has_usage": False,
            "has_features": False,
            "technologies_mentioned": []
        }

    sections = SECTION_PATTERN.findall(content)
    normalized = content.lower()
    technology_names = (
        "Python", "JavaScript", "TypeScript", "React", "FastAPI",
        "Flask", "Django", "Node.js", "PostgreSQL", "MongoDB",
        "Docker", "Redis", "Vue", "Angular", "Next.js"
    )

    return {
        "exists": True,
        "length": len(content),
        "sections": sections,
        "has_installation": bool(re.search(r"install|setup|getting started", normalized)),
        "has_usage": bool(re.search(r"usage|how to use|run the", normalized)),
        "has_features": bool(re.search(r"feature|capabilit", normalized)),
        "technologies_mentioned": [
            name for name in technology_names if name.lower() in normalized
        ]
    }