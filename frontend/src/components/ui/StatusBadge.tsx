import type { ExecutionStatus } from "../../types";

const LABELS: Record<ExecutionStatus, string> = {
  pending: "Pendente",
  running: "Em execução",
  success: "Sucesso",
  failed: "Falhou",
};

export function StatusBadge({ status }: { status: ExecutionStatus }) {
  return <span className={`badge badge-${status}`}>{LABELS[status]}</span>;
}
