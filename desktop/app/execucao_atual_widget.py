import datetime as dt

from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from . import db, robot_runner

STATUS_TITULO = {
    "sucesso": "✓ Cadastro concluído",
    "falha": "✕ Cadastro falhou",
    "executando": "◐ Executando no SISCORP...",
}


def _tile(valor: str, legenda: str) -> QFrame:
    caixa = QFrame()
    caixa.setObjectName("tile")
    layout = QVBoxLayout(caixa)
    layout.setContentsMargins(14, 10, 14, 10)
    label_valor = QLabel(valor)
    label_valor.setObjectName("tile-valor")
    label_legenda = QLabel(legenda)
    label_legenda.setObjectName("tile-legenda")
    layout.addWidget(label_valor)
    layout.addWidget(label_legenda)
    caixa.valor_label = label_valor
    return caixa


def _duracao_str(inicio: str | None, fim: str | None) -> str:
    if not inicio or not fim:
        return "—"
    try:
        segundos = int((dt.datetime.fromisoformat(fim) - dt.datetime.fromisoformat(inicio)).total_seconds())
    except ValueError:
        return "—"
    minutos, seg = divmod(max(segundos, 0), 60)
    return f"{minutos}m {seg:02d}s" if minutos else f"{seg}s"


class ExecucaoAtualWidget(QWidget):
    nova_execucao_solicitada = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._execucao_id: int | None = None

        raiz = QVBoxLayout(self)
        self.pilha = QStackedWidget()
        raiz.addWidget(self.pilha)

        self.pilha.addWidget(self._montar_pagina_executando())
        self.pilha.addWidget(self._montar_pagina_laudo())

    # ---------- página "executando" ----------

    def _montar_pagina_executando(self) -> QWidget:
        pagina = QWidget()
        layout = QVBoxLayout(pagina)

        breadcrumb = QLabel("EXECUÇÃO  /  <span style='color:#4c8dff'>em-andamento</span>")
        breadcrumb.setObjectName("breadcrumb")
        layout.addWidget(breadcrumb)

        titulo = QLabel("Executando no SISCORP")
        titulo.setObjectName("titulo-pagina")
        layout.addWidget(titulo)

        subtitulo = QLabel("Acompanhe abaixo o console do RobotFramework em tempo real.")
        subtitulo.setObjectName("subtitulo-pagina")
        layout.addWidget(subtitulo)

        cartao = QFrame()
        cartao.setObjectName("cartao")
        cartao_layout = QVBoxLayout(cartao)
        self.console = QPlainTextEdit()
        self.console.setObjectName("console")
        self.console.setReadOnly(True)
        cartao_layout.addWidget(self.console)
        layout.addWidget(cartao, stretch=1)

        return pagina

    # ---------- página "laudo" ----------

    def _montar_pagina_laudo(self) -> QWidget:
        pagina = QWidget()
        layout = QVBoxLayout(pagina)

        breadcrumb = QLabel("RELATÓRIO  /  <span style='color:#4c8dff'>laudo</span>")
        breadcrumb.setObjectName("breadcrumb")
        layout.addWidget(breadcrumb)

        titulo = QLabel("Laudo da Execução")
        titulo.setObjectName("titulo-pagina")
        layout.addWidget(titulo)

        self.badge = QFrame()
        self.badge.setObjectName("status-badge")
        badge_layout = QVBoxLayout(self.badge)
        self.badge_titulo = QLabel("")
        self.badge_titulo.setObjectName("status-badge-titulo")
        self.badge_subtitulo = QLabel("")
        self.badge_subtitulo.setObjectName("status-badge-subtitulo")
        badge_layout.addWidget(self.badge_titulo)
        badge_layout.addWidget(self.badge_subtitulo)
        layout.addWidget(self.badge)

        tiles = QHBoxLayout()
        self.tile_execucao = _tile("—", "execução #")
        self.tile_status = _tile("—", "status")
        self.tile_duracao = _tile("—", "duração")
        for tile in (self.tile_execucao, self.tile_status, self.tile_duracao):
            tiles.addWidget(tile)
        layout.addLayout(tiles)

        cartao = QFrame()
        cartao.setObjectName("cartao")
        cartao_layout = QVBoxLayout(cartao)

        subtitulo_artefatos = QLabel("ARTEFATOS GERADOS")
        subtitulo_artefatos.setObjectName("subtitulo")
        cartao_layout.addWidget(subtitulo_artefatos)

        linha_relatorio = QHBoxLayout()
        linha_relatorio.addWidget(self._label_artefato("report.html"))
        linha_relatorio.addStretch(1)
        self.botao_relatorio = QPushButton("Abrir Relatório")
        self.botao_relatorio.setObjectName("botao-secundario")
        self.botao_relatorio.clicked.connect(lambda: self._abrir_artefato("report.html"))
        linha_relatorio.addWidget(self.botao_relatorio)
        cartao_layout.addLayout(linha_relatorio)

        linha_log = QHBoxLayout()
        linha_log.addWidget(self._label_artefato("log.html"))
        linha_log.addStretch(1)
        self.botao_log = QPushButton("Abrir Log Detalhado")
        self.botao_log.setObjectName("botao-secundario")
        self.botao_log.clicked.connect(lambda: self._abrir_artefato("log.html"))
        linha_log.addWidget(self.botao_log)
        cartao_layout.addLayout(linha_log)

        self.erro_label = QLabel("")
        self.erro_label.setObjectName("alerta-erro")
        self.erro_label.setWordWrap(True)
        self.erro_label.hide()
        cartao_layout.addWidget(self.erro_label)

        layout.addWidget(cartao)
        layout.addStretch(1)

        acoes = QHBoxLayout()
        acoes.addStretch(1)
        self.botao_nova_execucao = QPushButton("Nova execução")
        self.botao_nova_execucao.setObjectName("botao-primario")
        self.botao_nova_execucao.clicked.connect(self.nova_execucao_solicitada.emit)
        acoes.addWidget(self.botao_nova_execucao)
        layout.addLayout(acoes)

        return pagina

    @staticmethod
    def _label_artefato(nome: str) -> QLabel:
        label = QLabel(nome)
        label.setObjectName("artefato-nome")
        return label

    # ---------- orquestração ----------

    def iniciar(self, execucao_id: int, thread) -> None:
        self._execucao_id = execucao_id
        self.console.clear()
        self.pilha.setCurrentIndex(0)
        thread.linha_recebida.connect(self._anexar_linha)
        thread.finalizado.connect(self._finalizar)

    def _anexar_linha(self, execucao_id: int, linha: str) -> None:
        if execucao_id != self._execucao_id:
            return
        self.console.appendPlainText(linha)

    def _finalizar(self, execucao_id: int, status: str, erro: str) -> None:
        if execucao_id != self._execucao_id:
            return

        execucao = db.obter_execucao(execucao_id)
        estado = "sucesso" if status == "success" else "falha"

        self.badge.setProperty("estado", estado)
        self.badge_titulo.setProperty("estado", estado)
        self.badge_titulo.setText(STATUS_TITULO[estado])
        for widget in (self.badge, self.badge_titulo):
            widget.style().unpolish(widget)
            widget.style().polish(widget)

        duracao = _duracao_str(execucao.started_at if execucao else None, execucao.finished_at if execucao else None)
        descricao = execucao.descricao_objeto if execucao else ""
        self.badge_subtitulo.setText(f"{descricao} · concluído em {duracao}" if descricao else f"concluído em {duracao}")

        self.tile_execucao.valor_label.setText(f"#{execucao_id}")
        self.tile_status.valor_label.setText("Sucesso" if estado == "sucesso" else "Falhou")
        self.tile_duracao.valor_label.setText(duracao)

        self.botao_relatorio.setEnabled(robot_runner.caminho_artefato(execucao_id, "report.html") is not None)
        self.botao_log.setEnabled(robot_runner.caminho_artefato(execucao_id, "log.html") is not None)

        if erro:
            self.erro_label.setText(erro)
            self.erro_label.show()
        else:
            self.erro_label.hide()

        self.pilha.setCurrentIndex(1)

    def _abrir_artefato(self, nome_arquivo: str) -> None:
        if self._execucao_id is None:
            return
        caminho = robot_runner.caminho_artefato(self._execucao_id, nome_arquivo)
        if caminho:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(caminho)))
