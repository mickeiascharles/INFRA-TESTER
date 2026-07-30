import sys

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow
from app.styles import STYLESHEET


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    app.setApplicationName("SISCORP PCA")

    janela = MainWindow()
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
