import asyncio
from pathlib import Path

from .video_parsers import *


class VideoHandler:
    def __init__(self, url, quality: Union[str, int], video_format: str, save_path: Path):
        if not url:
            raise Exception("视频地址无效！请重新输入")
        self.url = url
        # quality: (1080p:80;720p:64;480p:32;360p:16)(填写80或64或32或16)
        self.quality = quality
        self.video_format = video_format
        self.save_path = save_path
        self.video_parser: VideoParserInterface = self.get_proper_video_parser()

    def get_proper_video_parser(self) -> VideoParserInterface:
        if "bangumi" in self.url:
            return FanVideoParser(self.url, self.quality)  # 为了下载番剧的解析器
        else:
            return NormalVideoParser(self.url, self.quality)  # 默认的解析器

    def start_download(self):
        async_tasks = []
        for _index, downloader in enumerate(self.video_parser.downloader_list):
            async_tasks.append(downloader.download(self.save_path,
                                                   self.video_format,
                                                   (_index + 1) / len(self.video_parser.downloader_list) * 100))
        new_loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(new_loop)
        # loop = asyncio.get_event_loop()
        new_loop.run_until_complete(asyncio.wait(async_tasks))
        new_loop.close()


if __name__ == '__main__':
    # https://www.bilibili.com/video/BV11K411376D
    # https://www.bilibili.com/video/BV13o4y1U7hR
    print()
