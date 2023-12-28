import os
import argparse
import glob
import time
from datetime import datetime
from typing import final

import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv

from scripts.db import engine
from scripts.log import LogData, log_to_file, log_to_db


def read_file(file_name: str, *, echo=True) -> DataFrame:
    if echo:
        log_to_file(f"Reading the file {file_name!r}")

    try:
        return pd.read_csv(file_name)
    except Exception as err:
        log_to_file(f"{err}", mode="error")
        raise


def write_to_table(df: DataFrame, table_name: str, engine=engine, *, echo=True) -> None:
    if echo:
        log_to_file(f"Writing file to database as table {table_name!r}")

    try:
        df.to_sql(table_name, engine, index=False, if_exists="replace")
    except Exception as err:
        log_to_file(f"{err}", mode="error")
        raise


def main():
    files = glob.glob(f"{SOURCE_FOLDER}/*.csv")

    if len(files) != 0:
        for file_name in files:
            file_size_mb = os.path.getsize(file_name) / 1024**2
            table_name = os.path.basename(file_name).split(".")[0]
            start_date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            start_time = time.time()

            try:
                status = "success"
                df = read_file(file_name=file_name)
                write_to_table(df=df, table_name=table_name)
            except Exception:
                status = "error"
                log_to_file(f"ETL failed for the file {file_name!r}", mode="error")
            finally:
                end_time = time.time()
                duration = end_time - start_time
                data = LogData(
                    file_name=file_name,
                    file_size_mb=round(file_size_mb, 2),
                    table_name=table_name,
                    status=status,
                    start_date=start_date,
                    duration=round(duration, 2),
                )
                log_to_db(data)
                print()

    else:
        log_to_file(f"There is no csv file in the folder {SOURCE_FOLDER!r}")


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=False)
    args = parser.parse_args()
    
    if args.source:
        SOURCE_FOLDER:final = args.source
    else:
        try:
            SOURCE_FOLDER:final = os.environ['SOURCE_FOLDER']
        except KeyError:
            raise Exception('Source folder path should be given as command line argument or SOURCE_FOLDER environment variable must be set')
    
    if not os.path.exists(SOURCE_FOLDER):
        raise Exception('Source folder is not a directory')
    
    main()
