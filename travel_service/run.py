import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
VENV_PYTHON = BASE_DIR / ".venv" / "bin" / "python"

try:
    subprocess.run(
        [
            str(VENV_PYTHON),
            "-m",
            "uvicorn",
            "main:app",
            "--reload",
            "--port",
            "8002",
        ],
        cwd=BASE_DIR / "src",
    )
except KeyboardInterrupt:
    print("\nTravel service stopped.")