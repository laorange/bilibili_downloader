import os
import sqlite3
import sys
from pathlib import Path

from PySide2.QtCore import QRect, QMetaObject, QCoreApplication
from PySide2.QtGui import QIcon

from PySide2.QtWidgets import QApplication, QMessageBox, QPushButton, QPlainTextEdit, QErrorMessage, QVBoxLayout, \
    QHBoxLayout, QGroupBox, QLabel, QMainWindow, QWidget
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

        self.db_name = "database.sqlite3"
        self.db = self.connect_db()
        self.log_window = LogWindow(self.db)

        self.OUTPUT_PATH = BASE_DIR / "output"
        self.ui.save_path.setText(str(self.OUTPUT_PATH))

        self.ui.open_base_dir.triggered.connect(self.open_base_dir)
        self.ui.quit.triggered.connect(self.quit)
        self.ui.read_log.triggered.connect(self.read_log)

    def connect_db(self):
        db_exists_flag = (db_path := (BASE_DIR / self.db_name)).exists()
        db = sqlite3.connect(str(db_path))

        if not db_exists_flag:
            c = db.cursor()
            c.execute("create table Log (id INTEGER PRIMARY KEY AUTOINCREMENT, datetime char(20), info text)")
            c.close()
            db.commit()
        return db

    def show(self):
        self.showMinimized()

    # region Action事件
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
        choice = QMessageBox.question(self, "即将删除日志", "是否删除当前的所有日志？")
        if choice:
            c = self.db.cursor()
            c.execute("delete from Log where true;")
            c.close()
            self.db.commit()
        self.refresh_log()

    def refresh_log(self):
        c = self.db.cursor()
        c.execute("select datetime,info from Log;")
        log_output = ""
        for log in c.fetchall():
            log_output += f"{log[0]}: {log[1]}\n"
        c.close()
        self.ui.log_text.setPlainText(log_output if log_output else "当前没有日志！")

    # def show(self):
    #     super(LogWindow, self).show()


class Util:
    @staticmethod
    def ensure_dir_exists(dir_path: Path) -> Path:
        if not dir_path.parent.exists():
            Util.ensure_dir_exists(dir_path.parent)
        if not dir_path.exists():
            os.mkdir(dir_path)
        return dir_path

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


if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()
