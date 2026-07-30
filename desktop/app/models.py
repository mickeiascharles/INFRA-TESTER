from dataclasses import dataclass, field


@dataclass
class Credenciais:
    usuario: str = ""
    senha: str = ""


@dataclass
class DadosBasicos:
    status_contratacao: str = "EM PLANEJAMENTO"
    evento: str = ""
    ano_pca: str = ""
    area_demandante: str = ""
    descricao_objeto: str = ""
    justificativa: str = ""


@dataclass
class ItensContratacao:
    acao: str = ""
    plano_orcamentario: str = ""
    tipo_natureza: str = "INVESTIMENTOS"
    natureza_descricao: str = ""
    status_subitem: str = "EM PLANEJAMENTO"
    tipo_subitem: str = "Material"
    codigo_subitem: str = ""
    descricao_subitem: str = ""
    unidade_medida: str = ""
    preco_unitario: str = ""
    quantidade: str = ""


@dataclass
class DadosContratacao:
    tipo_licitacao: str = "PREGÃO ELETRÔNICO"
    data_assinatura: str = ""
    data_entrega_doc: str = ""
    objetivo_estrategico: str = ""
    prioridade: str = "BAIXA"
    sigiloso: str = "Não"


@dataclass
class PrevisaoDuracao:
    vigencia_meses: str = ""


@dataclass
class PrevisaoDesembolso:
    tipo_desembolso: str = "Misto"
    parcela_anual: str = "Sim"
    valor_parcela_unica: str = ""
    ano_desembolso: str = ""
    mes_desembolso: str = "Janeiro"
    valor_mensal_desembolso: str = ""


@dataclass
class DemandaPCA:
    credenciais: Credenciais = field(default_factory=Credenciais)
    dados_basicos: DadosBasicos = field(default_factory=DadosBasicos)
    itens_contratacao: ItensContratacao = field(default_factory=ItensContratacao)
    dados_contratacao: DadosContratacao = field(default_factory=DadosContratacao)
    previsao_duracao: PrevisaoDuracao = field(default_factory=PrevisaoDuracao)
    previsao_desembolso: PrevisaoDesembolso = field(default_factory=PrevisaoDesembolso)
    navegador: str = "Chrome"
    headless: bool = False

    def variaveis_robot(self) -> dict[str, str]:
        db, ic, dc = self.dados_basicos, self.itens_contratacao, self.dados_contratacao
        pd, pdb = self.previsao_duracao, self.previsao_desembolso

        variaveis = {
            "NAVEGADOR": "headlesschrome" if self.headless else self.navegador,
            "USUARIO": self.credenciais.usuario,
            "STATUS_CONTRATACAO": db.status_contratacao,
            "EVENTO": db.evento,
            "ANO_PCA": db.ano_pca,
            "AREA_DEMANDANTE": db.area_demandante,
            "DESCRICAO_OBJETO": db.descricao_objeto,
            "JUSTIFICATIVA": db.justificativa,
            "ACAO": ic.acao,
            "PLANO_ORCAMENTARIO": ic.plano_orcamentario,
            "TIPO_NATUREZA": ic.tipo_natureza,
            "NATUREZA_DESCRICAO": ic.natureza_descricao,
            "STATUS_SUBITEM": ic.status_subitem,
            "TIPO_SUBITEM": ic.tipo_subitem,
            "CODIGO_SUBITEM": ic.codigo_subitem,
            "DESCRICAO_SUBITEM": ic.descricao_subitem,
            "UNIDADE_MEDIDA": ic.unidade_medida,
            "PRECO_UNITARIO": ic.preco_unitario,
            "QUANTIDADE": ic.quantidade,
            "TIPO_LICITACAO": dc.tipo_licitacao,
            "DATA_ASSINATURA": dc.data_assinatura,
            "DATA_ENTREGA_DOC": dc.data_entrega_doc,
            "OBJETIVO_ESTRATEGICO": dc.objetivo_estrategico,
            "PRIORIDADE": dc.prioridade,
            "SIGILOSO": dc.sigiloso,
            "VIGENCIA_MESES": pd.vigencia_meses,
            "TIPO_DESEMBOLSO": pdb.tipo_desembolso,
            "PARCELA_ANUAL": pdb.parcela_anual,
            "ANO_DESEMBOLSO": pdb.ano_desembolso,
            "MES_DESEMBOLSO": pdb.mes_desembolso,
            "VALOR_MENSAL_DESEMBOLSO": pdb.valor_mensal_desembolso,
        }
        if pdb.valor_parcela_unica:
            variaveis["VALOR_PARCELA_UNICA"] = pdb.valor_parcela_unica
        return variaveis

    def campos_obrigatorios_faltando(self) -> list[str]:
        obrigatorios = {
            "Usuário": self.credenciais.usuario,
            "Senha": self.credenciais.senha,
            "Evento": self.dados_basicos.evento,
            "Ano": self.dados_basicos.ano_pca,
            "Área Demandante": self.dados_basicos.area_demandante,
            "Descrição do Objeto": self.dados_basicos.descricao_objeto,
            "Justificativa": self.dados_basicos.justificativa,
            "Ação": self.itens_contratacao.acao,
            "Plano Orçamentário": self.itens_contratacao.plano_orcamentario,
            "Descrição (Natureza)": self.itens_contratacao.natureza_descricao,
            "Código do Subitem": self.itens_contratacao.codigo_subitem,
            "Descrição do Subitem": self.itens_contratacao.descricao_subitem,
            "Unidade de Medida": self.itens_contratacao.unidade_medida,
            "Preço Unitário": self.itens_contratacao.preco_unitario,
            "Quantidade": self.itens_contratacao.quantidade,
            "Tipo de Licitação": self.dados_contratacao.tipo_licitacao,
            "Data de Assinatura": self.dados_contratacao.data_assinatura,
            "Data de Entrega": self.dados_contratacao.data_entrega_doc,
            "Objetivo Estratégico": self.dados_contratacao.objetivo_estrategico,
            "Vigência Contratual": self.previsao_duracao.vigencia_meses,
            "Ano do Desembolso": self.previsao_desembolso.ano_desembolso,
            "Valor Mensal de Desembolso": self.previsao_desembolso.valor_mensal_desembolso,
        }
        return [nome for nome, valor in obrigatorios.items() if not str(valor).strip()]
