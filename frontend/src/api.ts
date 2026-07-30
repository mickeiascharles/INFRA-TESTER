import type { DemandaPCA, ExecutionOut } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || `Erro HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  criarExecucao: (demanda: DemandaPCA) =>
    fetch(`${API_BASE}/api/executions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(demanda),
    }).then((res) => handle<ExecutionOut>(res)),

  listarExecucoes: () =>
    fetch(`${API_BASE}/api/executions`).then((res) => handle<ExecutionOut[]>(res)),

  obterExecucao: (id: number) =>
    fetch(`${API_BASE}/api/executions/${id}`).then((res) => handle<ExecutionOut>(res)),

  consoleExecucao: (id: number) =>
    fetch(`${API_BASE}/api/executions/${id}/console`).then((res) => res.text()),

  urlRelatorio: (id: number) => `${API_BASE}/api/executions/${id}/report`,
  urlLog: (id: number) => `${API_BASE}/api/executions/${id}/log`,
};
