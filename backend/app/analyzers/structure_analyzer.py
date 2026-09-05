def analyze_structure(tree_data: dict):

    tree = tree_data.get("tree", [])

    files = []
    directories = []

    for item in tree:

        if item["type"] == "blob":
            files.append(item["path"])

        elif item["type"] == "tree":
            directories.append(item["path"])

    extensions = {}

    for file in files:

        if "." in file:

            extension = file.rsplit(".", 1)[1].lower()

            extensions[extension] = (
                extensions.get(extension, 0) + 1
            )

    return {
        "total_files": len(files),
        "total_directories": len(directories),
        "files": files,
        "directories": directories,
        "file_extensions": extensions
    }