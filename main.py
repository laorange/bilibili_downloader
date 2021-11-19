import datetime
import os
import sqlite3
import sys
from pathlib import Path

from PySide2.QtCore import QRect, QMetaObject, QCoreApplication
from PySide2.QtGui import QIcon

from PySide2.QtWidgets import QApplication, QMessageBox, QPushButton, QPlainTextEdit, QErrorMessage, QVBoxLayout, \
    QHBoxLayout, QGroupBox, QLabel, QMainWindow, QWidget, QFileDialog
from PySide2.QtUiTools import QUiLoader
import PySide2

from ui import Ui_bilibili_downloader
from log import Ui_log

BASE_DIR = Path(__file__).resolve().parent


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_bilibili_downloader()
        self.ui.setupUi(self)

        self.db_name: str = "database.sqlite3"
        self.db: sqlite3.Connection = self.connect_db()
        self.log_window = LogWindow(self.db)

        # region 加载设置
        self.config: list = self.get_config()
        self.SAVE_PATH: Path = self.config[1]
        self.video_format: str = self.config[2]
        self.ui.video_format.setCurrentText(self.video_format)
        self.ui.save_path.setText(str(self.SAVE_PATH))
        # endregion

        # region 绑定主窗口-槽事件
        self.ui.open_base_dir.triggered.connect(self.open_base_dir)
        self.ui.quit.triggered.connect(self.quit)
        self.ui.read_log.triggered.connect(self.read_log)
        self.ui.change_save_path.clicked.connect(self.change_save_path)
        self.ui.video_format.currentIndexChanged.connect(self.video_format_event)
        # endregion

    def video_format_event(self):
        new_video_format = self.ui.video_format.currentText()
        with CursorDecorator(self.db) as c:
            c.execute(f"update Config set video_format='{new_video_format}' where true;")

    def get_config(self) -> list:
        with CursorDecorator(self.db) as c:
            c.execute("select * from Config")
            config: tuple = c.fetchone()
        return list(config)

    def connect_db(self):
        db_exists_flag: bool = (db_path := (BASE_DIR / self.db_name)).exists()
        db = sqlite3.connect(str(db_path))

        if not db_exists_flag:
            with CursorDecorator(db) as c:
                c.execute("create table Log (id INTEGER PRIMARY KEY AUTOINCREMENT, datetime char(20), info text)")
                c.execute("create table Config (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "save_path char(300), video_format char(10), video_quality char(10))")
                c.execute(f"insert into Config (save_path, video_format, video_quality) "
                          f"VALUES ('{str(BASE_DIR / 'output')}', '.flv', '16')")

                c.execute("create table Cookies (id INTEGER PRIMARY KEY AUTOINCREMENT, datetime char(20), SESSDATA text)")
                c.execute(f"insert into Cookies (datetime, SESSDATA) VALUES ('{Util.get_datetime_str_now()}', '75a75cf2%2C1564669876%2Cb7c7b171')")
        return db

    def show(self):
        self.showMinimized()

    # region Action-事件
    def open_base_dir(self):
        if sys.platform.startswith('win'):
            os.startfile(BASE_DIR)
        else:
            QMessageBox.warning(self, "很抱歉", "该功能仅支持在Windows上使用")

    def quit(self):
        choice = QMessageBox.question(self, "即将退出程序", "确认退出程序？")
        if choice:
            self.close()

    def read_log(self):
        self.log_window.show()

    # endregion

    # region 组件-对应的事件
    def change_save_path(self):
        file_dialog = QFileDialog(self)
        if new_save_path := file_dialog.getExistingDirectory(self, "请选择用于保存下载的视频的文件夹"):
            self.SAVE_PATH = new_save_path
            self.ui.save_path.setText(new_save_path)
            with CursorDecorator(self.db) as c:
                c.execute(f"update Config set save_path='{new_save_path}' where true;")
    # endregion


class LogWindow(QWidget):
    def __init__(self, database: sqlite3.Connection):
        super(LogWindow, self).__init__()
        self.db = database
        self.ui = Ui_log()
        self.ui.setupUi(self)

        self.refresh_log()
        self.ui.close_button.clicked.connect(self.close)
        self.ui.clear_log.clicked.connect(self.clear_log)

    def clear_log(self):
        choice: bool = QMessageBox.question(self, "即将删除日志", "是否删除当前的所有日志？")
        if choice:
            with CursorDecorator(self.db) as c:
                c.execute("delete from Log where true;")
        self.refresh_log()

    def refresh_log(self):
        with CursorDecorator(self.db) as c:
            c.execute("select datetime,info from Log;")
            log_output: str = ""
            for log in c.fetchall():
                log_output += f"{log[0]}: {log[1]}\n"
        self.ui.log_text.setPlainText(log_output if log_output else "当前没有日志！")


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
        return datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    # @staticmethod
    # def download_from_url(url, file_path) -> bool:
    #     logger.debug(f"\n--正在下载--\nurl:{url}\nfile_path:{file_path}\n")
    #
    #     start = time.time()  # 下载开始时间
    #     response = requests.get(url, stream=True)  # stream=True必须写上
    #     size = 0  # 初始化已下载大小
    #     chunk_size = 1024  # 每次下载的数据大小
    #     content_size = int(response.headers['content-length'])  # 下载文件总大小
    #     try:
    #         if response.status_code == 200:  # 判断是否响应成功
    #             logger.debug('{}:{size:.2f} MB'.format(file_path, size=content_size / chunk_size / 1024))
    #             with open(file_path, 'wb') as file:  # 显示进度条
    #                 for data in response.iter_content(chunk_size=chunk_size):
    #                     file.write(data)
    #                     size += len(data)
    #         durant = time.time() - start  # 下载结束时间
    #         logger.debug('\n{} -- 下载完成! 用时: {:.2f}秒，平均下载速度: {:.2f}kb/s\n'.format(
    #             file_path, durant, os.path.getsize(file_path) / durant / 1024))  # 输出下载用时时间
    #     except Exception as e:
    #         logger.error(str(e))
    #         return False
    #     return True


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
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()

    with open("requirements.txt") as f:
        f.read()
