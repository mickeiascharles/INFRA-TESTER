import { Field } from "../ui/Field";
import type { PrevisaoDuracao } from "../../types";

interface Props {
  value: PrevisaoDuracao;
  onChange: (next: PrevisaoDuracao) => void;
}

export function Step4PrevisaoDuracao({ value, onChange }: Props) {
  return (
    <div className="step-grid">
      <Field label="Vigência Contratual (meses)" required>
        <input
          value={value.vigencia_meses}
          onChange={(e) => onChange({ ...value, vigencia_meses: e.target.value })}
          inputMode="numeric"
        />
      </Field>
    </div>
  );
}
