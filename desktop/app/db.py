import datetime as dt
import json
import sqlite3
from dataclasses import dataclass

from .config import DB_PATH


@dataclass
class Execucao:
    id: int
    status: str
    descricao_objeto: str
    area_demandante: str
    ano_pca: str
    usuario: str
    log_tail: str
    error_message: str
    created_at: str
    started_at: str | None
    finished_at: str | None


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar() -> None:
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS execucoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL DEFAULT 'pending',
                descricao_objeto TEXT DEFAULT '',
                area_demandante TEXT DEFAULT '',
                ano_pca TEXT DEFAULT '',
                usuario TEXT DEFAULT '',
                payload_json TEXT DEFAULT '{}',
                log_tail TEXT DEFAULT '',
                error_message TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                started_at TEXT,
                finished_at TEXT
            )
            """
        )


def criar_execucao(descricao_objeto: str, area_demandante: str, ano_pca: str, usuario: str, payload: dict) -> int:
    with _conn() as conn:
        cursor = conn.execute(
            """
            INSERT INTO execucoes (status, descricao_objeto, area_demandante, ano_pca, usuario, payload_json, created_at)
            VALUES ('pending', ?, ?, ?, ?, ?, ?)
            """,
            (descricao_objeto, area_demandante, ano_pca, usuario, json.dumps(payload), dt.datetime.now().isoformat(timespec="seconds")),
        )
        return cursor.lastrowid


def marcar_iniciada(execucao_id: int) -> None:
    with _conn() as conn:
        conn.execute(
            "UPDATE execucoes SET status='running', started_at=? WHERE id=?",
            (dt.datetime.now().isoformat(timespec="seconds"), execucao_id),
        )


def marcar_finalizada(execucao_id: int, status: str, log_tail: str, error_message: str = "") -> None:
    with _conn() as conn:
        conn.execute(
            "UPDATE execucoes SET status=?, log_tail=?, error_message=?, finished_at=? WHERE id=?",
            (status, log_tail, error_message, dt.datetime.now().isoformat(timespec="seconds"), execucao_id),
        )


def listar_execucoes() -> list[Execucao]:
    with _conn() as conn:
        linhas = conn.execute("SELECT * FROM execucoes ORDER BY id DESC").fetchall()
    return [Execucao(**{k: linha[k] for k in linha.keys() if k != "payload_json"}) for linha in linhas]


def obter_execucao(execucao_id: int) -> Execucao | None:
    with _conn() as conn:
        linha = conn.execute("SELECT * FROM execucoes WHERE id=?", (execucao_id,)).fetchone()
    if not linha:
        return None
    return Execucao(**{k: linha[k] for k in linha.keys() if k != "payload_json"})
