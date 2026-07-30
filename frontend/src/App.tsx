import { NavLink, Route, Routes } from "react-router-dom";
import { NovaDemanda } from "./pages/NovaDemanda";
import { Execucoes } from "./pages/Execucoes";
import { ExecucaoDetalhe } from "./pages/ExecucaoDetalhe";
import "./App.css";

function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-brand">
          <span className="app-brand-mark">SA</span>
          <span>
            SISCORP <strong>PCA</strong>
          </span>
        </div>
        <nav className="app-nav">
          <NavLink to="/nova" className={({ isActive }) => (isActive ? "active" : "")}>
            Nova Demanda
          </NavLink>
          <NavLink to="/execucoes" className={({ isActive }) => (isActive ? "active" : "")}>
            Execuções
          </NavLink>
        </nav>
      </header>

      <main className="app-main">
        <Routes>
          <Route path="/" element={<NovaDemanda />} />
          <Route path="/nova" element={<NovaDemanda />} />
          <Route path="/execucoes" element={<Execucoes />} />
          <Route path="/execucoes/:id" element={<ExecucaoDetalhe />} />
        </Routes>
      </main>

      <footer className="app-footer">Automação de cadastro de PCA via Robot Framework — INFRA S.A.</footer>
    </div>
  );
}

export default App;
