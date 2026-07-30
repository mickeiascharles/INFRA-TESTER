from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .. import db
from ..models import Credenciais, DemandaPCA
from ..robot_runner import RobotRunnerThread
from .steps import (
    Step1DadosBasicos,
    Step2ItensContratacao,
    Step3DadosContratacao,
    Step4PrevisaoDuracao,
    Step5PrevisaoDesembolso,
    Step6Revisao,
)

# (slug de breadcrumb, título, subtítulo) de cada passo do wizard
STEP_META = [
    ("dados-basicos", "Dados Básicos", "Informações gerais da contratação a ser cadastrada no PCA."),
    ("itens-contratacao", "Itens de Contratação", "Natureza de despesa detalhada e subitem do PCA."),
    ("dados-contratacao", "Dados da Contratação", "Licitação, datas estimadas e prioridade."),
    ("previsao-duracao", "Previsão de Duração", "Vigência contratual estimada, em meses."),
    ("previsao-desembolso", "Previsão de Desembolso", "Como o valor será desembolsado ao longo do contrato."),
    ("revisao", "Revisão e Execução", "Confira os dados antes de enviar ao robô."),
]


class NovaDemandaWidget(QWidget):
    execucao_iniciada = Signal(int, object)  # execucao_id, RobotRunnerThread

    def __init__(self, parent=None):
        super().__init__(parent)
        self.demanda = DemandaPCA()
        self._thread: RobotRunnerThread | None = None

        raiz = QVBoxLayout(self)

        self.breadcrumb = QLabel("")
        self.breadcrumb.setObjectName("breadcrumb")
        raiz.addWidget(self.breadcrumb)

        linha_titulo = QHBoxLayout()
        self.titulo = QLabel("")
        self.titulo.setObjectName("titulo-pagina")
        linha_titulo.addWidget(self.titulo)
        self.badge_passo = QLabel("")
        self.badge_passo.setObjectName("passo-badge")
        linha_titulo.addWidget(self.badge_passo)
        linha_titulo.addStretch(1)
        raiz.addLayout(linha_titulo)

        self.subtitulo = QLabel("")
        self.subtitulo.setObjectName("subtitulo-pagina")
        self.subtitulo.setWordWrap(True)
        raiz.addWidget(self.subtitulo)

        cartao = QFrame()
        cartao.setObjectName("cartao")
        cartao_layout = QVBoxLayout(cartao)

        self.step1 = Step1DadosBasicos(self.demanda.dados_basicos)
        self.step2 = Step2ItensContratacao(self.demanda.itens_contratacao)
        self.step3 = Step3DadosContratacao(self.demanda.dados_contratacao)
        self.step4 = Step4PrevisaoDuracao(self.demanda.previsao_duracao)
        self.step5 = Step5PrevisaoDesembolso(self.demanda.previsao_desembolso)
        self.step6 = Step6Revisao(self.demanda)

        self.pilha = QStackedWidget()
        for etapa in (self.step1, self.step2, self.step3, self.step4, self.step5, self.step6):
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(etapa)
            scroll.setFrameShape(QFrame.Shape.NoFrame)
            self.pilha.addWidget(scroll)

        cartao_layout.addWidget(self.pilha)
        raiz.addWidget(cartao, stretch=1)

        acoes = QHBoxLayout()
        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.setObjectName("botao-secundario")
        self.botao_voltar.clicked.connect(self._voltar)
        acoes.addWidget(self.botao_voltar)
        acoes.addStretch(1)
        self.botao_avancar = QPushButton("Avançar")
        self.botao_avancar.setObjectName("botao-primario")
        self.botao_avancar.clicked.connect(self._avancar)
        acoes.addWidget(self.botao_avancar)
        raiz.addLayout(acoes)

        self._ir_para(0)

    def definir_sessao(self, credenciais: Credenciais, headless: bool) -> None:
        self.demanda.credenciais = credenciais
        self.demanda.headless = headless

    def _voltar(self) -> None:
        self._ir_para(self.pilha.currentIndex() - 1)

    def _avancar(self) -> None:
        indice_atual = self.pilha.currentIndex()
        if indice_atual < len(STEP_META) - 1:
            self._ir_para(indice_atual + 1)
        else:
            self._enviar()

    def _ir_para(self, indice: int) -> None:
        indice = max(0, min(len(STEP_META) - 1, indice))
        self.pilha.setCurrentIndex(indice)

        slug, titulo, subtitulo = STEP_META[indice]
        self.breadcrumb.setText(
            f"CONFIGURAÇÃO DA DEMANDA  /  <span style='color:#4c8dff'>{slug}</span>"
        )
        self.titulo.setText(titulo)
        self.subtitulo.setText(subtitulo)
        self.badge_passo.setText(f"passo {indice + 1}/{len(STEP_META)}")

        self.botao_voltar.setEnabled(indice > 0)
        ultimo = indice == len(STEP_META) - 1
        self.botao_avancar.setText("Executar no SISCORP" if ultimo else "Avançar")
        self.botao_avancar.setObjectName("botao-executar" if ultimo else "botao-primario")
        self.botao_avancar.style().unpolish(self.botao_avancar)
        self.botao_avancar.style().polish(self.botao_avancar)
        if ultimo:
            self.step6.atualizar_resumo()

    def _enviar(self) -> None:
        faltando = self.demanda.campos_obrigatorios_faltando()
        if faltando:
            self.step6.mostrar_erro("Preencha os campos obrigatórios: " + ", ".join(faltando))
            return
        self.step6.mostrar_erro("")

        execucao_id = db.criar_execucao(
            descricao_objeto=self.demanda.dados_basicos.descricao_objeto,
            area_demandante=self.demanda.dados_basicos.area_demandante,
            ano_pca=self.demanda.dados_basicos.ano_pca,
            usuario=self.demanda.credenciais.usuario,
            payload=self.demanda.variaveis_robot(),
        )

        thread = RobotRunnerThread(execucao_id, self.demanda)
        self._thread = thread
        self.execucao_iniciada.emit(execucao_id, thread)
        thread.start()

        self.resetar()

    def resetar(self) -> None:
        credenciais = self.demanda.credenciais
        headless = self.demanda.headless
        self.demanda = DemandaPCA(credenciais=credenciais, headless=headless)
        for widget in (self.step1, self.step2, self.step3, self.step4, self.step5, self.step6):
            widget.setParent(None)
        self.step1 = Step1DadosBasicos(self.demanda.dados_basicos)
        self.step2 = Step2ItensContratacao(self.demanda.itens_contratacao)
        self.step3 = Step3DadosContratacao(self.demanda.dados_contratacao)
        self.step4 = Step4PrevisaoDuracao(self.demanda.previsao_duracao)
        self.step5 = Step5PrevisaoDesembolso(self.demanda.previsao_desembolso)
        self.step6 = Step6Revisao(self.demanda)
        while self.pilha.count():
            self.pilha.removeWidget(self.pilha.widget(0))
        for etapa in (self.step1, self.step2, self.step3, self.step4, self.step5, self.step6):
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(etapa)
            scroll.setFrameShape(QFrame.Shape.NoFrame)
            self.pilha.addWidget(scroll)
        self._ir_para(0)
