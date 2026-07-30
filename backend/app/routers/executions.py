import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from sqlalchemy.orm import Session

from .. import robot_runner
from ..database import get_db
from ..models import Execution
from ..schemas import DemandaPCA, ExecutionOut

router = APIRouter(prefix="/api/executions", tags=["executions"])


@router.post("", response_model=ExecutionOut)
def criar_execucao(demanda: DemandaPCA, db: Session = Depends(get_db)):
    execution = Execution(
        status="pending",
        descricao_objeto=demanda.dados_basicos.descricao_objeto,
        area_demandante=demanda.dados_basicos.area_demandante,
        ano_pca=demanda.dados_basicos.ano_pca,
        usuario=demanda.credenciais.usuario,
        payload_json=json.dumps(demanda.model_dump(exclude={"credenciais"})),
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    robot_runner.start_execution(execution.id, demanda)

    return execution


@router.get("", response_model=list[ExecutionOut])
def listar_execucoes(db: Session = Depends(get_db)):
    return db.query(Execution).order_by(Execution.id.desc()).all()


@router.get("/{execution_id}", response_model=ExecutionOut)
def obter_execucao(execution_id: int, db: Session = Depends(get_db)):
    execution = db.get(Execution, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execução não encontrada")
    return execution


@router.get("/{execution_id}/console", response_class=PlainTextResponse)
def console_execucao(execution_id: int, db: Session = Depends(get_db)):
    execution = db.get(Execution, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execução não encontrada")
    if execution.status in ("success", "failed"):
        return execution.log_tail
    return robot_runner.get_console_tail(execution_id)


def _artifact_path(execution_id: int, filename: str) -> Path:
    path = robot_runner.RUNS_DIR / str(execution_id) / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"{filename} ainda não disponível")
    return path


@router.get("/{execution_id}/report")
def report_execucao(execution_id: int):
    return FileResponse(_artifact_path(execution_id, "report.html"))


@router.get("/{execution_id}/log")
def log_execucao(execution_id: int):
    return FileResponse(_artifact_path(execution_id, "log.html"))
