import os
structure = {
    "backend": [
        "app.py",
        "scheduler.py",
        "models.py"
    ],
    "frontend": {
        "": ["package.json"],
        "src": ["App.jsx"],
        "public": ["index.html"]
    }
}

def create_dirs_and_files(base_path, struct):
    for name, content in struct.items():
        dir_path = os.path.join(base_path, name) if name else base_path
        if isinstance(content, list):
            os.makedirs(dir_path, exist_ok=True)
            for filename in content:
                file_path = os.path.join(dir_path, filename)
                if not os.path.exists(file_path):
                    open(file_path, 'w').close()
        elif isinstance(content, dict):
            os.makedirs(dir_path, exist_ok=True)
            create_dirs_and_files(dir_path, content)

base = os.getcwd()  
create_dirs_and_files(base, structure)
print("Directory structure created successfully.")