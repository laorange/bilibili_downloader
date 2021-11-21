import asyncio
from pathlib import Path

from .video_parsers import *
from .my_classes import UiToolKit


class VideoHandler:
    def __init__(self, url, quality: Union[str, int], save_path: Path, ui_tool_kit: UiToolKit):
        if not url:
            raise Exception("视频地址无效！请重新输入")
        self.url = url
        # quality: (1080p:80;720p:64;480p:32;360p:16)(填写80或64或32或16)
        self.quality = quality
        self.save_path = save_path
        self.ui_tool_kit = ui_tool_kit
        self.video_parser = self.get_proper_video_parser()

    def get_proper_video_parser(self) -> VideoParserInterface:
        if "bangumi" in self.url:
            return FanVideoParser(self.url, self.quality)
        else:
            return NormalVideoParser(self.url, self.quality)

    def start_download(self):
        async_tasks = []
        for _index, downloader in enumerate(self.video_parser.downloader_list):
            async_tasks.append(downloader.download(self.save_path, self.ui_tool_kit, (_index + 1) / len(self.video_parser.downloader_list) * 100))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(async_tasks))
        loop.close()


if __name__ == '__main__':
    # handle = VideoHandler('https://www.bilibili.com/video/BV11K411376D', 16)
    # handle = VideoHandler('https://www.bilibili.com/video/BV13o4y1U7hR', 16, Path(__file__).resolve().parent.parent / "test_download",
    #                       UiToolKit())
    # handle.start_download()
    print()

# https://www.bilibili.com/video/BV11K411376D?spm_id_from=333.999.0.0
# https://www.bilibili.com/video/BV1UL411t7CR?spm_id_from=333.999.0.0
# https://api.bilibili.com/x/web-interface/view?aid=377346670

# https://api.bilibili.com/x/web-interface/view?bvid=BV1UL411t7CR
# https://api.bilibili.com/x/web-interface/view?bvid=BV11K411376D
# https://api.bilibili.com/x/web-interface/view?bvid=BV13o4y1U7hR
# https://interface.bilibili.com/v2/playurl?appkey=iVGUTjsxvpLeuDCf&cid=387281578&otype=json&qn=80&quality=80&type=&sign=05b82c5bcc51c8b4614676da088140e0
# https://interface.bilibili.com/v2/playurl?appkey=iVGUTjsxvpLeuDCf&cid=392043279&otype=json&qn=80&quality=80&type=&sign=05b82c5bcc51c8b4614676da088140e0
# https://interface.bilibili.com/v2/playurl?appkey=iVGUTjsxvpLeuDCf&cid=392043279&otype=json&qn=80&quality=80&type=&sign=4755c4da064d8ba9a4dd5600c00ab842

# https://interface.bilibili.com/v2/playurl?appkey=iVGUTjsxvpLeuDCf&cid=387281578&otype=json&qn=80&quality=80&type=&sign=05b82c5bcc51c8b4614676da088140e0
