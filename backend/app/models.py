import datetime as dt

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Execution(Base):
    __tablename__ = "executions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending|running|success|failed
    descricao_objeto: Mapped[str] = mapped_column(String(255), default="")
    area_demandante: Mapped[str] = mapped_column(String(50), default="")
    ano_pca: Mapped[str] = mapped_column(String(10), default="")
    usuario: Mapped[str] = mapped_column(String(100), default="")
    payload_json: Mapped[str] = mapped_column(Text, default="{}")
    log_tail: Mapped[str] = mapped_column(Text, default="")
    error_message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)
    started_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    run_dir: Mapped[str] = mapped_column(String(255), default="")
