import { Field } from "../ui/Field";
import type { ItensContratacao } from "../../types";

interface Props {
  value: ItensContratacao;
  onChange: (next: ItensContratacao) => void;
}

const TIPO_NATUREZA_OPCOES = ["INVESTIMENTOS", "CUSTEIO"];
const TIPO_SUBITEM_OPCOES = ["Material", "Serviço"];

export function Step2ItensContratacao({ value, onChange }: Props) {
  const set = <K extends keyof ItensContratacao>(key: K, val: ItensContratacao[K]) =>
    onChange({ ...value, [key]: val });

  return (
    <div className="step-section">
      <h3 className="step-subtitle">Natureza de Despesa Detalhada</h3>
      <div className="step-grid">
        <Field label="Ação" required>
          <input value={value.acao} onChange={(e) => set("acao", e.target.value)} />
        </Field>
        <Field label="Plano Orçamentário" required>
          <input value={value.plano_orcamentario} onChange={(e) => set("plano_orcamentario", e.target.value)} />
        </Field>
        <Field label="Tipo" required>
          <select value={value.tipo_natureza} onChange={(e) => set("tipo_natureza", e.target.value)}>
            {TIPO_NATUREZA_OPCOES.map((op) => (
              <option key={op} value={op}>
                {op}
              </option>
            ))}
          </select>
        </Field>
        <Field label="Descrição (Natureza)" required hint="ex: 4.4.50.41.07">
          <input value={value.natureza_descricao} onChange={(e) => set("natureza_descricao", e.target.value)} />
        </Field>
      </div>

      <h3 className="step-subtitle">Subitem</h3>
      <div className="step-grid">
        <Field label="Status da Contratação (Subitem)" required>
          <input value={value.status_subitem} onChange={(e) => set("status_subitem", e.target.value)} />
        </Field>
        <Field label="Tipo de Subitem" required>
          <select value={value.tipo_subitem} onChange={(e) => set("tipo_subitem", e.target.value)}>
            {TIPO_SUBITEM_OPCOES.map((op) => (
              <option key={op} value={op}>
                {op}
              </option>
            ))}
          </select>
        </Field>
        <Field label="Código do Subitem" required hint="Grupo/Classe/PDM são preenchidos automaticamente pelo SISCORP">
          <input value={value.codigo_subitem} onChange={(e) => set("codigo_subitem", e.target.value)} />
        </Field>
        <Field label="Descrição do Subitem" required>
          <input value={value.descricao_subitem} onChange={(e) => set("descricao_subitem", e.target.value)} />
        </Field>
        <Field label="Unidade de Medida" required>
          <input value={value.unidade_medida} onChange={(e) => set("unidade_medida", e.target.value)} />
        </Field>
        <Field label="Preço Unitário" required>
          <input value={value.preco_unitario} onChange={(e) => set("preco_unitario", e.target.value)} inputMode="decimal" />
        </Field>
        <Field label="Quantidade" required>
          <input value={value.quantidade} onChange={(e) => set("quantidade", e.target.value)} inputMode="numeric" />
        </Field>
      </div>
    </div>
  );
}
