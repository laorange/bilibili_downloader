import abc
import hashlib
import re
from typing import List, Union  # , Dict
from .my_classes import MyConfig, PageInAPI, VideoDownloader, FinalUrlContainer
import httpx


class VideoParserInterface(abc.ABC):
    def __init__(self, url: str, quality: Union[str, int]):
        self.url = url
        self.quality = quality
        self.title: str = "视频标题（待更新）"
        self.page_list: List[PageInAPI] = self.get_page_list()
        self.downloader_list = self.get_downloader_list()

    def set_title(self, title: str):
        # fix: windows文件夹的名字中不能包含 \/:*?"<>|
        replace_table: dict = {"\\": "_",
                               "/": "_",
                               ":": "：",
                               "*": "x",
                               "?": "？",
                               '"': "'",
                               "<": "(",
                               ">": ")",
                               "|": "丨"}
        for forbidden_char, replace_char in replace_table.items():
            title = title.replace(forbidden_char, replace_char)
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
        html = httpx.get(start_url, headers=MyConfig.base_headers).json()
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
                **MyConfig.base_headers,
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
