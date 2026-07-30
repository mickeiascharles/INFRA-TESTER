import type { ReactNode } from "react";

interface FieldProps {
  label: string;
  children: ReactNode;
  hint?: string;
  required?: boolean;
}

export function Field({ label, children, hint, required }: FieldProps) {
  return (
    <label className="field">
      <span className="field-label">
        {label}
        {required && <span className="field-required">*</span>}
      </span>
      {children}
      {hint && <span className="field-hint">{hint}</span>}
    </label>
  );
}
