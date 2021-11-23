import time
from typing import List, Union, Dict
from .common_util import Util
from pathlib import Path
import httpx
import asyncio
from .signals import my_signal


class MyConfig:
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


class UiToolKit:
    def __init__(self):
        self.recorded_time = time.time()
        self.recorded_size = 0

    def update_record_time(self):
        self.recorded_time = time.time()
        self.recorded_size = 0

    @staticmethod
    def enable_download_button():
        my_signal.enable_download_button.emit()

    @staticmethod
    def disable_download_button():
        my_signal.disable_download_button.emit()

    @staticmethod
    def set_download_button_text(text):
        my_signal.set_download_button_text.emit(text)

    @staticmethod
    def set_speed(speed_str: str):
        my_signal.set_speed.emit(speed_str)

    @staticmethod
    def set_progress_bar(progress_value: int):
        my_signal.set_progress_bar.emit(progress_value)

    @staticmethod
    def set_all_progress_bar(all_progress_value: int):
        my_signal.set_all_progress_bar.emit(all_progress_value)

    @staticmethod
    def set_url_box(text: str = ""):
        my_signal.set_url_box.emit(text)

    # todo: 新增about、critical
    @staticmethod
    def about(title: str, text):
        my_signal.output_message_about.emit(title, text)

    @staticmethod
    def warning(title: str, text):
        my_signal.output_message_warning.emit(title, text)

    @staticmethod
    def critical(title: str, text):
        my_signal.output_message_critical.emit(title, text)

    def update_status_on_ui(self, progress_value: int, all_progress_value: int):
        if (interval_time := (time.time() - self.recorded_time)) > MyConfig.UI_REFRESH_INTERVAL:
            speed = int(self.recorded_size / interval_time)
            speed_text = Util.get_format_size(speed) + "/s"
            self.update_record_time()
            self.set_speed(speed_text)
            self.set_progress_bar(progress_value)
            self.set_all_progress_bar(all_progress_value)

    def initialize_status(self):
        self.set_speed("----")
        self.set_progress_bar(0)
        self.set_all_progress_bar(0)
        self.enable_download_button()
        self.set_url_box()
        self.set_download_button_text("下载")


ui_tool_kit = UiToolKit()


class PageInAPI:
    """用于记录api中的单个Page的信息。包含重要的cid"""

    # title类似于电视剧剧名，page.part类似于每一集的集名
    def __init__(self, info_dict: Dict[str, Union[int, str]]):
        self.a_id = info_dict.get("aid", '')
        self.bv_id = info_dict.get("bvid", '')
        self.c_id = info_dict.get("cid", '')
        self.page: str = str(info_dict.get("page", '0'))
        self.part = info_dict.get("part", '视频名')
        self.duration = info_dict.get("duration", '')
        self.vid = info_dict.get("vid", '')
        self.weblink = info_dict.get("weblink", '')
        self.dimension = info_dict.get("dimension", '')
        self.first_frame = info_dict.get("first_frame", '')
        self._from = info_dict.get("from", '')
        self._info_dict = info_dict

        self.url: List[str] = []
        self.size: List[int] = []

    def set_url(self, url: str):
        self.url.append(url)

    def set_size(self, size: int = 1):
        self.size.append(size)

    def get_url(self) -> List[str]:
        if not self.url:
            raise Exception("该Page的url未被设置，请使用.set_url方法设置")
        return self.url

    def get_size(self) -> List[int]:
        if not self.size:
            raise Warning("该Page的size未被设置，请使用.set_size方法设置")
        if len(self.size) != len(self.url):
            raise Exception("该Page的url和size(都是list)元素个数不同，请检查！")
        return self.size


class VideoDownloader:
    def __init__(self, title, page: PageInAPI):  # , target_url_list: List[FinalUrlContainer]
        self.title = title
        self.page = page
        self.local_path = Path(__file__)  # 这里是随便设个值，反正后面要改

    async def download(self, save_path: Path, video_format: str = ".flv", all_progress_value: Union[int, float] = 0, headers: dict = None):
        if headers is None:
            headers = MyConfig.download_base_headers
        self.local_path = Util.ensure_dir_exists(save_path / self.title)

        for _index, url in enumerate(self.page.get_url()):
            if len(self.page.get_url()) > 1:
                video_name: str = self.page.part + f"_{_index}" + video_format
            else:
                video_name: str = self.page.part + video_format

            size_record = 0
            async_downloader = httpx.AsyncClient(headers=headers)
            with open(self.local_path / video_name, 'wb') as f:
                async with async_downloader.stream('GET', url) as response:
                    async for chunk in response.aiter_bytes():
                        size_record += len(chunk)
                        progress = int(size_record / self.page.get_size()[_index] * 100)
                        ui_tool_kit.recorded_size += len(chunk)
                        ui_tool_kit.update_status_on_ui(progress, all_progress_value)
                        f.write(chunk)
        # await async_downloader.aclose()
        # await asyncio.sleep(1)
