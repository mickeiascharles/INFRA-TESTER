import datetime as dt
import os
import shutil
import subprocess
import threading

from .config import ROBOT_FILE, RUNS_DIR
from .database import SessionLocal
from .models import Execution
from .schemas import DemandaPCA

LOG_TAIL_LINES = 60

_processes: dict[int, subprocess.Popen] = {}
_lock = threading.Lock()


def _variables_for(demanda: DemandaPCA) -> dict[str, str]:
    navegador = "headlesschrome" if demanda.headless else demanda.navegador
    db = demanda.dados_basicos
    ic = demanda.itens_contratacao
    dc = demanda.dados_contratacao
    pd = demanda.previsao_duracao
    pdb = demanda.previsao_desembolso

    variables = {
        "NAVEGADOR": navegador,
        "USUARIO": demanda.credenciais.usuario,
        "STATUS_CONTRATACAO": db.status_contratacao,
        "EVENTO": db.evento,
        "ANO_PCA": db.ano_pca,
        "AREA_DEMANDANTE": db.area_demandante,
        "DESCRICAO_OBJETO": db.descricao_objeto,
        "JUSTIFICATIVA": db.justificativa,
        "ACAO": ic.acao,
        "PLANO_ORCAMENTARIO": ic.plano_orcamentario,
        "TIPO_NATUREZA": ic.tipo_natureza,
        "NATUREZA_DESCRICAO": ic.natureza_descricao,
        "STATUS_SUBITEM": ic.status_subitem,
        "TIPO_SUBITEM": ic.tipo_subitem,
        "CODIGO_SUBITEM": ic.codigo_subitem,
        "DESCRICAO_SUBITEM": ic.descricao_subitem,
        "UNIDADE_MEDIDA": ic.unidade_medida,
        "PRECO_UNITARIO": ic.preco_unitario,
        "QUANTIDADE": ic.quantidade,
        "TIPO_LICITACAO": dc.tipo_licitacao,
        "DATA_ASSINATURA": dc.data_assinatura,
        "DATA_ENTREGA_DOC": dc.data_entrega_doc,
        "OBJETIVO_ESTRATEGICO": dc.objetivo_estrategico,
        "PRIORIDADE": dc.prioridade,
        "SIGILOSO": dc.sigiloso,
        "VIGENCIA_MESES": pd.vigencia_meses,
        "TIPO_DESEMBOLSO": pdb.tipo_desembolso,
        "PARCELA_ANUAL": pdb.parcela_anual,
        "ANO_DESEMBOLSO": pdb.ano_desembolso,
        "MES_DESEMBOLSO": pdb.mes_desembolso,
        "VALOR_MENSAL_DESEMBOLSO": pdb.valor_mensal_desembolso,
    }
    if pdb.valor_parcela_unica:
        variables["VALOR_PARCELA_UNICA"] = pdb.valor_parcela_unica
    return variables


def start_execution(execution_id: int, demanda: DemandaPCA) -> None:
    thread = threading.Thread(target=_run, args=(execution_id, demanda), daemon=True)
    thread.start()


def _run(execution_id: int, demanda: DemandaPCA) -> None:
    db = SessionLocal()
    run_dir = RUNS_DIR / str(execution_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    console_path = run_dir / "console.log"

    execution = db.get(Execution, execution_id)
    execution.status = "running"
    execution.started_at = dt.datetime.utcnow()
    execution.run_dir = str(run_dir)
    db.commit()

    robot_bin = shutil.which("robot")
    if not robot_bin:
        execution.status = "failed"
        execution.error_message = (
            "Executável 'robot' não encontrado no PATH. Instale as dependências de "
            "backend/requirements.txt (robotframework + robotframework-seleniumlibrary + selenium) "
            "e um chromedriver compatível."
        )
        execution.finished_at = dt.datetime.utcnow()
        db.commit()
        db.close()
        return

    variables = _variables_for(demanda)
    args = [robot_bin, "--outputdir", str(run_dir)]
    for key, value in variables.items():
        args += ["--variable", f"{key}:{value}"]
    args.append(str(ROBOT_FILE))

    env = os.environ.copy()
    env["SISCORP_SENHA"] = demanda.credenciais.senha

    try:
        with open(console_path, "w", encoding="utf-8") as console_file:
            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                cwd=str(run_dir),
            )
            with _lock:
                _processes[execution_id] = process

            for line in process.stdout:  # type: ignore[union-attr]
                console_file.write(line)
                console_file.flush()

            return_code = process.wait()
    except Exception as exc:  # noqa: BLE001
        execution.status = "failed"
        execution.error_message = f"Falha ao iniciar o Robot Framework: {exc}"
        execution.finished_at = dt.datetime.utcnow()
        db.commit()
        db.close()
        return
    finally:
        with _lock:
            _processes.pop(execution_id, None)

    tail_lines = console_path.read_text(encoding="utf-8", errors="replace").splitlines()[-LOG_TAIL_LINES:]
    execution.log_tail = "\n".join(tail_lines)
    execution.status = "success" if return_code == 0 else "failed"
    if return_code != 0:
        execution.error_message = "O robô finalizou com falhas. Veja o log/relatório para detalhes."
    execution.finished_at = dt.datetime.utcnow()
    db.commit()
    db.close()


def get_console_tail(execution_id: int, max_lines: int = 200) -> str:
    run_dir = RUNS_DIR / str(execution_id)
    console_path = run_dir / "console.log"
    if not console_path.exists():
        return ""
    lines = console_path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(lines[-max_lines:])
