import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import type { ExecutionOut } from "../types";
import { StatusBadge } from "../components/ui/StatusBadge";

export function Execucoes() {
  const [execucoes, setExecucoes] = useState<ExecutionOut[]>([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    let ativo = true;
    async function carregar() {
      try {
        const dados = await api.listarExecucoes();
        if (ativo) setExecucoes(dados);
      } finally {
        if (ativo) setCarregando(false);
      }
    }
    carregar();
    const id = setInterval(carregar, 4000);
    return () => {
      ativo = false;
      clearInterval(id);
    };
  }, []);

  return (
    <div className="page">
      <h1 className="page-title">Execuções</h1>
      <p className="page-subtitle">Histórico de cadastros de demanda disparados no SISCORP.</p>

      {carregando && execucoes.length === 0 && <p>Carregando...</p>}
      {!carregando && execucoes.length === 0 && (
        <p>
          Nenhuma execução ainda. <Link to="/nova">Cadastre a primeira demanda</Link>.
        </p>
      )}

      <table className="table">
        <thead>
          <tr>
            <th>#</th>
            <th>Status</th>
            <th>Descrição do Objeto</th>
            <th>Área</th>
            <th>Ano PCA</th>
            <th>Usuário</th>
            <th>Criado em</th>
          </tr>
        </thead>
        <tbody>
          {execucoes.map((ex) => (
            <tr key={ex.id}>
              <td>
                <Link to={`/execucoes/${ex.id}`}>#{ex.id}</Link>
              </td>
              <td>
                <StatusBadge status={ex.status} />
              </td>
              <td>{ex.descricao_objeto}</td>
              <td>{ex.area_demandante}</td>
              <td>{ex.ano_pca}</td>
              <td>{ex.usuario}</td>
              <td>{new Date(ex.created_at).toLocaleString("pt-BR")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
