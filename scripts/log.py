import logging
from datetime import datetime
from typing import NamedTuple
from sqlalchemy import text

from .db import engine

LOG_FILE = "logs.log"
LOG_TABLE = "dbo.logs"

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
    file_size: float
    table_name: str
    status: str
    start_date: datetime
    duration: float


def log_to_db(data: LogData) -> None:
    # UGLY: should be modified
    stmt = f"""
    insert into dbo.logs(file_name, file_size, table_name, status, start_date, duration)
    values (
        {data.file_name!r},
        {data.file_size!r},
        {data.table_name!r},
        {data.status!r},
        {data.start_date!r},
        {data.duration!r}
    );
"""
    with engine.begin() as conn:
        conn.execute(text(stmt))
