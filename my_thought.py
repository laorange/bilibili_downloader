import hashlib
import re

import httpx
import abc
from typing import List, Union, Dict

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

async_downloader = httpx.AsyncClient()


# https://interface.bilibili.com/v2/playurl?appkey=iVGUTjsxvpLeuDCf&cid=387281578&otype=json&qn=80&quality=80&type=&sign=05b82c5bcc51c8b4614676da088140e0

# def get_cid(bv_id="BV1UL411t7CR"):
#     bv_id = bv_id
#     api_url_root = "https://api.bilibili.com/x/web-interface/view?"
#     api_url = api_url_root + "bvid=" + bv_id
#
#     print(api_url)
#
#     api_data: dict = httpx.get(api_url, headers={
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
#     }).json()
#
#     print(api_data)
#     try:
#         return api_data.get("data").get("cid")
#     except Exception as e:
#         print(e)
#         print("cid获取时出错")


# def get_api_url(cid: str):
#     appkey = 'iVGUTjsxvpLeuDCf'
#     sec = 'aHRmhWMLkdeMuILqORnYZocwMBpMEOdt'
#
#     params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, 80, 80)
#     sign_key = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
#     url_api = f'https://interface.bilibili.com/v2/playurl?{params}&sign={sign_key}'
#
#     print(url_api, appkey, cid, 80, params, sign_key)
#
#     return url_api


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


class VideoDownloader:
    def __init__(self, title, page: PageInAPI, url_list: List[str]):
        self.title = title
        self.page = page
        self.url_list = url_list

    async def download(self, local_path):
        pass


class VideoParserInterface(abc.ABC):
    def __init__(self, url: str, quality: Union[str, int]):
        self.url = url
        self.quality = quality
        self.title: str = "视频标题（待更新）"
        self.page_list: List[PageInAPI] = self.get_page_list()
        self.downloader_list = self.get_downloader_list()
        # self.interface_of_play_url: List[str] = self.get_interface_of_play_url()
        # self.play_list: List[str] = self.get_play_list()

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
            downloader_list.append(VideoDownloader(self.title, page, [chunk['url'] for chunk in html['durl']]))
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
        for downloader in self.video_parser.downloader_list:
            downloader.download(safe_path)


if __name__ == '__main__':
    # print(get_cid())
    # cid = get_cid()
    # print(get_api_url(cid))
    handle = VideoHandler('https://www.bilibili.com/video/BV1UL411t7CR?spm_id_from=333.999.0.0', 16)
