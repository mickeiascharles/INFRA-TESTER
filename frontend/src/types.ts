export interface Credenciais {
  usuario: string;
  senha: string;
}

export interface DadosBasicos {
  status_contratacao: string;
  evento: string;
  ano_pca: string;
  area_demandante: string;
  descricao_objeto: string;
  justificativa: string;
}

export interface ItensContratacao {
  acao: string;
  plano_orcamentario: string;
  tipo_natureza: string;
  natureza_descricao: string;
  status_subitem: string;
  tipo_subitem: string;
  codigo_subitem: string;
  descricao_subitem: string;
  unidade_medida: string;
  preco_unitario: string;
  quantidade: string;
}

export interface DadosContratacao {
  tipo_licitacao: string;
  data_assinatura: string;
  data_entrega_doc: string;
  objetivo_estrategico: string;
  prioridade: string;
  sigiloso: string;
}

export interface PrevisaoDuracao {
  vigencia_meses: string;
}

export interface PrevisaoDesembolso {
  tipo_desembolso: string;
  parcela_anual: string;
  valor_parcela_unica?: string;
  ano_desembolso: string;
  mes_desembolso: string;
  valor_mensal_desembolso: string;
}

export interface DemandaPCA {
  credenciais: Credenciais;
  dados_basicos: DadosBasicos;
  itens_contratacao: ItensContratacao;
  dados_contratacao: DadosContratacao;
  previsao_duracao: PrevisaoDuracao;
  previsao_desembolso: PrevisaoDesembolso;
  navegador: string;
  headless: boolean;
}

export type ExecutionStatus = "pending" | "running" | "success" | "failed";

export interface ExecutionOut {
  id: number;
  status: ExecutionStatus;
  descricao_objeto: string;
  area_demandante: string;
  ano_pca: string;
  usuario: string;
  log_tail: string;
  error_message: string;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
}
