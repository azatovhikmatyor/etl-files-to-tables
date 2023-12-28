import os
import glob
import time
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from scripts import engine
from scripts import log_to_file, log_to_db
from scripts.log import LogData


SOURCE_FOLDER = os.environ.get("SOURCE_FOLDER")


def read_file(file_name: str, *, echo=True) -> pd.DataFrame:
    if echo:
        log_to_file(f"Reading the file {file_name!r}")

    try:
        return pd.read_csv(file_name)
    except Exception as err:
        log_to_file(f"{err.strerror}: {err.filename!r}", mode="error")


def write_to_table(
    df: pd.DataFrame, table_name: str, engine=engine, *, echo=True
) -> None:
    if echo:
        log_to_file(f"Writing file to database as table {table_name!r}")

    try:
        df.to_sql(table_name, engine, index=False, if_exists="replace")
    except Exception as err:
        log_to_file(f"{err}", mode="error")


def main():
    # Logging to database logs table logic should be modified.
    files = glob.glob(f"{SOURCE_FOLDER}/*.csv")

    if len(files) != 0:
        for file in files:
            start_time = time.time()
            df = read_file(file_name=file)
            file_size = os.path.getsize(file)
            table_name = os.path.basename(file).split(".")[0]

            write_to_table(df=df, table_name=table_name)
            end_time = time.time()
            duration = end_time - start_time
            data = LogData(
                file_name=file,
                file_size=file_size,
                table_name=table_name,
                status="success",
                start_date="2020-10-31",  # should be modified
                duration=duration,
            )
            log_to_db(data)
            print()

    else:
        log_to_file(f"There is no file in folder {SOURCE_FOLDER!r}")


if __name__ == "__main__":
    main()
