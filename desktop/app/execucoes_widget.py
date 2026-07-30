from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from . import db, robot_runner

STATUS_LABELS = {
    "pending": "Pendente",
    "running": "Em execução",
    "success": "Sucesso",
    "failed": "Falhou",
}


class ExecucoesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._execucao_selecionada: int | None = None

        raiz = QVBoxLayout(self)

        titulo = QLabel("Execuções")
        titulo.setObjectName("titulo-pagina")
        raiz.addWidget(titulo)

        subtitulo = QLabel("Histórico de cadastros de demanda disparados no SISCORP.")
        subtitulo.setObjectName("subtitulo-pagina")
        raiz.addWidget(subtitulo)

        splitter = QSplitter(Qt.Orientation.Vertical)

        self.tabela = QTableWidget(0, 6)
        self.tabela.setHorizontalHeaderLabels(
            ["#", "Status", "Descrição do Objeto", "Área", "Ano", "Usuário"]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabela.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela.itemSelectionChanged.connect(self._selecionou_linha)
        splitter.addWidget(self.tabela)

        painel_detalhe = QFrame()
        painel_detalhe.setObjectName("cartao")
        detalhe_layout = QVBoxLayout(painel_detalhe)

        cabecalho_detalhe = QHBoxLayout()
        self.label_detalhe = QLabel("Selecione uma execução")
        self.label_detalhe.setObjectName("subtitulo")
        cabecalho_detalhe.addWidget(self.label_detalhe)
        cabecalho_detalhe.addStretch(1)

        self.botao_relatorio = QPushButton("Abrir Relatório")
        self.botao_relatorio.setObjectName("botao-secundario")
        self.botao_relatorio.clicked.connect(lambda: self._abrir_artefato("report.html"))
        self.botao_relatorio.setEnabled(False)
        cabecalho_detalhe.addWidget(self.botao_relatorio)

        self.botao_log = QPushButton("Abrir Log Detalhado")
        self.botao_log.setObjectName("botao-secundario")
        self.botao_log.clicked.connect(lambda: self._abrir_artefato("log.html"))
        self.botao_log.setEnabled(False)
        cabecalho_detalhe.addWidget(self.botao_log)

        detalhe_layout.addLayout(cabecalho_detalhe)

        self.console = QPlainTextEdit()
        self.console.setObjectName("console")
        self.console.setReadOnly(True)
        detalhe_layout.addWidget(self.console)

        splitter.addWidget(painel_detalhe)
        splitter.setSizes([220, 380])

        raiz.addWidget(splitter, stretch=1)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.atualizar)
        self._timer.start(3000)
        self.atualizar()

    def atualizar(self) -> None:
        execucoes = db.listar_execucoes()
        linha_selecionada_id = self._execucao_selecionada

        self.tabela.blockSignals(True)
        self.tabela.setRowCount(len(execucoes))
        for linha, execucao in enumerate(execucoes):
            self.tabela.setItem(linha, 0, QTableWidgetItem(str(execucao.id)))
            item_status = QTableWidgetItem(STATUS_LABELS.get(execucao.status, execucao.status))
            self.tabela.setItem(linha, 1, item_status)
            self.tabela.setItem(linha, 2, QTableWidgetItem(execucao.descricao_objeto))
            self.tabela.setItem(linha, 3, QTableWidgetItem(execucao.area_demandante))
            self.tabela.setItem(linha, 4, QTableWidgetItem(execucao.ano_pca))
            self.tabela.setItem(linha, 5, QTableWidgetItem(execucao.usuario))
            if execucao.id == linha_selecionada_id:
                self.tabela.selectRow(linha)
        self.tabela.blockSignals(False)

        if linha_selecionada_id is not None:
            self._mostrar_detalhe(linha_selecionada_id)

    def selecionar_execucao(self, execucao_id: int) -> None:
        self._execucao_selecionada = execucao_id
        self.atualizar()

    def _selecionou_linha(self) -> None:
        linhas = self.tabela.selectionModel().selectedRows()
        if not linhas:
            return
        execucao_id = int(self.tabela.item(linhas[0].row(), 0).text())
        self._execucao_selecionada = execucao_id
        self._mostrar_detalhe(execucao_id)

    def _mostrar_detalhe(self, execucao_id: int) -> None:
        execucao = db.obter_execucao(execucao_id)
        if not execucao:
            return
        self.label_detalhe.setText(
            f"Execução #{execucao.id} — {STATUS_LABELS.get(execucao.status, execucao.status)}"
        )
        finalizado = execucao.status in ("success", "failed")
        self.botao_relatorio.setEnabled(finalizado and robot_runner.caminho_artefato(execucao_id, "report.html") is not None)
        self.botao_log.setEnabled(finalizado and robot_runner.caminho_artefato(execucao_id, "log.html") is not None)

        if finalizado:
            texto = execucao.log_tail or robot_runner.caminho_console(execucao_id)
            if execucao.error_message:
                texto = f"[ERRO] {execucao.error_message}\n\n{texto}"
        else:
            texto = robot_runner.caminho_console(execucao_id) or "Aguardando início do robô..."

        if self.console.toPlainText() != texto:
            self.console.setPlainText(texto)
            barra = self.console.verticalScrollBar()
            barra.setValue(barra.maximum())

    def anexar_linha_ao_vivo(self, execucao_id: int, linha: str) -> None:
        if execucao_id != self._execucao_selecionada:
            return
        self.console.appendPlainText(linha)

    def _abrir_artefato(self, nome_arquivo: str) -> None:
        if self._execucao_selecionada is None:
            return
        caminho = robot_runner.caminho_artefato(self._execucao_selecionada, nome_arquivo)
        if caminho:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(caminho)))
