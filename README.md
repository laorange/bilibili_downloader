# Bilibili_downloader

## [特点]

1. 使用了`pyside2`构建ui

2. 使用了`httpx`以协程方式下载
3. 借鉴java接口式、面向对象式开发(java初学者的一次尝试)
4. 大部分代码进行了类型标注

- [x] 能够下载单集的普通视频
- [x] 能够下载多集的普通视频
- [ ] 能够下载番剧

## [截图]



## [二次开发构思]

`VideoHandler`在初始化时，会调用`get_proper_video_parser`方法，如下方代码所示

```python
# video_handler.py
class VideoHandler:
    def __init__(self, url, quality: Union[str, int], video_format: str, save_path: Path):
		# ...
        self.video_parser = self.get_proper_video_parser()

    def get_proper_video_parser(self) -> VideoParserInterface:
        if "bangumi" in self.url:
            return FanVideoParser(self.url, self.quality)  # 为了下载番剧的解析器
        else:
            return NormalVideoParser(self.url, self.quality)  # 默认的解析器
```

可以在此方法中自定义返回的视频分析器(继承自`VideoParserInterface`)

```python
# my_classes.py
class VideoParserInterface(abc.ABC):
    def __init__(self, url: str, quality: Union[str, int]):
        # ...
        self.downloader_list: List[VideoDownloader] = self.get_downloader_list()

    @abc.abstractmethod
    def get_downloader_list(self) -> List[VideoDownloader]:
        pass
```

`PageInAPI`是用于记录某一集视频的详细信息(命名由来：b站的API对某一集的视频的名为`Page`)

```python
# my_classes.py
class PageInAPI:
    """用于记录api中的单个Page的信息。包含重要的cid"""
    # 另一处的title类似于电视剧剧名，此处的PageInAPI.part类似于每一集的集名
    def __init__(self, info_dict: Dict[str, Union[int, str]]):
        # ...
        self.part = info_dict.get("part", '视频名')
        # ...
```

## [next-step]

- [ ] 写入log
- [ ] 写完readme
- [ ] 推上github

## [参考]

接口参考：[`Henryhaohao/Bilibili_video_download`](https://github.com/Henryhaohao/Bilibili_video_download)

