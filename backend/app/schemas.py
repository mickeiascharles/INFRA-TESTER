import datetime as dt

from pydantic import BaseModel, Field


class Credenciais(BaseModel):
    usuario: str
    senha: str = Field(..., min_length=1)


class DadosBasicos(BaseModel):
    status_contratacao: str = "EM PLANEJAMENTO"
    evento: str
    ano_pca: str
    area_demandante: str
    descricao_objeto: str
    justificativa: str


class ItensContratacao(BaseModel):
    acao: str
    plano_orcamentario: str
    tipo_natureza: str
    natureza_descricao: str
    status_subitem: str = "EM PLANEJAMENTO"
    tipo_subitem: str
    codigo_subitem: str
    descricao_subitem: str
    unidade_medida: str
    preco_unitario: str
    quantidade: str


class DadosContratacao(BaseModel):
    tipo_licitacao: str
    data_assinatura: str
    data_entrega_doc: str
    objetivo_estrategico: str
    prioridade: str
    sigiloso: str = "Não"


class PrevisaoDuracao(BaseModel):
    vigencia_meses: str


class PrevisaoDesembolso(BaseModel):
    tipo_desembolso: str
    parcela_anual: str
    valor_parcela_unica: str | None = None
    ano_desembolso: str
    mes_desembolso: str
    valor_mensal_desembolso: str


class DemandaPCA(BaseModel):
    credenciais: Credenciais
    dados_basicos: DadosBasicos
    itens_contratacao: ItensContratacao
    dados_contratacao: DadosContratacao
    previsao_duracao: PrevisaoDuracao
    previsao_desembolso: PrevisaoDesembolso
    navegador: str = "Chrome"
    headless: bool = True


class ExecutionOut(BaseModel):
    id: int
    status: str
    descricao_objeto: str
    area_demandante: str
    ano_pca: str
    usuario: str
    log_tail: str
    error_message: str
    created_at: dt.datetime
    started_at: dt.datetime | None
    finished_at: dt.datetime | None

    class Config:
        from_attributes = True
