import time
from PySide2.QtCore import Signal, QObject


# class UiToolKit:
#
    # def enable_download_button(self):
    #     self.ui.download_button.setEnabled(True)
    #
    # def disable_download_button(self):
    #     self.ui.download_button.setEnabled(False)
    #
    # def set_download_button_text(self, text):
    #     self.ui.download_button.setText(text)
    #
    # def set_speed(self, speed_text: str):
    #     self.ui.speed.setText()
    #
    # def set_progress_bar(self, progress_value: int):
    #     self.ui.progress_bar.setValue(progress_value)
    #
    # def set_all_progress_bar(self, all_progress_value: int):
    #     self.ui.all_progress_bar.setValue(all_progress_value)


class MySignal(QObject):
    enable_download_button = Signal()
    disable_download_button = Signal()
    set_download_button_text = Signal(str)
    set_speed = Signal(str)
    set_progress_bar = Signal(int)
    set_all_progress_bar = Signal(int)

    def __init__(self):
        super(MySignal, self).__init__()
        self.recorded_time = time.time()


my_signal = MySignal()
