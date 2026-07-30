import { Field } from "../ui/Field";
import type { PrevisaoDesembolso } from "../../types";

interface Props {
  value: PrevisaoDesembolso;
  onChange: (next: PrevisaoDesembolso) => void;
}

const TIPO_DESEMBOLSO_OPCOES = ["Único", "Mensal", "Misto"];
const MESES = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
];

export function Step5PrevisaoDesembolso({ value, onChange }: Props) {
  const set = <K extends keyof PrevisaoDesembolso>(key: K, val: PrevisaoDesembolso[K]) =>
    onChange({ ...value, [key]: val });

  return (
    <div className="step-grid">
      <Field label="Tipo de Desembolso" required>
        <select value={value.tipo_desembolso} onChange={(e) => set("tipo_desembolso", e.target.value)}>
          {TIPO_DESEMBOLSO_OPCOES.map((op) => (
            <option key={op} value={op}>
              {op}
            </option>
          ))}
        </select>
      </Field>

      <Field label="Parcela Anual" required>
        <select value={value.parcela_anual} onChange={(e) => set("parcela_anual", e.target.value)}>
          <option value="Sim">Sim</option>
          <option value="Não">Não</option>
        </select>
      </Field>

      <Field label="Valor da Parcela Única" hint="Opcional, se aplicável">
        <input
          value={value.valor_parcela_unica ?? ""}
          onChange={(e) => set("valor_parcela_unica", e.target.value)}
          inputMode="decimal"
        />
      </Field>

      <Field label="Ano do Desembolso Mensal" required>
        <input value={value.ano_desembolso} onChange={(e) => set("ano_desembolso", e.target.value)} inputMode="numeric" />
      </Field>

      <Field label="Mês do Desembolso Mensal" required>
        <select value={value.mes_desembolso} onChange={(e) => set("mes_desembolso", e.target.value)}>
          {MESES.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
      </Field>

      <Field label="Valor Mensal de Desembolso" required>
        <input
          value={value.valor_mensal_desembolso}
          onChange={(e) => set("valor_mensal_desembolso", e.target.value)}
          inputMode="decimal"
        />
      </Field>
    </div>
  );
}
