import ast
import subprocess
import sys
from pathlib import Path

ALLOWED_PACKAGES = {
    "requests"
}

FORBIDDEN_IMPORTS = {
    "os", "sys", "subprocess", "socket",
    "shutil", "pathlib", "threading"
}

TIMEOUT = 10  # saniye

def analyze_imports(file_path: Path):
    tree = ast.parse(file_path.read_text(encoding="utf-8"))
    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module.split(".")[0])

    return imports

def install_packages(pkgs):
    for pkg in pkgs:
        if pkg not in ALLOWED_PACKAGES:
            raise Exception(f"❌ Yasak paket: {pkg}")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", pkg
        ])

def run_py(file_path: Path):
    imports = analyze_imports(file_path)

    if imports & FORBIDDEN_IMPORTS:
        raise Exception("❌ Tehlikeli import tespit edildi")

    install_packages(imports)

    proc = subprocess.Popen(
        [sys.executable, file_path.name],
        cwd=file_path.parent
    )

    try:
        proc.wait(timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise Exception("⏱️ Script timeout ile durduruldu")
