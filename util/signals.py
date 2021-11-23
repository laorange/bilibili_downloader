import time
from PySide2.QtCore import Signal, QObject


class MySignal(QObject):
    enable_download_button = Signal()
    disable_download_button = Signal()
    set_download_button_text = Signal(str)
    set_speed = Signal(str)
    set_progress_bar = Signal(int)
    set_all_progress_bar = Signal(int)
    set_url_box = Signal(str)

    output_message_about = Signal(str, str)
    output_message_warning = Signal(str, str)
    # output_message_question = Signal(str, str)  # 用信号传确认框的结果貌似不行？
    output_message_critical = Signal(str, str)

    write_log = Signal(str)

    def __init__(self):
        super(MySignal, self).__init__()
        self.recorded_time = time.time()


my_signal = MySignal()
