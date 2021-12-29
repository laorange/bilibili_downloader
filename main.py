import datetime
import os
import re
import sqlite3
import sys
import time
import json
import traceback
from pathlib import Path
from typing import List, Dict, Union
from threading import Thread
from urllib.parse import quote, unquote

# import PySide6
import httpx
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QFileDialog

from util.main_ui import Ui_bilibili_downloader
from util.log_ui import Ui_log
from util.cookie_ui import Ui_cookie_ui

from util.common_util import Util, CursorDecorator
from util.my_classes import MyConfig, ui_tool_kit
from util.video_handler import VideoHandler
from util.signals import my_signal

__version__ = "1.2.0"

BASE_DIR = Path(os.path.realpath(sys.argv[0])).resolve().parent


class JsonConfig(object):
    def __init__(self, config_path: Path):
        self.config_dict = self.get_initialize_config()
        self.config_path: Path = config_path
        self.load_config_dict()

    @staticmethod
    def get_initialize_config() -> Dict[str, Union[int, str]]:
        config_dict = {
            "Cookie_SESSDATA": MyConfig.sess_data,
            "Cookie_datetime": Util.get_datetime_str_now(),
            "MyConfig_save_path": str(BASE_DIR / 'output'),
            "MyConfig_video_format": '.flv',
            "MyConfig_video_quality": '16',
            "MyConfig_async_tasks_max_num": "5"
        }
        return config_dict

    def load_config_dict(self):
        if self.config_path.exists():
            with open(self.config_path) as config_file:
                self.config_dict = json.load(config_file)
        else:
            self.update_config()

    def update_config(self):
        with open(self.config_path, "wt", encoding="utf-8") as config_file:
            json.dump(self.config_dict, config_file, indent=4)

    def get(self, key: str):
        if key not in self.config_dict:
            self.config_dict = self.get_initialize_config()
        return self.config_dict.get(key)

    def set(self, key: str, new_value: str):
        assert key in self.config_dict
        self.config_dict[key] = new_value
        self.update_config()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_bilibili_downloader()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Bilibili-视频下载工具 v{__version__}")

        self.quality_choices: List[str] = ["16", "32", "64", "80", "112"]

        self.db: sqlite3.Connection = self.connect_db()
        self.config = JsonConfig(BASE_DIR / MyConfig.config_file_name)
        self.log_window = LogWindow(self.db)
        self.cookie_window = CookieWindow(self.config)
        self.cookie_window.get_sess_data_and_its_update_time()  # 更新MyConfig里的设置

        # region 加载设置
        self.SAVE_PATH: Path = Path(self.config.get("MyConfig_save_path"))
        self.video_format: str = self.config.get("MyConfig_video_format")
        self.ui.video_format.setCurrentText(self.video_format)
        self.video_quality: str = self.config.get("MyConfig_video_quality")
        self.ui.video_quality.setCurrentIndex(self.quality_choices.index(self.video_quality))
        self.ui.save_path.setText(str(self.SAVE_PATH))
        self.async_tasks_max_num: int = int(self.config.get("MyConfig_async_tasks_max_num"))
        self.ui.async_tasks_max_num.setValue(self.async_tasks_max_num)
        MyConfig.sess_data = self.config.get("Cookie_SESSDATA")
        # endregion

        # region 绑定主窗口-槽事件
        self.ui.open_base_dir.triggered.connect(self.open_base_dir_func)
        self.ui.open_save_dir.triggered.connect(self.open_save_dir_func)
        self.ui.quit.triggered.connect(self.close)
        self.ui.read_log.triggered.connect(self.read_log)
        self.ui.about_this.triggered.connect(self.about_tis)
        self.ui.help_text.triggered.connect(self.help_text)
        self.ui.set_cookie_action.triggered.connect(self.set_cookie_action)
        self.ui.check_for_update_action.triggered.connect(self.check_for_update)

        self.ui.change_save_path.clicked.connect(self.change_save_path_event)
        self.ui.video_format.currentIndexChanged.connect(self.video_format_change_event)
        self.ui.video_quality.currentIndexChanged.connect(self.video_quality_change_event)
        self.ui.download_button.clicked.connect(self.download_button_clicked_event)
        self.ui.async_tasks_max_num.valueChanged.connect(self.change_async_tasks_max_num_event)

        # region 自定义信号绑定的事件
        my_signal.enable_download_button.connect(self.enable_download_button)
        my_signal.disable_download_button.connect(self.disable_download_button)
        my_signal.set_download_button_text.connect(self.set_download_button_text)
        my_signal.set_speed.connect(self.set_speed)
        my_signal.set_progress_bar.connect(self.set_progress_bar)
        my_signal.set_all_progress_bar.connect(self.set_all_progress_bar)
        my_signal.set_url_box.connect(self.set_url_box)
        my_signal.output_message_about.connect(self.output_message_about)
        my_signal.output_message_warning.connect(self.output_message_warning)
        my_signal.output_message_critical.connect(self.output_message_critical)
        my_signal.write_log.connect(self.write_log)
        # endregion
        # endregion

    def get_video_quality(self) -> str:
        # quality: (1080p:80;720p:64;480p:32;360p:16)(填写80或64或32或16)
        quality_index = self.ui.video_quality.currentIndex()
        return str(self.quality_choices[quality_index])

    @staticmethod
    def connect_db():
        db_exists_flag: bool = (db_path := (BASE_DIR / MyConfig.db_name)).exists()
        db = sqlite3.connect(str(db_path))

        if not db_exists_flag:
            with CursorDecorator(db) as c:
                c.execute("create table Log (id INTEGER PRIMARY KEY AUTOINCREMENT, datetime char(20), info text)")
        return db

    def write_log(self, log_info: str):
        with CursorDecorator(self.db) as c:
            # c.execute("create table Log (id INTEGER PRIMARY KEY AUTOINCREMENT, datetime char(20), info text)")
            sql = f"insert into Log (datetime, info) VALUES ('{Util.get_datetime_str_now()}', '{quote(log_info)}')"
            c.execute(sql)

    # region Action-事件
    def open_window_of_a_dir(self, dir_path: Path = None):
        if sys.platform.startswith('win'):
            if not dir_path:
                dir_path = BASE_DIR
            os.startfile(Util.ensure_dir_exists(dir_path))
        else:
            QMessageBox.warning(self, "很抱歉", "打开指定文件夹的功能仅支持在Windows上使用")

    def open_base_dir_func(self):
        self.open_window_of_a_dir(BASE_DIR)

    def open_save_dir_func(self):
        self.open_window_of_a_dir(self.SAVE_PATH)

    def read_log(self):
        self.log_window.showMaximized()

    def about_tis(self):
        QMessageBox.about(self, "关于本程序", f"本项目仅用于学习交流，请勿用于任何商业用途！\n"
                                         f"项目地址：https://github.com/laorange/bilibili_downloader/\n版本号：{__version__}")

    def help_text(self):
        help_text_path = BASE_DIR / 'README.pdf'
        if sys.platform.startswith('win'):
            if help_text_path.exists():
                os.startfile(help_text_path)
            elif (markdown_path := (BASE_DIR / "README.md")).exists():
                os.startfile(markdown_path)
            else:
                QMessageBox.warning(self, "警告", "未找到帮助文档，文档疑似被误删")
        else:
            QMessageBox.about(self, "提示", f"帮助文档路径：{str(help_text_path)}")

    def set_cookie_action(self):
        self.cookie_window.showMaximized()

    def check_for_update(self):
        try:
            url = "https://gitee.com/api/v5/repos/laorange/bilibili_downloader/releases/latest"
            _data: dict = httpx.get(url, headers=MyConfig.base_headers).json()
            latest_version = ".".join([group for group in re.search(r"(\d+)\.(\d+)\.(\d+)", _data.get('name')).groups()])
            if latest_version == __version__:
                ui_tool_kit.about("提示", "当前版本已经是最新版啦！")
            else:
                choice = QMessageBox.question(self, "是否更新", f"当前版本：{__version__}\n最新版本：{latest_version}\n\n是否更新？")
                if choice == QMessageBox.Yes:
                    if sys.platform.startswith('win'):
                        os.startfile("https://gitee.com/laorange/bilibili_downloader/releases/")
                    else:
                        QMessageBox.warning(self, "提示", "由于系统兼容性问题，请通过访问帮助文档中的下载地址来下载最新版本")
        except Exception as e:
            ui_tool_kit.warning("出错了", str(e))
            ui_tool_kit.write_log(traceback.format_exc())

    # endregion

    # region 组件-对应的事件
    def change_async_tasks_max_num_event(self):
        async_tasks_max_num = self.ui.async_tasks_max_num.value()
        self.config.set("MyConfig_async_tasks_max_num", async_tasks_max_num)

    def change_save_path_event(self):
        file_dialog = QFileDialog(self)
        if new_save_path := file_dialog.getExistingDirectory(self, "请选择用于保存下载的视频的文件夹"):
            self.SAVE_PATH = Path(new_save_path)
            self.ui.save_path.setText(new_save_path)
            self.config.set("MyConfig_save_path", new_save_path)

    def video_format_change_event(self):
        new_video_format = self.ui.video_format.currentText()
        self.config.set("MyConfig_video_format", new_video_format)

    def video_quality_change_event(self):
        new_video_quality = self.quality_choices[self.ui.video_quality.currentIndex()]
        self.config.set("MyConfig_video_quality", new_video_quality)

    def enable_download_button(self):
        self.ui.download_button.setEnabled(True)

    def disable_download_button(self):
        self.ui.download_button.setEnabled(False)

    def set_download_button_text(self, text):
        self.ui.download_button.setText(text)

    def set_speed(self, speed_text: str):
        self.ui.speed.setText(speed_text)

    def set_progress_bar(self, progress_value: int):
        self.ui.progress_bar.setValue(progress_value)

    def set_all_progress_bar(self, all_progress_value: int):
        self.ui.all_progress_bar.setValue(all_progress_value)

    def set_url_box(self, url_text: str):
        self.ui.url.setText(url_text)

    def output_message_about(self, title, text):
        QMessageBox.about(self, title, text)

    def output_message_warning(self, title, text):
        return QMessageBox.warning(self, title, text)

    def output_message_critical(self, title, text):
        return QMessageBox.critical(self, title, text)

    def download_button_clicked_event(self):
        def download_func():
            try:
                ui_tool_kit.revive_the_download_progress()
                ui_tool_kit.enable_download_button()
                ui_tool_kit.set_download_button_text("取消下载")
                video_handler.start_download()
                if not ui_tool_kit.block:
                    ui_tool_kit.about("完成", "下载完成！")
                self.open_window_of_a_dir(video_handler.video_parser.downloader_list[0].local_path)
            except Exception as _e:
                print_exc()
                ui_tool_kit.write_log(traceback.format_exc())
                ui_tool_kit.critical("出错了", str(_e))
            finally:
                ui_tool_kit.initialize_status()

        url = self.ui.url.text()
        if "取消" in self.ui.download_button.text():
            choice = QMessageBox.question(self, "平平无奇的确认框", "是否要强行终止下载任务？\n注：已下载的部分并不会被删除")
            if choice == QMessageBox.Yes:
                ui_tool_kit.kill_the_download_progress()
                time.sleep(1)
                QMessageBox.warning(self, "警告", "已强行终止下载任务")

        elif not url.strip():
            ui_tool_kit.critical("没有检测到输入!", "请在输入链接后再点击下载")
            ui_tool_kit.initialize_status()
        else:
            try:
                self.set_download_button_text("解析中")
                self.disable_download_button()
                QMessageBox.about(self, "请确认", "已检测到输入，即将开始解析\n解析可能会消耗若干秒钟，还请耐心等待")

                video_handler = VideoHandler(url, self.get_video_quality(), self.video_format, self.SAVE_PATH, self.async_tasks_max_num)

                video_info_list = []
                for _index, downloader in enumerate(video_handler.video_parser.downloader_list):
                    video_info_list.append(f"视频名：{downloader.title}\n{downloader.page.part}" if _index == 0 else downloader.page.part)

                video_info_showed = ui_tool_kit.get_formatted_str_from_video_info_list(video_info_list)
                choice = QMessageBox.question(self, "是否开始下载?", "以下视频将会被下载，请确认：\n" + video_info_showed)
                if choice == QMessageBox.Yes:
                    task = Thread(target=download_func)
                    task.start()
                else:
                    ui_tool_kit.initialize_status()
            except Exception as e:
                from traceback import print_exc
                print_exc()
                # QMessageBox.critical(self, "出错了", "\n".join(e.args))
                self.write_log(str(e) + f"【输入的url是：{url}】")
                QMessageBox.critical(self, "出错了", str(e))
                ui_tool_kit.initialize_status()

    # endregion

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '关闭提示', "是否要退出界面？")
        if reply == QMessageBox.Yes:
            ui_tool_kit.kill_the_download_progress()
            sys.exit(app.exec())
        elif reply == QMessageBox.No:
            event.ignore()

    def show(self):
        super(MainWindow, self).show()
        if not sys.platform.startswith('win'):
            QMessageBox.warning(self, "提示", "部分功能在非Windows系统上使用可能会有异常\n建议在Windows系统上使用本程序")


class LogWindow(QWidget):
    def __init__(self, database: sqlite3.Connection):
        super(LogWindow, self).__init__()
        self.db = database
        self.ui = Ui_log()
        self.ui.setupUi(self)

        self.ui.close_button.clicked.connect(self.close)
        self.ui.clear_log.clicked.connect(self.clear_log)

    def clear_log(self):
        choice: bool = (QMessageBox.question(self, "即将删除日志", "是否删除当前的所有日志？") == QMessageBox.Yes)
        if choice:
            with CursorDecorator(self.db) as c:
                c.execute("delete from Log where true;")
        self.refresh_log()

    def refresh_log(self):
        with CursorDecorator(self.db) as c:
            c.execute("select datetime,info from Log;")
            log_output: str = ""
            for log in c.fetchall():
                log_output += f"{log[0]}: {unquote(log[1])}\n"
        self.ui.log_text.setPlainText(log_output if log_output else "当前没有日志！")

    def showMaximized(self) -> None:
        self.refresh_log()
        super(LogWindow, self).showMaximized()


class CookieWindow(QWidget):
    def __init__(self, json_config: JsonConfig) -> None:
        super(CookieWindow, self).__init__()
        self.json_config = json_config
        self.ui = Ui_cookie_ui()
        self.ui.setupUi(self)

        self.ui.cancel_button.clicked.connect(self.close)
        self.ui.update_button.clicked.connect(self.update_button_event)

    def showMaximized(self):
        super(CookieWindow, self).showMaximized()
        self.show_latest_sess_data()

    def get_sess_data_and_its_update_time(self):
        sess_data = self.json_config.get("Cookie_SESSDATA")
        update_datetime_str = self.json_config.get("Cookie_datetime")
        return sess_data, update_datetime_str

    def show_latest_sess_data(self):
        sess_data, update_datetime_str = self.get_sess_data_and_its_update_time()
        update_datetime = datetime.datetime.strptime(update_datetime_str, MyConfig.time_format)
        if (datetime.datetime.now() - update_datetime).days > 20:
            QMessageBox.about(self, "提示", "上一次更新cookie已经是20多天以前了(有效期30天)...\n建议择日不如撞日，赶紧更新一下吧?")
        self.ui.update_datetime_text.setText(update_datetime_str)
        self.ui.SESSDATA_INPUT.setText(sess_data)

    def update_button_event(self):
        choice = QMessageBox.question(self, "确认", "是否确认更新cookie？\n")
        new_sess_data = self.ui.SESSDATA_INPUT.text()
        if new_sess_data:
            if choice == QMessageBox.Yes:
                self.json_config.set("Cookie_SESSDATA", new_sess_data)
                self.json_config.set("Cookie_datetime", Util.get_datetime_str_now())
                MyConfig.sess_data = self.json_config.get("Cookie_SESSDATA")
                QMessageBox.about(self, "提示", "更新成功！")
        else:
            QMessageBox.about(self, "提示", "你的输入是空的哟！")
        self.show_latest_sess_data()


if __name__ == '__main__':
    if sys.version_info.major + 0.1 * sys.version_info.minor < 3.8:
        input("您的python版本过低，请使用3.8及以上版本，或改写全部的海象运算符( := )")
        raise EnvironmentError

    if (cmd_file := (BASE_DIR / "cmd.txt")).exists():
        with open(cmd_file, 'rt', encoding='utf-8') as f:
            txt = f.read()
        with open(cmd_file, 'wt', encoding='utf-8') as f:
            new_txt = re.sub(r"_\d\.\d\.\d", "_" + __version__, txt)
            f.write(new_txt)

    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
