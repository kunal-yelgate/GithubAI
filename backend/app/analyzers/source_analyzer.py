import ast
import re


def _analyze_python(content: str):
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return {"imports": [], "classes": [], "functions": [], "routes": []}

    imports = []
    classes = []
    functions = []
    routes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr in {"get", "post", "put", "patch", "delete"} and decorator.args:
                        route = decorator.args[0]
                        if isinstance(route, ast.Constant) and isinstance(route.value, str):
                            routes.append(route.value)

    return {
        "imports": sorted(set(imports)),
        "classes": sorted(set(classes)),
        "functions": sorted(set(functions)),
        "routes": sorted(set(routes))
    }


def _analyze_javascript(content: str):
    imports = re.findall(r"(?:import .*? from\s+|require\()['\"]([^'\"]+)", content)
    exports = re.findall(r"export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)", content)
    functions = re.findall(r"(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)", content)
    function_names = [name for pair in functions for name in pair if name]
    components = [name for name in function_names if name[:1].isupper()]

    return {
        "imports": sorted(set(imports)),
        "exports": sorted(set(exports)),
        "functions": sorted(set(function_names)),
        "components": sorted(set(components))
    }


def analyze_source_file(path: str, content: str):
    suffix = path.rsplit(".", 1)[-1].lower() if "." in path else ""
    if suffix == "py":
        language = "Python"
        details = _analyze_python(content)
    elif suffix in {"js", "jsx", "ts", "tsx"}:
        language = "JavaScript" if suffix in {"js", "jsx"} else "TypeScript"
        details = _analyze_javascript(content)
    else:
        return None

    return {"file": path, "language": language, **details}


def analyze_source_files(files: dict[str, str]):
    return [
        analysis for path, content in files.items()
        if (analysis := analyze_source_file(path, content)) is not None
    ]