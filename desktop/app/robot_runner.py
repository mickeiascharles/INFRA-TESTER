import os

import robot
from PySide6.QtCore import QThread, Signal

from . import db
from .config import ROBOT_FILE, RUNS_DIR
from .models import DemandaPCA

LOG_TAIL_LINES = 80


class _StreamAoVivo:
    """File-like object: grava no console.log e emite cada linha via sinal Qt."""

    def __init__(self, arquivo, emitir_linha):
        self._arquivo = arquivo
        self._emitir_linha = emitir_linha
        self._buffer = ""

    def write(self, texto: str) -> int:
        self._arquivo.write(texto)
        self._arquivo.flush()
        self._buffer += texto
        while "\n" in self._buffer:
            linha, self._buffer = self._buffer.split("\n", 1)
            self._emitir_linha(linha)
        return len(texto)

    def flush(self) -> None:
        self._arquivo.flush()


class RobotRunnerThread(QThread):
    linha_recebida = Signal(int, str)
    finalizado = Signal(int, str, str)  # execucao_id, status, error_message

    def __init__(self, execucao_id: int, demanda: DemandaPCA, parent=None):
        super().__init__(parent)
        self.execucao_id = execucao_id
        self.demanda = demanda

    def cancelar(self) -> None:
        # Robot Framework não expõe cancelamento cooperativo via API in-process;
        # isto é um kill forçado usado apenas ao fechar o app com execuções pendentes.
        self.terminate()

    def run(self) -> None:
        run_dir = RUNS_DIR / str(self.execucao_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        console_path = run_dir / "console.log"

        db.marcar_iniciada(self.execucao_id)

        variaveis = [f"{chave}:{valor}" for chave, valor in self.demanda.variaveis_robot().items()]
        env_original = os.environ.get("SISCORP_SENHA")
        os.environ["SISCORP_SENHA"] = self.demanda.credenciais.senha

        try:
            with open(console_path, "w", encoding="utf-8") as arquivo_log:
                stream = _StreamAoVivo(arquivo_log, lambda linha: self.linha_recebida.emit(self.execucao_id, linha))
                codigo_retorno = robot.run(
                    str(ROBOT_FILE),
                    variable=variaveis,
                    outputdir=str(run_dir),
                    stdout=stream,
                    stderr=stream,
                )
        except Exception as exc:  # noqa: BLE001
            msg = f"Falha ao executar o Robot Framework: {exc}"
            db.marcar_finalizada(self.execucao_id, "failed", "", msg)
            self.finalizado.emit(self.execucao_id, "failed", msg)
            return
        finally:
            if env_original is None:
                os.environ.pop("SISCORP_SENHA", None)
            else:
                os.environ["SISCORP_SENHA"] = env_original

        linhas = console_path.read_text(encoding="utf-8", errors="replace").splitlines()
        log_tail = "\n".join(linhas[-LOG_TAIL_LINES:])
        status = "success" if codigo_retorno == 0 else "failed"
        erro = "" if status == "success" else "O robô finalizou com falhas. Veja o log/relatório para detalhes."

        db.marcar_finalizada(self.execucao_id, status, log_tail, erro)
        self.finalizado.emit(self.execucao_id, status, erro)


def caminho_console(execucao_id: int) -> str:
    caminho = RUNS_DIR / str(execucao_id) / "console.log"
    if not caminho.exists():
        return ""
    return caminho.read_text(encoding="utf-8", errors="replace")


def caminho_artefato(execucao_id: int, nome_arquivo: str):
    caminho = RUNS_DIR / str(execucao_id) / nome_arquivo
    return caminho if caminho.exists() else None
