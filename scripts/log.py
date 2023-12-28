import logging
from datetime import datetime
from typing import NamedTuple, final
from sqlalchemy import insert

from .db import engine, LogTable

LOG_FILE:final = "logs.log"

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def log_to_file(msg: str, mode: str = "info") -> None:
    match mode:
        case "info":
            logging.info(msg=msg)
        case "error":
            logging.error(msg=msg)
        case _:
            raise ValueError("`mode` must be `info` or `error`")

    print(msg)


class LogData(NamedTuple):
    file_name: str
    file_size_mb: float
    table_name: str
    status: str
    start_date: datetime
    duration: float


def log_to_db(data: LogData) -> None:
    stmt = insert(LogTable).values(
        file_name=data.file_name,
        file_size_mb=data.file_size_mb,
        table_name=data.table_name,
        status=data.status,
        start_date=data.start_date,
        duration=data.duration,
    )
    with engine.begin() as conn:
        conn.execute(stmt)