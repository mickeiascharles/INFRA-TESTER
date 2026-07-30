import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import type { ExecutionOut } from "../types";
import { StatusBadge } from "../components/ui/StatusBadge";

export function ExecucaoDetalhe() {
  const { id } = useParams<{ id: string }>();
  const execucaoId = Number(id);
  const [execucao, setExecucao] = useState<ExecutionOut | null>(null);
  const [console_, setConsole] = useState("");
  const consoleRef = useRef<HTMLPreElement>(null);

  useEffect(() => {
    let ativo = true;
    async function tick() {
      const [ex, log] = await Promise.all([
        api.obterExecucao(execucaoId),
        api.consoleExecucao(execucaoId),
      ]);
      if (!ativo) return;
      setExecucao(ex);
      setConsole(log);
    }
    tick();
    const interval = setInterval(() => {
      if (execucao && (execucao.status === "success" || execucao.status === "failed")) return;
      tick();
    }, 2000);
    return () => {
      ativo = false;
      clearInterval(interval);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [execucaoId, execucao?.status]);

  useEffect(() => {
    consoleRef.current?.scrollTo({ top: consoleRef.current.scrollHeight });
  }, [console_]);

  if (!execucao) {
    return (
      <div className="page">
        <p>Carregando execução #{execucaoId}...</p>
      </div>
    );
  }

  const finalizado = execucao.status === "success" || execucao.status === "failed";

  return (
    <div className="page">
      <p>
        <Link to="/execucoes">← Voltar para execuções</Link>
      </p>
      <div className="detail-header">
        <h1 className="page-title">Execução #{execucao.id}</h1>
        <StatusBadge status={execucao.status} />
      </div>
      <p className="page-subtitle">
        {execucao.descricao_objeto} — {execucao.area_demandante} / {execucao.ano_pca}
      </p>

      {execucao.error_message && <p className="alert-error">{execucao.error_message}</p>}

      {finalizado && (
        <div className="wizard-actions" style={{ marginBottom: 16 }}>
          <a className="btn btn-secondary" href={api.urlRelatorio(execucao.id)} target="_blank" rel="noreferrer">
            Ver Report (Robot Framework)
          </a>
          <a className="btn btn-secondary" href={api.urlLog(execucao.id)} target="_blank" rel="noreferrer">
            Ver Log detalhado
          </a>
        </div>
      )}

      <h3 className="step-subtitle">
        {finalizado ? "Log final" : "Executando... acompanhe em tempo real"}
      </h3>
      <pre className="console-output" ref={consoleRef}>
        {console_ || "Aguardando início do robô..."}
      </pre>
    </div>
  );
}
