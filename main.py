import os
import sqlite3
import sys
from pathlib import Path
from typing import List
from threading import Thread

# import PySide2
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QFileDialog

from util.main_ui import Ui_bilibili_downloader
from util.log_ui import Ui_log
from util.common_util import Util, CursorDecorator
from util.my_classes import UiToolKit
from util.video_handler import VideoHandler

BASE_DIR = Path(__file__).resolve().parent


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_bilibili_downloader()
        self.ui.setupUi(self)

        self.db_name: str = "database.sqlite3"
        self.quality_choices: List[str] = ["16", "32", "64", "80", "112"]

        self.db: sqlite3.Connection = self.connect_db()
        self.log_window = LogWindow(self.db)

        # region 加载设置
        self.config: list = self.get_config()
        self.SAVE_PATH: Path = Path(self.config[1])
        self.video_format: str = self.config[2]
        self.ui.video_format.setCurrentText(self.video_format)
        self.video_quality: str = self.config[3]
        self.ui.video_quality.setCurrentIndex(self.quality_choices.index(self.video_quality))
        self.ui.save_path.setText(str(self.SAVE_PATH))
        self.ui_tool_kit = UiToolKit(self.ui)
        # endregion

        # region 绑定主窗口-槽事件
        self.ui.open_base_dir.triggered.connect(self.open_window_of_a_dir)
        self.ui.quit.triggered.connect(self.quit)
        self.ui.read_log.triggered.connect(self.read_log)
        self.ui.change_save_path.clicked.connect(self.change_save_path_event)
        self.ui.video_format.currentIndexChanged.connect(self.video_format_change_event)
        self.ui.video_quality.currentIndexChanged.connect(self.video_quality_change_event)
        self.ui.download_button.clicked.connect(self.download_button_clicked_event)
        # endregion

    def get_config(self) -> list:
        with CursorDecorator(self.db) as c:
            c.execute("select * from MyConfig")
            config: tuple = c.fetchone()
        return list(config)

    def get_video_quality(self) -> str:
        # quality: (1080p:80;720p:64;480p:32;360p:16)(填写80或64或32或16)
        quality_index = self.ui.video_quality.currentIndex()
        return str(self.quality_choices[quality_index])

    def connect_db(self):
        db_exists_flag: bool = (db_path := (BASE_DIR / self.db_name)).exists()
        db = sqlite3.connect(str(db_path))

        if not db_exists_flag:
            with CursorDecorator(db) as c:
                c.execute("create table Log (id INTEGER PRIMARY KEY AUTOINCREMENT, datetime char(20), info text)")
                c.execute("create table MyConfig (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "save_path char(300), video_format char(10), video_quality char(10))")
                c.execute(f"insert into MyConfig (save_path, video_format, video_quality) "
                          f"VALUES ('{str(BASE_DIR / 'output')}', '.flv', '16')")

                c.execute("create table Cookies (id INTEGER PRIMARY KEY AUTOINCREMENT, datetime char(20), SESSDATA text)")
                c.execute(f"insert into Cookies (datetime, SESSDATA) VALUES ('{Util.get_datetime_str_now()}', '75a75cf2%2C1564669876%2Cb7c7b171')")
        return db

    def show(self):
        self.showMinimized()

    # region Action-事件
    def open_window_of_a_dir(self, dir_path: Path = None):
        if sys.platform.startswith('win'):
            if dir_path is None:
                dir_path = BASE_DIR
            os.startfile(dir_path)
        else:
            QMessageBox.warning(self, "很抱歉", "该功能仅支持在Windows上使用")

    def quit(self):
        choice = QMessageBox.question(self, "即将退出程序", "确认退出程序？")
        if choice == QMessageBox.Yes:
            self.close()

    def read_log(self):
        self.log_window.show()

    # endregion

    # region 组件-对应的事件
    def change_save_path_event(self):
        file_dialog = QFileDialog(self)
        if new_save_path := file_dialog.getExistingDirectory(self, "请选择用于保存下载的视频的文件夹"):
            self.SAVE_PATH = new_save_path
            self.ui.save_path.setText(new_save_path)
            with CursorDecorator(self.db) as c:
                c.execute(f"update MyConfig set save_path='{new_save_path}' where true;")

    def video_format_change_event(self):
        new_video_format = self.ui.video_format.currentText()
        with CursorDecorator(self.db) as c:
            c.execute(f"update MyConfig set video_format='{new_video_format}' where true;")

    def video_quality_change_event(self):
        new_video_quality = self.quality_choices[self.ui.video_quality.currentIndex()]
        with CursorDecorator(self.db) as c:
            c.execute(f"update MyConfig set video_quality='{new_video_quality}' where true;")

    def download_button_clicked_event(self):
        def download_func(self):
            try:
                self.ui_tool_kit.disable_download_button()
                self.ui_tool_kit.set_download_button_text("解析中")
                video_handler = VideoHandler(url, self.get_video_quality(), self.SAVE_PATH, self.ui_tool_kit)
                video_info_list = [f"{downloader.title}-{downloader.page.part}" for downloader in video_handler.video_parser.downloader_list]
                video_info_showed = "以下视频将会被下载，请确认：\n" + "\n".join(video_info_list)
                choice = QMessageBox.question(self, "是否开始下载?", video_info_showed)
                if choice == QMessageBox.Yes:
                    self.ui_tool_kit.set_download_button_text("下载中")
                    video_handler.start_download()
                self.ui_tool_kit.initialize_status()

                choice = QMessageBox.question(self, "完成", "下载完成！是否打开视频所在文件夹？")
                if choice == QMessageBox.Yes:
                    self.open_window_of_a_dir(self.SAVE_PATH)
            except Exception as e:
                from traceback import print_exc
                print_exc()
                QMessageBox.critical(self, "出错了", "\n".join(e.args))

        url = self.ui.url.text()
        if not url.strip():
            QMessageBox.critical(self, "没有检测到输入!", "请在输入链接后再点击下载")
        else:
            # task = Thread(target=download_func, args=[self])
            # task.start()
            download_func(self)
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


if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()
