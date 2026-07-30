from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from . import db
from .execucao_atual_widget import ExecucaoAtualWidget
from .execucoes_widget import ExecucoesWidget
from .login_widget import LoginWidget
from .models import Credenciais
from .robot_runner import RobotRunnerThread
from .wizard.nova_demanda_widget import NovaDemandaWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SISCORP PCA — Automação de Cadastro")
        self.resize(1080, 760)

        db.inicializar()
        self._threads: dict[int, RobotRunnerThread] = {}

        self.pilha_raiz = QStackedWidget()
        self.setCentralWidget(self.pilha_raiz)

        self.tela_login = LoginWidget()
        self.tela_login.autenticado.connect(self._autenticado)
        self.pilha_raiz.addWidget(self.tela_login)

        self.pilha_raiz.addWidget(self._montar_app())

    def _montar_app(self) -> QWidget:
        central = QWidget()
        raiz = QHBoxLayout(central)
        raiz.setContentsMargins(0, 0, 0, 0)
        raiz.setSpacing(0)

        raiz.addWidget(self._criar_barra_lateral())

        self.pilha = QStackedWidget()
        self.pagina_nova_demanda = NovaDemandaWidget()
        self.pagina_execucao_atual = ExecucaoAtualWidget()
        self.pagina_execucoes = ExecucoesWidget()
        self.pilha.addWidget(self.pagina_nova_demanda)
        self.pilha.addWidget(self.pagina_execucao_atual)
        self.pilha.addWidget(self.pagina_execucoes)
        raiz.addWidget(self.pilha, stretch=1)

        self.pagina_nova_demanda.execucao_iniciada.connect(self._execucao_iniciada)
        self.pagina_execucao_atual.nova_execucao_solicitada.connect(lambda: self._navegar(0))

        return central

    def _criar_barra_lateral(self) -> QWidget:
        barra = QFrame()
        barra.setObjectName("barra-lateral")
        barra.setFixedWidth(220)
        layout = QVBoxLayout(barra)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        marca = QLabel("  SISCORP PCA")
        marca.setObjectName("marca")
        marca.setFixedHeight(60)
        layout.addWidget(marca)

        self.botao_nova = QPushButton("Nova Demanda")
        self.botao_nova.setObjectName("nav-botao")
        self.botao_nova.setCheckable(True)
        self.botao_nova.setChecked(True)
        self.botao_nova.clicked.connect(lambda: self._navegar(0))
        layout.addWidget(self.botao_nova)

        self.botao_execucoes = QPushButton("Execuções")
        self.botao_execucoes.setObjectName("nav-botao")
        self.botao_execucoes.setCheckable(True)
        self.botao_execucoes.clicked.connect(lambda: self._navegar(2))
        layout.addWidget(self.botao_execucoes)

        layout.addStretch(1)

        self.botao_sair = QPushButton("Sair")
        self.botao_sair.setObjectName("nav-botao-sair")
        self.botao_sair.clicked.connect(self._encerrar_sessao)
        layout.addWidget(self.botao_sair)

        rodape = QLabel("Automação via\nRobot Framework")
        rodape.setObjectName("rodape-lateral")
        layout.addWidget(rodape)

        return barra

    def _navegar(self, indice: int) -> None:
        self.pilha.setCurrentIndex(indice)
        self.botao_nova.setChecked(indice == 0)
        self.botao_execucoes.setChecked(indice == 2)
        if indice == 2:
            self.pagina_execucoes.atualizar()

    def _autenticado(self, usuario: str, senha: str, headless: bool) -> None:
        self.pagina_nova_demanda.definir_sessao(Credenciais(usuario=usuario, senha=senha), headless)
        self.pilha_raiz.setCurrentIndex(1)
        self._navegar(0)

    def _encerrar_sessao(self) -> None:
        for thread in self._threads.values():
            thread.cancelar()
        self._threads.clear()
        self.tela_login.usuario.clear()
        self.tela_login.senha.clear()
        self.pagina_nova_demanda.definir_sessao(Credenciais(), False)
        self.pagina_nova_demanda.resetar()
        self.pilha_raiz.setCurrentIndex(0)

    def _execucao_iniciada(self, execucao_id: int, thread: RobotRunnerThread) -> None:
        self._threads[execucao_id] = thread
        thread.finalizado.connect(lambda eid, status, erro: self._execucao_finalizada(eid))
        self.pagina_execucao_atual.iniciar(execucao_id, thread)
        self.pilha.setCurrentIndex(1)
        self.botao_nova.setChecked(False)
        self.botao_execucoes.setChecked(False)

    def _execucao_finalizada(self, execucao_id: int) -> None:
        self._threads.pop(execucao_id, None)

    def closeEvent(self, event) -> None:  # noqa: N802 (Qt override)
        for thread in self._threads.values():
            thread.cancelar()
        super().closeEvent(event)
