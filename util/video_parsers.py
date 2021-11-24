import abc
import hashlib
import json
import re
from typing import List, Union  # , Dict
from .my_classes import MyConfig, PageInAPI, VideoDownloader, ui_tool_kit
import httpx


class VideoParserInterface(abc.ABC):
    def __init__(self, url: str, quality: Union[str, int]):
        self.url = url
        self.quality = quality
        self.title: str = "视频标题（待更新）"
        self.downloader_list: List[VideoDownloader] = self.get_downloader_list()

    def set_title(self, title: str):
        # fix: windows文件夹的名字中不能包含 \/:*?"<>|
        replace_table: dict = {"\\": "_", "/": "_", ":": "：", "*": "x",
                               "?": "？", '"': "'", "<": "(", ">": ")", "|": "丨"}
        for forbidden_char, replace_char in replace_table.items():
            title = title.replace(forbidden_char, replace_char)
        self.title = title

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
            raise Exception("解析错误。请检查输入的网址是否正确")
        html = httpx.get(start_url, headers=MyConfig.base_headers).json()
        data: dict = html['data']
        self.set_title(data.get("title", "视频标题（更新失败）"))
        if search_p_result := re.search(r'\?p=(\d+)', self.url):
            # 单独下载分P视频中的一集
            p = search_p_result.group(1)
            return [PageInAPI(data['pages'][int(p) - 1])]
        else:
            # 如果p不存在就是全集下载
            return [PageInAPI(page) for page in data['pages']]

    def get_downloader_list(self):
        downloader_list = []
        page_list = self.get_page_list()
        for page in page_list:
            encrypted_api: str = self.get_encrypted_api(page.c_id, self.quality)
            html = httpx.get(encrypted_api, headers={
                **MyConfig.base_headers,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            }).json()
            for chunk in html['durl']:
                page.add_url(chunk['url'])
                page.add_size(int(chunk['size']))
            downloader_list.append(VideoDownloader(self.title, page))
        return downloader_list

    @staticmethod
    def get_encrypted_api(c_id, quality) -> str:
        # entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
        # app_key, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
        app_key, sec = ('iVGUTjsxvpLeuDCf', 'aHRmhWMLkdeMuILqORnYZocwMBpMEOdt')
        params = f"appkey={app_key}&cid={c_id}&otype=json&qn={quality}&quality={quality}&type="
        sign_key = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
        return f'https://interface.bilibili.com/v2/playurl?{params}&sign={sign_key}'


# window.__INITIAL_STATE__.mediaInfo.param.season_id
# https://www.bilibili.com/read/cv5293665/
# https://www.bilibili.com/bangumi/play/ss2572
class FanVideoParser(VideoParserInterface):
    def __init__(self, url: str, quality: Union[str, int]):
        # if MyConfig.sess_data == MyConfig.init_sess_data:
        #     ui_tool_kit.warning("请注意", "番剧的下载需要在”设置“-”设置cookie“中更新数据后才能下载哦~")
        super().__init__(url, quality)
        # raise Exception("当前版本不支持下载番剧")

    def get_downloader_list(self) -> List[VideoDownloader]:
        page_list = self.get_page_list()
        downloader_list = [VideoDownloader(self.title, page) for page in page_list]
        return downloader_list

    def get_page_list(self) -> List[PageInAPI]:
        temp_info_dict = {"is_vip": False}

        # region step-1 获取season_id
        if not (bv_search := re.search(r'/?bangumi/play/(\w+)/?\??', self.url)):
            raise Exception("解析错误。请检查输入的网址是否正确。")
        single_page_flag = False
        first_step_id = bv_search.group(1)
        if first_step_id.lower().startswith("ep"):
            single_page_flag = True
        start_url_step1 = "https://www.bilibili.com/bangumi/play/" + bv_search.group(1)

        html_step1: str = httpx.get(start_url_step1, headers=MyConfig.base_headers).text
        if not (search_result := re.search(r'INITIAL_STATE__=(.*?"]});', html_step1)):
            raise Exception("解析错误，请检查")
        page_info: dict = json.loads(search_result.group(1))
        self.set_title(page_info['h1Title'])
        season_id: Union[str, int] = page_info['mediaInfo']['season_id']

        # endregion

        # region step-2 获取每个episode的信息
        class Episode:
            def __init__(self, data: dict):
                self.aid = data["aid"]
                self.cid = data["cid"]
                self.id = data["id"]
                self.vid = data["id"]
                self.short_title: str = data['title']
                self.long_title: str = data['long_title']
                self.part = (self.short_title + " " + self.long_title).strip()
                self.share_url: str = data["share_url"]
                self.is_vip = (data["badge"] == "会员")
                if self.is_vip:
                    temp_info_dict["is_vip"] = True

            def __str__(self):
                return self.part

        def parse_data_step2(data: Union[dict, list, str, int], temp_episode_list=None) -> List[Episode]:
            if temp_episode_list is None:
                temp_episode_list = []
            if isinstance(data, dict):
                for key, item in data.items():
                    if key == "episodes":
                        for _episode in item:
                            temp_episode_list.append(Episode(_episode))
                    else:
                        parse_data_step2(item, temp_episode_list)
            elif isinstance(data, list):
                for item in data:
                    parse_data_step2(item, temp_episode_list)
            return temp_episode_list

        api_url_step2 = f"https://api.bilibili.com/pgc/web/season/section?season_id={season_id}"
        data_step2: dict = httpx.get(api_url_step2, headers=MyConfig.base_headers).json()
        episode_list: List[Episode] = parse_data_step2(data_step2)
        # endregion

        # region 获取最终的 page_list: List[PageInAPI]
        page_list: List[PageInAPI] = [PageInAPI(episode.__dict__) for episode in episode_list if
                                      ((not single_page_flag) or first_step_id in episode.share_url)]
        headers = {**MyConfig.base_headers,
                   'Cookie': MyConfig.sess_data,
                   'Host': 'api.bilibili.com'}
        for page in page_list:
            url_api_step3 = f'https://api.bilibili.com/x/player/playurl?cid=' \
                            f'{page.__getattribute__("cid")}&avid={page.__getattribute__("aid")}&qn={self.quality}'
            print(url_api_step3)
            html_step3 = httpx.get(url_api_step3, headers=headers).json()

            # 当下载会员视频时,如果cookie中传入的不是大会员的SESSDATA时就会返回: {'code': -404, 'message': '啥都木有', 'ttl': 1, 'data': None}
            try:
                for _chunk in html_step3['data']['durl']:
                    page.add_url(_chunk['url'])
                    page.add_size(_chunk['size'])
            except KeyError:
                if html_step3['code'] != 0:
                    ui_tool_kit.warning("注意", f'请注意!title:{page.part}，当前集数为B站大会员专享,若想下载,Cookie中请传入大会员的SESSDATA。详情请查看日志。'
                                              '\n设置方法：在”设置“-”设置cookie“中更新')
                    ui_tool_kit.write_log(f"没有大会员，已跳过Page: {page.__dict__}")
                else:
                    ui_tool_kit.warning("注意", f'请注意!遭遇未知原因解析错误！title:{page.part}，详情请查看日志')
                    ui_tool_kit.write_log(f"出错了，已跳过Page: {page.__dict__}")
        return page_list
        # endregion
