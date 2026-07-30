from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROBOT_FILE = (BASE_DIR.parent / "robot" / "cadastrar_pca.robot").resolve()
RUNS_DIR = (BASE_DIR / "runs").resolve()
DB_PATH = (BASE_DIR / "executions.db").resolve()

RUNS_DIR.mkdir(parents=True, exist_ok=True)
