import os

PROJECT_STRUCTURE = {
    "app": {
        "__init__.py": "",
        "extensions.py": "",
        "logger.py": "",
        "main": {
            "__init__.py": "",
            "routes.py": "",
            "schemas.py": "",
        },
        "rag": {
            "__init__.py": "",
            "pipeline.py": "",
            "loaders.py": "",
            "retriever.py": "",
            "generator.py": "",
        },
        "models": {
            "__init__.py": "",
            "db_models.py": "",
        },
        "static": {},
        "templates": {},
    },
    "ml": {
        "experiments": {},
        "indexing": {
            "build_index.py": "",
        },
        "evaluation": {},
    },
    "configs": {
        "base.yaml": "",
        "dev.yaml": "",
        "prod.yaml": "",
    },
    "logs": {
        "app.log": "",
        "rag.log": "",
    },
    "scripts": {
        "run_dev.sh": "",
        "run_prod.sh": "",
    },
    "tests": {
        "test_rag.py": "",
    },
    "Dockerfile": "",
    "docker-compose.yml": "",
    ".env": "",
    "requirements.txt": "",
    "README.md": "",
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    if name.endswith(".py"):
                        f.write(
                            f'"""\n{name}\nAuto-generated file.\n"""\n\n'
                        )
            else:
                print(f"Skipping existing file: {path}")


if __name__ == "__main__":
    root_dir = os.getcwd()
    print(f"Creating project structure in: {root_dir}")
    create_structure(root_dir, PROJECT_STRUCTURE)
    print("✅ Project structure created successfully.")
