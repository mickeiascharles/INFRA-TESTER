from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginWidget(QWidget):
    autenticado = Signal(str, str, bool)  # usuario, senha, headless

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("tela-login")

        raiz = QVBoxLayout(self)
        raiz.addStretch(1)

        linha_central = QHBoxLayout()
        linha_central.addStretch(1)

        cartao = QFrame()
        cartao.setObjectName("cartao-login")
        cartao.setFixedWidth(380)
        cartao_layout = QVBoxLayout(cartao)
        cartao_layout.setContentsMargins(28, 28, 28, 28)
        cartao_layout.setSpacing(10)

        cabecalho = QHBoxLayout()
        marca = QFrame()
        marca.setObjectName("marca-login")
        cabecalho.addWidget(marca)

        textos_marca = QVBoxLayout()
        textos_marca.setSpacing(0)
        titulo = QLabel("SISCORP PCA")
        titulo.setObjectName("marca-login-titulo")
        subtitulo = QLabel("RobotFramework · Selenium")
        subtitulo.setObjectName("marca-login-subtitulo")
        textos_marca.addWidget(titulo)
        textos_marca.addWidget(subtitulo)
        cabecalho.addLayout(textos_marca)
        cabecalho.addStretch(1)
        cartao_layout.addLayout(cabecalho)

        descricao = QLabel("Seus dados de acesso INFRA S.A")
        descricao.setObjectName("login-descricao")
        cartao_layout.addWidget(descricao)

        cartao_layout.addWidget(QLabel("Usuário"))
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("nome.nome@infrasa.gov.br")
        cartao_layout.addWidget(self.usuario)

        cartao_layout.addWidget(QLabel("Senha"))
        self.senha = QLineEdit()
        self.senha.setEchoMode(QLineEdit.EchoMode.Password)
        cartao_layout.addWidget(self.senha)

        self.headless = QCheckBox("Executar sem abrir a janela do navegador (headless)")
        cartao_layout.addWidget(self.headless)

        self.alerta = QLabel("")
        self.alerta.setObjectName("alerta-erro")
        self.alerta.setWordWrap(True)
        self.alerta.hide()
        cartao_layout.addWidget(self.alerta)

        self.botao_entrar = QPushButton("Entrar")
        self.botao_entrar.setObjectName("botao-primario")
        self.botao_entrar.clicked.connect(self._entrar)
        cartao_layout.addWidget(self.botao_entrar)

        rodape = QLabel("⚑ pré-requisito: Chrome/Chromium instalado")
        rodape.setObjectName("login-rodape")
        cartao_layout.addWidget(rodape)

        self.senha.returnPressed.connect(self._entrar)

        linha_central.addWidget(cartao)
        linha_central.addStretch(1)
        raiz.addLayout(linha_central)
        raiz.addStretch(1)

    def _entrar(self) -> None:
        usuario = self.usuario.text().strip()
        senha = self.senha.text()
        if not usuario or not senha:
            self.alerta.setText("Preencha usuário e senha.")
            self.alerta.show()
            return
        self.alerta.hide()
        self.autenticado.emit(usuario, senha, self.headless.isChecked())
