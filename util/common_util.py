from pathlib import Path
import os
import datetime
import sqlite3
from typing import Union, Tuple


class MyConfig:
    """项目的全局变量，哪里需要哪里调"""
    sess_data_update_datetime_str = "很久很久以前"
    init_sess_data = '75a75cf2%2C1564669876%2Cb7c7b171'
    sess_data = '75a75cf2%2C1564669876%2Cb7c7b171'
    time_format = "%Y-%m-%d %H:%M:%S"
    base_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    download_base_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Range': 'bytes=0-',  # Range 的值要为 bytes=0- 才能下载完整视频
        'Origin': 'https://www.bilibili.com',
        "Referer": "https://www.bilibili.com/video/",
        'Connection': 'keep-alive',
    }
    # ui刷新的间隔时间
    UI_REFRESH_INTERVAL = 1


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
        return datetime.datetime.now().strftime(MyConfig.time_format)

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
