import time
from typing import List, Union, Dict
from .common_util import Util
from pathlib import Path
import httpx
import asyncio
from .main_ui import Ui_bilibili_downloader


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
    def __init__(self, main_windows_ui: Ui_bilibili_downloader):
        self.ui = main_windows_ui
        self.recorded_time = time.time()

    def update_record_time(self):
        self.recorded_time = time.time()

    def enable_download_button(self):
        self.ui.download_button.setEnabled(True)

    def disable_download_button(self):
        self.ui.download_button.setEnabled(False)

    def set_download_button_text(self, text):
        self.ui.download_button.setText(text)

    def set_speed(self, speed_of_bytes: int):
        self.ui.speed.setText(Util.get_format_size(speed_of_bytes) + "/s")

    def set_progress_bar(self, progress_value: int):
        self.ui.progress_bar.setValue(progress_value)

    def set_all_progress_bar(self, all_progress_value: int):
        self.ui.all_progress_bar.setValue(all_progress_value)

    def update_status_on_ui(self, speed_of_bytes: int, progress_value: int, all_progress_value: int):
        if time.time() - self.recorded_time > MyConfig.UI_REFRESH_INTERVAL:
            self.update_record_time()
            self.set_speed(speed_of_bytes)
            self.set_progress_bar(progress_value)
            self.set_all_progress_bar(all_progress_value)

    def initialize_status(self):
        self.ui.speed.setText("----")
        self.set_progress_bar(0)
        self.set_all_progress_bar(0)
        self.enable_download_button()
        self.set_download_button_text("下载")


class PageInAPI:
    """用于记录api中的单个Page的信息。包含重要的cid"""

    def __init__(self, info_dict: Dict[str, Union[int, str]]):
        self.a_id = info_dict.get("aid", '')
        self.bv_id = info_dict.get("bvid", '')
        self.c_id = info_dict.get("cid", '')
        self.page: str = str(info_dict.get("page", '0'))
        self.part = info_dict.get("part", '')
        self.duration = info_dict.get("duration", '')
        self.vid = info_dict.get("vid", '')
        self.weblink = info_dict.get("weblink", '')
        self.dimension = info_dict.get("dimension", '')
        self.first_frame = info_dict.get("first_frame", '')
        self._from = info_dict.get("from", '')
        self._info_dict = info_dict


class FinalUrlContainer:
    def __init__(self, url, size: int = 1):
        self.url = url
        self.size = size


class VideoDownloader:
    def __init__(self, title, page: PageInAPI, target_url_list: List[FinalUrlContainer]):
        self.title = title
        self.page = page
        self.final_url_list = target_url_list

    async def download(self, local_path: Path, ui_tool_kit: UiToolKit, all_progress_value: Union[int, float]):
        for url_container in self.final_url_list:
            size_record = 0
            async_downloader = httpx.AsyncClient(headers=MyConfig.download_base_headers)
            with open(Util.ensure_dir_exists(local_path / self.title) / (self.page.part + ".mp4"), 'wb') as f:
                recorded_time = time.time()
                async with async_downloader.stream('GET', url_container.url) as response:
                    async for chunk in response.aiter_bytes():
                        size_record += len(chunk)
                        # recorded_time = time.time()
                        # print("103:", recorded_time)
                        speed = int(len(chunk) / (time.time() - recorded_time + 1e-8))
                        recorded_time = time.time()
                        progress = int(size_record / url_container.size * 100)
                        ui_tool_kit.update_status_on_ui(speed, progress, all_progress_value)
                        f.write(chunk)
            # await async_downloader.aclose()
        await asyncio.sleep(1)
