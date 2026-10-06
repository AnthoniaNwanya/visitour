import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
VENV_PYTHON = BASE_DIR / ".venv" / "bin" / "python"

subprocess.run(
    [
        str(VENV_PYTHON),
        "-m",
        "uvicorn",
        "main:app",
        "--reload",
        "--port",
        "8003",
    ],
    cwd=BASE_DIR / "src",
)
