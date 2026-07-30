from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import QDate

from ..models import (
    DadosBasicos,
    DadosContratacao,
    ItensContratacao,
    PrevisaoDesembolso,
    PrevisaoDuracao,
)


def _required_label(texto: str) -> str:
    return f"{texto} *"


def _br_date_to_qdate(valor: str) -> QDate:
    try:
        dia, mes, ano = valor.split("/")
        return QDate(int(ano), int(mes), int(dia))
    except (ValueError, AttributeError):
        return QDate.currentDate()


class Step1DadosBasicos(QWidget):
    def __init__(self, dados: DadosBasicos, parent=None):
        super().__init__(parent)
        self.dados = dados
        layout = QFormLayout(self)
        layout.setSpacing(12)

        self.status = QComboBox()
        self.status.addItems(["EM PLANEJAMENTO", "EM CONTRATAÇÃO", "CONTRATADO", "CANCELADO"])
        self.status.setCurrentText(dados.status_contratacao)
        self.status.currentTextChanged.connect(lambda v: setattr(dados, "status_contratacao", v))
        layout.addRow(_required_label("Status da Contratação"), self.status)

        self.evento = QLineEdit(dados.evento)
        self.evento.textChanged.connect(lambda v: setattr(dados, "evento", v))
        layout.addRow(_required_label("Evento"), self.evento)

        self.ano = QLineEdit(dados.ano_pca)
        self.ano.textChanged.connect(lambda v: setattr(dados, "ano_pca", v))
        layout.addRow(_required_label("Ano"), self.ano)

        self.area = QLineEdit(dados.area_demandante)
        self.area.textChanged.connect(lambda v: setattr(dados, "area_demandante", v.upper()))
        layout.addRow(_required_label("Área Demandante"), self.area)

        self.descricao = QPlainTextEdit(dados.descricao_objeto)
        self.descricao.setFixedHeight(70)
        self.descricao.textChanged.connect(lambda: setattr(dados, "descricao_objeto", self.descricao.toPlainText()))
        layout.addRow(_required_label("Descrição do Objeto"), self.descricao)

        self.justificativa = QPlainTextEdit(dados.justificativa)
        self.justificativa.setFixedHeight(70)
        self.justificativa.textChanged.connect(lambda: setattr(dados, "justificativa", self.justificativa.toPlainText()))
        layout.addRow(_required_label("Justificativa da Contratação"), self.justificativa)

        layout.addRow("", _hint_mono("→ EVENTO · ANO_PCA · AREA_DEMANDANTE · DESCRICAO_OBJETO · JUSTIFICATIVA"))


class Step2ItensContratacao(QWidget):
    def __init__(self, dados: ItensContratacao, parent=None):
        super().__init__(parent)
        self.dados = dados
        raiz = QVBoxLayout(self)

        raiz.addWidget(_subtitulo("Natureza de Despesa Detalhada"))
        form1 = QFormLayout()
        form1.setSpacing(12)

        self.acao = QLineEdit(dados.acao)
        self.acao.textChanged.connect(lambda v: setattr(dados, "acao", v))
        form1.addRow(_required_label("Ação"), self.acao)

        self.plano = QLineEdit(dados.plano_orcamentario)
        self.plano.textChanged.connect(lambda v: setattr(dados, "plano_orcamentario", v))
        form1.addRow(_required_label("Plano Orçamentário"), self.plano)

        self.tipo_natureza = QComboBox()
        self.tipo_natureza.addItems(["INVESTIMENTOS", "CUSTEIO"])
        self.tipo_natureza.setCurrentText(dados.tipo_natureza)
        self.tipo_natureza.currentTextChanged.connect(lambda v: setattr(dados, "tipo_natureza", v))
        form1.addRow(_required_label("Tipo"), self.tipo_natureza)

        self.natureza_descricao = QLineEdit(dados.natureza_descricao)
        self.natureza_descricao.setPlaceholderText("ex: 4.4.50.41.07")
        self.natureza_descricao.textChanged.connect(lambda v: setattr(dados, "natureza_descricao", v))
        form1.addRow(_required_label("Descrição (Natureza)"), self.natureza_descricao)
        raiz.addLayout(form1)

        raiz.addWidget(_subtitulo("Subitem"))
        form2 = QFormLayout()
        form2.setSpacing(12)

        self.status_subitem = QLineEdit(dados.status_subitem)
        self.status_subitem.textChanged.connect(lambda v: setattr(dados, "status_subitem", v))
        form2.addRow(_required_label("Status da Contratação (Subitem)"), self.status_subitem)

        self.tipo_subitem = QComboBox()
        self.tipo_subitem.addItems(["Material", "Serviço"])
        self.tipo_subitem.setCurrentText(dados.tipo_subitem)
        self.tipo_subitem.currentTextChanged.connect(lambda v: setattr(dados, "tipo_subitem", v))
        form2.addRow(_required_label("Tipo de Subitem"), self.tipo_subitem)

        self.codigo_subitem = QLineEdit(dados.codigo_subitem)
        self.codigo_subitem.textChanged.connect(lambda v: setattr(dados, "codigo_subitem", v))
        form2.addRow(_required_label("Código do Subitem"), self.codigo_subitem)
        form2.addRow("", _hint("Grupo/Classe/PDM são preenchidos automaticamente pelo SISCORP"))

        self.descricao_subitem = QLineEdit(dados.descricao_subitem)
        self.descricao_subitem.textChanged.connect(lambda v: setattr(dados, "descricao_subitem", v))
        form2.addRow(_required_label("Descrição do Subitem"), self.descricao_subitem)

        self.unidade_medida = QLineEdit(dados.unidade_medida)
        self.unidade_medida.textChanged.connect(lambda v: setattr(dados, "unidade_medida", v))
        form2.addRow(_required_label("Unidade de Medida"), self.unidade_medida)

        self.preco_unitario = QLineEdit(dados.preco_unitario)
        self.preco_unitario.textChanged.connect(lambda v: setattr(dados, "preco_unitario", v))
        form2.addRow(_required_label("Preço Unitário"), self.preco_unitario)

        self.quantidade = QLineEdit(dados.quantidade)
        self.quantidade.textChanged.connect(lambda v: setattr(dados, "quantidade", v))
        form2.addRow(_required_label("Quantidade"), self.quantidade)
        raiz.addLayout(form2)
        raiz.addWidget(
            _hint_mono(
                "→ ACAO · PLANO_ORCAMENTARIO · TIPO_NATUREZA · NATUREZA_DESCRICAO · STATUS_SUBITEM · "
                "TIPO_SUBITEM · CODIGO_SUBITEM · DESCRICAO_SUBITEM · UNIDADE_MEDIDA · PRECO_UNITARIO · QUANTIDADE"
            )
        )
        raiz.addStretch(1)


class Step3DadosContratacao(QWidget):
    def __init__(self, dados: DadosContratacao, parent=None):
        super().__init__(parent)
        self.dados = dados
        layout = QFormLayout(self)
        layout.setSpacing(12)

        self.tipo_licitacao = QComboBox()
        self.tipo_licitacao.addItems(
            ["PREGÃO ELETRÔNICO", "CONCORRÊNCIA", "DISPENSA", "INEXIGIBILIDADE"]
        )
        self.tipo_licitacao.setCurrentText(dados.tipo_licitacao)
        self.tipo_licitacao.currentTextChanged.connect(lambda v: setattr(dados, "tipo_licitacao", v))
        layout.addRow(_required_label("Tipo de Licitação"), self.tipo_licitacao)

        self.data_assinatura = QDateEdit(_br_date_to_qdate(dados.data_assinatura))
        self.data_assinatura.setCalendarPopup(True)
        self.data_assinatura.setDisplayFormat("dd/MM/yyyy")
        self.data_assinatura.dateChanged.connect(
            lambda d: setattr(dados, "data_assinatura", d.toString("dd/MM/yyyy"))
        )
        dados.data_assinatura = self.data_assinatura.date().toString("dd/MM/yyyy")
        layout.addRow(_required_label("Data estimada de Assinatura"), self.data_assinatura)

        self.data_entrega = QDateEdit(_br_date_to_qdate(dados.data_entrega_doc))
        self.data_entrega.setCalendarPopup(True)
        self.data_entrega.setDisplayFormat("dd/MM/yyyy")
        self.data_entrega.dateChanged.connect(
            lambda d: setattr(dados, "data_entrega_doc", d.toString("dd/MM/yyyy"))
        )
        dados.data_entrega_doc = self.data_entrega.date().toString("dd/MM/yyyy")
        layout.addRow(_required_label("Data estimada de Entrega"), self.data_entrega)

        self.objetivo_estrategico = QLineEdit(dados.objetivo_estrategico)
        self.objetivo_estrategico.setPlaceholderText("ex: 1.3")
        self.objetivo_estrategico.textChanged.connect(lambda v: setattr(dados, "objetivo_estrategico", v))
        layout.addRow(_required_label("Objetivo Estratégico"), self.objetivo_estrategico)

        self.prioridade = QComboBox()
        self.prioridade.addItems(["BAIXA", "MÉDIA", "ALTA"])
        self.prioridade.setCurrentText(dados.prioridade)
        self.prioridade.currentTextChanged.connect(lambda v: setattr(dados, "prioridade", v))
        layout.addRow(_required_label("Prioridade"), self.prioridade)

        self.sigiloso = QComboBox()
        self.sigiloso.addItems(["Não", "Sim"])
        self.sigiloso.setCurrentText(dados.sigiloso)
        self.sigiloso.currentTextChanged.connect(lambda v: setattr(dados, "sigiloso", v))
        layout.addRow(_required_label("Sigiloso"), self.sigiloso)

        layout.addRow(
            "",
            _hint_mono(
                "→ TIPO_LICITACAO · DATA_ASSINATURA · DATA_ENTREGA_DOC · OBJETIVO_ESTRATEGICO · PRIORIDADE · SIGILOSO"
            ),
        )


class Step4PrevisaoDuracao(QWidget):
    def __init__(self, dados: PrevisaoDuracao, parent=None):
        super().__init__(parent)
        self.dados = dados
        layout = QFormLayout(self)
        layout.setSpacing(12)

        self.vigencia = QLineEdit(dados.vigencia_meses)
        self.vigencia.textChanged.connect(lambda v: setattr(dados, "vigencia_meses", v))
        layout.addRow(_required_label("Vigência Contratual (meses)"), self.vigencia)

        layout.addRow("", _hint_mono("→ VIGENCIA_MESES"))


class Step5PrevisaoDesembolso(QWidget):
    def __init__(self, dados: PrevisaoDesembolso, parent=None):
        super().__init__(parent)
        self.dados = dados
        layout = QFormLayout(self)
        layout.setSpacing(12)

        self.tipo_desembolso = QComboBox()
        self.tipo_desembolso.addItems(["Único", "Mensal", "Misto"])
        self.tipo_desembolso.setCurrentText(dados.tipo_desembolso)
        self.tipo_desembolso.currentTextChanged.connect(lambda v: setattr(dados, "tipo_desembolso", v))
        layout.addRow(_required_label("Tipo de Desembolso"), self.tipo_desembolso)

        self.parcela_anual = QComboBox()
        self.parcela_anual.addItems(["Sim", "Não"])
        self.parcela_anual.setCurrentText(dados.parcela_anual)
        self.parcela_anual.currentTextChanged.connect(lambda v: setattr(dados, "parcela_anual", v))
        layout.addRow(_required_label("Parcela Anual"), self.parcela_anual)

        self.valor_parcela_unica = QLineEdit(dados.valor_parcela_unica)
        self.valor_parcela_unica.textChanged.connect(lambda v: setattr(dados, "valor_parcela_unica", v))
        layout.addRow("Valor da Parcela Única", self.valor_parcela_unica)
        layout.addRow("", _hint("Opcional, se aplicável"))

        self.ano_desembolso = QLineEdit(dados.ano_desembolso)
        self.ano_desembolso.textChanged.connect(lambda v: setattr(dados, "ano_desembolso", v))
        layout.addRow(_required_label("Ano do Desembolso Mensal"), self.ano_desembolso)

        self.mes_desembolso = QComboBox()
        self.mes_desembolso.addItems(
            ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        )
        self.mes_desembolso.setCurrentText(dados.mes_desembolso)
        self.mes_desembolso.currentTextChanged.connect(lambda v: setattr(dados, "mes_desembolso", v))
        layout.addRow(_required_label("Mês do Desembolso Mensal"), self.mes_desembolso)

        self.valor_mensal = QLineEdit(dados.valor_mensal_desembolso)
        self.valor_mensal.textChanged.connect(lambda v: setattr(dados, "valor_mensal_desembolso", v))
        layout.addRow(_required_label("Valor Mensal de Desembolso"), self.valor_mensal)

        layout.addRow(
            "",
            _hint_mono(
                "→ TIPO_DESEMBOLSO · PARCELA_ANUAL · VALOR_PARCELA_UNICA · ANO_DESEMBOLSO · "
                "MES_DESEMBOLSO · VALOR_MENSAL_DESEMBOLSO"
            ),
        )


class Step6Revisao(QWidget):
    def __init__(self, demanda, parent=None):
        super().__init__(parent)
        self.demanda = demanda
        raiz = QVBoxLayout(self)

        self.sessao = _hint(f"Sessão ativa: {demanda.credenciais.usuario}")
        raiz.addWidget(self.sessao)

        raiz.addWidget(_subtitulo("Comando que será enviado ao RobotFramework"))
        self.resumo = QPlainTextEdit()
        self.resumo.setReadOnly(True)
        self.resumo.setFixedHeight(220)
        raiz.addWidget(self.resumo)

        self.alerta = QLabel("")
        self.alerta.setObjectName("alerta-erro")
        self.alerta.setWordWrap(True)
        self.alerta.hide()
        raiz.addWidget(self.alerta)
        raiz.addStretch(1)

    def atualizar_resumo(self) -> None:
        self.sessao.setText(f"Sessão ativa: {self.demanda.credenciais.usuario}")
        variaveis = self.demanda.variaveis_robot()
        linhas = [f"{chave}: {valor}" for chave, valor in variaveis.items()]
        self.resumo.setPlainText("\n".join(linhas))

    def mostrar_erro(self, mensagem: str) -> None:
        if mensagem:
            self.alerta.setText(mensagem)
            self.alerta.show()
        else:
            self.alerta.hide()


def _subtitulo(texto: str) -> QLabel:
    label = QLabel(texto.upper())
    label.setObjectName("subtitulo")
    return label


def _hint(texto: str) -> QLabel:
    label = QLabel(texto)
    label.setObjectName("dica")
    label.setWordWrap(True)
    return label


def _hint_mono(texto: str) -> QLabel:
    label = QLabel(texto)
    label.setObjectName("dica-mono")
    label.setWordWrap(True)
    return label
