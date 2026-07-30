import { Field } from "../ui/Field";
import type { DadosBasicos } from "../../types";

interface Props {
  value: DadosBasicos;
  onChange: (next: DadosBasicos) => void;
}

const STATUS_OPCOES = ["EM PLANEJAMENTO", "EM CONTRATAÇÃO", "CONTRATADO", "CANCELADO"];

export function Step1DadosBasicos({ value, onChange }: Props) {
  const set = <K extends keyof DadosBasicos>(key: K, val: DadosBasicos[K]) =>
    onChange({ ...value, [key]: val });

  return (
    <div className="step-grid">
      <Field label="Status da Contratação" required>
        <select value={value.status_contratacao} onChange={(e) => set("status_contratacao", e.target.value)}>
          {STATUS_OPCOES.map((op) => (
            <option key={op} value={op}>
              {op}
            </option>
          ))}
        </select>
      </Field>

      <Field label="Evento" required>
        <input value={value.evento} onChange={(e) => set("evento", e.target.value)} />
      </Field>

      <Field label="Ano" required>
        <input
          value={value.ano_pca}
          onChange={(e) => set("ano_pca", e.target.value)}
          inputMode="numeric"
          maxLength={4}
        />
      </Field>

      <Field label="Área Demandante" required>
        <input
          value={value.area_demandante}
          onChange={(e) => set("area_demandante", e.target.value.toUpperCase())}
          placeholder="ex: SUPTI"
        />
      </Field>

      <Field label="Descrição do Objeto" required>
        <textarea
          value={value.descricao_objeto}
          onChange={(e) => set("descricao_objeto", e.target.value)}
          rows={3}
        />
      </Field>

      <Field label="Justificativa da Contratação" required>
        <textarea
          value={value.justificativa}
          onChange={(e) => set("justificativa", e.target.value)}
          rows={3}
        />
      </Field>
    </div>
  );
}
