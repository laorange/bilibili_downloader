from pathlib import Path
import os
import datetime
import sqlite3
from typing import Union, Tuple


class Util:
    @staticmethod
    def ensure_dir_exists(dir_path: Path) -> Path:
        if not dir_path.parent.exists():
            Util.ensure_dir_exists(dir_path.parent)
        if not dir_path.exists():
            os.mkdir(dir_path)
        return dir_path

    @staticmethod
    def get_datetime_str_now():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_format_size(num_of_bytes: int) -> str:
        def transform_size(num: Union[int, float], unit: int = 0) -> Tuple[Union[int, float], int]:
            if num > 1024 and unit < 4:
                return transform_size(num / 1024, unit + 1)
            return num, unit

        units = ["B", "KB", "MB", "GB", "TB"]
        final_num, unit_index = transform_size(num_of_bytes)
        return f"{final_num:.2f}{units[unit_index]}"


class CursorDecorator:
    def __init__(self, db: sqlite3.Connection):
        self.db: sqlite3.Connection = db

    def __enter__(self):
        self.cursor = self.db.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        if exc_tb is None:
            self.db.commit()
        else:
            print("EXCEPTION! type:[", exc_type, "],value:[", exc_val, "],exc_tb:[", exc_tb, "]")
            self.db.rollback()


if __name__ == '__main__':
    print(Util.get_format_size(30))
    e = Exception("哈哈哈")
    print(e)
