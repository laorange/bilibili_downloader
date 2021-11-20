import abc
import hashlib
import re
import asyncio
from pathlib import Path
from typing import List, Union, Dict

import httpx

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

    # def get_url_parameters(self):


class FinalUrlContainer:
    def __init__(self, url, size: int = 1):
        self.url = url
        self.size = size


class VideoDownloader:
    def __init__(self, title, page: PageInAPI, target_url_list: List[FinalUrlContainer]):
        self.title = title
        self.page = page
        self.final_url_list = target_url_list

    async def download(self, local_path: Path):
        for url_container in self.final_url_list:
            size_record = 0
            async_downloader = httpx.AsyncClient(headers=download_base_headers)
            with open(Util.ensure_dir_exists(local_path / self.title) / (self.page.part + ".mp4"), 'wb') as f:
                async with async_downloader.stream('GET', url_container.url) as response:
                    async for chunk in response.aiter_raw():
                        size_record += len(chunk)
                        print(f"\r进度：{size_record / url_container.size * 100:.2f}%", end="")
                        f.write(chunk)
        await asyncio.sleep(1)


class VideoParserInterface(abc.ABC):
    def __init__(self, url: str, quality: Union[str, int]):
        self.url = url
        self.quality = quality
        self.title: str = "视频标题（待更新）"
        self.page_list: List[PageInAPI] = self.get_page_list()
        self.downloader_list = self.get_downloader_list()

    def set_title(self, title: str):
        self.title = title

    @abc.abstractmethod
    def get_page_list(self) -> List[PageInAPI]:
        pass

    @abc.abstractmethod
    def get_downloader_list(self) -> List[VideoDownloader]:
        pass


class NormalVideoParser(VideoParserInterface):
    def __init__(self, url: str, quality: Union[str, int]):
        super().__init__(url, quality)

    def get_page_list(self) -> List[PageInAPI]:
        if bv_search := re.search(r'/?(BV\w+)/?', self.url):
            start_url = "https://api.bilibili.com/x/web-interface/view?bvid=" + bv_search.group(1)
        elif av_search := re.search(r'/(av\d+)/?', self.url):
            start_url = "https://api.bilibili.com/x/web-interface/view?aid=" + av_search.group(1)
        else:
            raise Exception("解析错误。请检查输入的网址是否正确。")
        html = httpx.get(start_url, headers=base_headers).json()
        data: dict = html['data']
        self.set_title(data.get("title", "视频标题（更新失败）"))
        if '?p=' in start_url:
            # 单独下载分P视频中的一集
            p = re.search(r'\?p=(\d+)', start_url).group(1)
            return [PageInAPI(data['pages'][int(p) - 1])]
        else:
            # 如果p不存在就是全集下载
            return [PageInAPI(page) for page in data['pages']]

    def get_downloader_list(self):
        downloader_list = []
        for page in self.page_list:
            encrypted_api: str = self.get_encrypted_api(page.c_id)
            html = httpx.get(encrypted_api, headers={
                **base_headers,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            }).json()
            downloader_list.append(VideoDownloader(self.title, page, [FinalUrlContainer(chunk['url'], int(chunk['size'])) for chunk in html['durl']]))
        return downloader_list

    def get_encrypted_api(self, c_id) -> str:
        # entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
        # app_key, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
        app_key, sec = ('iVGUTjsxvpLeuDCf', 'aHRmhWMLkdeMuILqORnYZocwMBpMEOdt')
        params = f"appkey={app_key}&cid={c_id}&otype=json&qn={self.quality}&quality={self.quality}&type="
        sign_key = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
        return f'https://interface.bilibili.com/v2/playurl?{params}&sign={sign_key}'


class FanVideoParser(VideoParserInterface):
    def __init__(self, url: str, quality: Union[str, int]):
        super().__init__(url, quality)
        raise Exception("当前版本不支持下载番剧")

    def get_page_list(self) -> List[PageInAPI]:
        pass

    def get_downloader_list(self):
        pass


class VideoHandler:
    def __init__(self, url, quality: Union[str, int]):
        self.url = url
        # quality: (1080p:80;720p:64;480p:32;360p:16)(填写80或64或32或16)
        self.quality = quality
        self.video_parser = self.get_proper_video_parser()

    def get_proper_video_parser(self) -> VideoParserInterface:
        if "bangumi" in self.url:
            return FanVideoParser(self.url, self.quality)
        else:
            return NormalVideoParser(self.url, self.quality)

    def start_download(self, safe_path):
        async_tasks = []
        for downloader in self.video_parser.downloader_list:
            async_tasks.append(downloader.download(safe_path))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(async_tasks))
        loop.close()


class Util:
    @staticmethod
    def ensure_dir_exists(dir_path: Path) -> Path:
        import os
        if not dir_path.parent.exists():
            Util.ensure_dir_exists(dir_path.parent)
        if not dir_path.exists():
            os.mkdir(dir_path)
        return dir_path

    @staticmethod
    def get_datetime_str_now():
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")


if __name__ == '__main__':
    # handle = VideoHandler('https://www.bilibili.com/video/BV11K411376D', 16)
    handle = VideoHandler('https://www.bilibili.com/video/BV13o4y1U7hR', 16)
    handle.start_download(Path(__file__).resolve().parent)
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
