import { Field } from "../ui/Field";
import type { DadosContratacao } from "../../types";

interface Props {
  value: DadosContratacao;
  onChange: (next: DadosContratacao) => void;
}

const TIPO_LICITACAO_OPCOES = [
  "PREGÃO ELETRÔNICO",
  "CONCORRÊNCIA",
  "DISPENSA",
  "INEXIGIBILIDADE",
];
const PRIORIDADE_OPCOES = ["BAIXA", "MÉDIA", "ALTA"];

function toInputDate(brDate: string): string {
  const [d, m, y] = brDate.split("/");
  if (!d || !m || !y) return "";
  return `${y}-${m.padStart(2, "0")}-${d.padStart(2, "0")}`;
}

function toBrDate(isoDate: string): string {
  const [y, m, d] = isoDate.split("-");
  if (!d || !m || !y) return "";
  return `${d}/${m}/${y}`;
}

export function Step3DadosContratacao({ value, onChange }: Props) {
  const set = <K extends keyof DadosContratacao>(key: K, val: DadosContratacao[K]) =>
    onChange({ ...value, [key]: val });

  return (
    <div className="step-grid">
      <Field label="Tipo de Licitação" required>
        <select value={value.tipo_licitacao} onChange={(e) => set("tipo_licitacao", e.target.value)}>
          {TIPO_LICITACAO_OPCOES.map((op) => (
            <option key={op} value={op}>
              {op}
            </option>
          ))}
        </select>
      </Field>

      <Field label="Data estimada de Assinatura" required>
        <input
          type="date"
          value={toInputDate(value.data_assinatura)}
          onChange={(e) => set("data_assinatura", toBrDate(e.target.value))}
        />
      </Field>

      <Field label="Data estimada de Entrega" required>
        <input
          type="date"
          value={toInputDate(value.data_entrega_doc)}
          onChange={(e) => set("data_entrega_doc", toBrDate(e.target.value))}
        />
      </Field>

      <Field label="Objetivo Estratégico" required hint="ex: 1.3">
        <input value={value.objetivo_estrategico} onChange={(e) => set("objetivo_estrategico", e.target.value)} />
      </Field>

      <Field label="Prioridade" required>
        <select value={value.prioridade} onChange={(e) => set("prioridade", e.target.value)}>
          {PRIORIDADE_OPCOES.map((op) => (
            <option key={op} value={op}>
              {op}
            </option>
          ))}
        </select>
      </Field>

      <Field label="Sigiloso" required>
        <select value={value.sigiloso} onChange={(e) => set("sigiloso", e.target.value)}>
          <option value="Não">Não</option>
          <option value="Sim">Sim</option>
        </select>
      </Field>
    </div>
  );
}
