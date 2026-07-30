import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { StepIndicator } from "../components/ui/StepIndicator";
import { Field } from "../components/ui/Field";
import { Step1DadosBasicos } from "../components/steps/Step1DadosBasicos";
import { Step2ItensContratacao } from "../components/steps/Step2ItensContratacao";
import { Step3DadosContratacao } from "../components/steps/Step3DadosContratacao";
import { Step4PrevisaoDuracao } from "../components/steps/Step4PrevisaoDuracao";
import { Step5PrevisaoDesembolso } from "../components/steps/Step5PrevisaoDesembolso";
import { api } from "../api";
import type { DemandaPCA } from "../types";

const STEP_LABELS = [
  "Dados Básicos",
  "Itens de Contratação",
  "Dados da Contratação",
  "Previsão de Duração",
  "Previsão de Desembolso",
  "Revisão e Envio",
];

const DEFAULT_DEMANDA: DemandaPCA = {
  credenciais: { usuario: "", senha: "" },
  dados_basicos: {
    status_contratacao: "EM PLANEJAMENTO",
    evento: "",
    ano_pca: String(new Date().getFullYear() + 1),
    area_demandante: "",
    descricao_objeto: "",
    justificativa: "",
  },
  itens_contratacao: {
    acao: "",
    plano_orcamentario: "",
    tipo_natureza: "INVESTIMENTOS",
    natureza_descricao: "",
    status_subitem: "EM PLANEJAMENTO",
    tipo_subitem: "Material",
    codigo_subitem: "",
    descricao_subitem: "",
    unidade_medida: "",
    preco_unitario: "",
    quantidade: "",
  },
  dados_contratacao: {
    tipo_licitacao: "PREGÃO ELETRÔNICO",
    data_assinatura: "",
    data_entrega_doc: "",
    objetivo_estrategico: "",
    prioridade: "BAIXA",
    sigiloso: "Não",
  },
  previsao_duracao: { vigencia_meses: "" },
  previsao_desembolso: {
    tipo_desembolso: "Misto",
    parcela_anual: "Sim",
    valor_parcela_unica: "",
    ano_desembolso: String(new Date().getFullYear() + 1),
    mes_desembolso: "Janeiro",
    valor_mensal_desembolso: "",
  },
  navegador: "Chrome",
  headless: true,
};

export function NovaDemanda() {
  const [step, setStep] = useState(0);
  const [demanda, setDemanda] = useState<DemandaPCA>(DEFAULT_DEMANDA);
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const navigate = useNavigate();

  const irPara = (index: number) => setStep(Math.max(0, Math.min(STEP_LABELS.length - 1, index)));

  async function enviar() {
    setErro(null);
    if (!demanda.credenciais.usuario || !demanda.credenciais.senha) {
      setErro("Informe usuário e senha do SISCORP para o robô conseguir logar.");
      return;
    }
    setEnviando(true);
    try {
      const execucao = await api.criarExecucao(demanda);
      navigate(`/execucoes/${execucao.id}`);
    } catch (e) {
      setErro(e instanceof Error ? e.message : "Falha ao iniciar o cadastro.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <div className="page">
      <h1 className="page-title">Nova Demanda no PCA</h1>
      <p className="page-subtitle">
        Preencha os dados abaixo. Ao enviar, um robô fará o cadastro automaticamente no SISCORP.
      </p>

      <StepIndicator steps={STEP_LABELS} current={step} onSelect={irPara} />

      <div className="card">
        {step === 0 && (
          <Step1DadosBasicos
            value={demanda.dados_basicos}
            onChange={(dados_basicos) => setDemanda({ ...demanda, dados_basicos })}
          />
        )}
        {step === 1 && (
          <Step2ItensContratacao
            value={demanda.itens_contratacao}
            onChange={(itens_contratacao) => setDemanda({ ...demanda, itens_contratacao })}
          />
        )}
        {step === 2 && (
          <Step3DadosContratacao
            value={demanda.dados_contratacao}
            onChange={(dados_contratacao) => setDemanda({ ...demanda, dados_contratacao })}
          />
        )}
        {step === 3 && (
          <Step4PrevisaoDuracao
            value={demanda.previsao_duracao}
            onChange={(previsao_duracao) => setDemanda({ ...demanda, previsao_duracao })}
          />
        )}
        {step === 4 && (
          <Step5PrevisaoDesembolso
            value={demanda.previsao_desembolso}
            onChange={(previsao_desembolso) => setDemanda({ ...demanda, previsao_desembolso })}
          />
        )}
        {step === 5 && (
          <div className="step-section">
            <h3 className="step-subtitle">Credenciais do SISCORP</h3>
            <p className="field-hint">
              Usadas apenas para esta execução do robô — não são armazenadas.
            </p>
            <div className="step-grid">
              <Field label="Usuário" required>
                <input
                  value={demanda.credenciais.usuario}
                  onChange={(e) =>
                    setDemanda({ ...demanda, credenciais: { ...demanda.credenciais, usuario: e.target.value } })
                  }
                />
              </Field>
              <Field label="Senha" required>
                <input
                  type="password"
                  value={demanda.credenciais.senha}
                  onChange={(e) =>
                    setDemanda({ ...demanda, credenciais: { ...demanda.credenciais, senha: e.target.value } })
                  }
                />
              </Field>
              <Field label="Executar em modo headless (sem abrir janela do navegador)">
                <input
                  type="checkbox"
                  checked={demanda.headless}
                  onChange={(e) => setDemanda({ ...demanda, headless: e.target.checked })}
                />
              </Field>
            </div>

            <h3 className="step-subtitle">Resumo</h3>
            <pre className="review-json">{JSON.stringify(
              { ...demanda, credenciais: { usuario: demanda.credenciais.usuario, senha: "••••••" } },
              null,
              2
            )}</pre>

            {erro && <p className="alert-error">{erro}</p>}
          </div>
        )}
      </div>

      <div className="wizard-actions">
        <button className="btn btn-secondary" onClick={() => irPara(step - 1)} disabled={step === 0 || enviando}>
          Voltar
        </button>
        {step < STEP_LABELS.length - 1 ? (
          <button className="btn btn-primary" onClick={() => irPara(step + 1)}>
            Avançar
          </button>
        ) : (
          <button className="btn btn-primary" onClick={enviar} disabled={enviando}>
            {enviando ? "Enviando..." : "Cadastrar no SISCORP"}
          </button>
        )}
      </div>
    </div>
  );
}
