import sys
from pathlib import Path

FROZEN = getattr(sys, "frozen", False)

if FROZEN:
    # Executável empacotado: dados graváveis (banco, logs) ficam ao lado do
    # binário, não dentro do bundle temporário do PyInstaller (que pode ser
    # somente leitura e é apagado a cada execução no modo --onefile).
    BASE_DIR = Path(sys.executable).resolve().parent
    BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))
    ROBOT_FILE = (BUNDLE_DIR / "robot" / "cadastrar_pca.robot").resolve()
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    ROBOT_FILE = (BASE_DIR.parent / "robot" / "cadastrar_pca.robot").resolve()

RUNS_DIR = (BASE_DIR / "runs").resolve()
DB_PATH = (BASE_DIR / "execucoes.db").resolve()

RUNS_DIR.mkdir(parents=True, exist_ok=True)
