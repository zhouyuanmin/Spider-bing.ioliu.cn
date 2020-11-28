import re
import os
import requests
from typing import Set, AnyStr


class Spider(object):
    def __init__(self):
        self.url = 'https://bing.ioliu.cn/?p={p}'
        self.download_url = 'http://h2.ioliu.cn/bing/{url}_1920x1080.jpg?images'  # + 'lim'
        self.download_urls: Set[AnyStr] = set()
        self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'}

    def crawling_jpg_url(self, page: int = 144):
        for p in range(page):
            try:
                # 下载页面
                html = requests.get(
                    self.url.format(p=p),
                    headers=self.headers
                ).text
                # 提取下载链接
                urls = re.findall(
                    pattern=r'<a class="mark" href="/photo/(.*?)\?force=home.*?"></a>',
                    string=html
                )
                if not urls:
                    # logging
                    with open('error1.log', 'a') as f:
                        f.write(f'{self.url.format(p=p)}\n')
                # 拼接下载链接
                urls = [self.download_url.format(url=url) for url in urls]

                for url in urls:
                    # 添加下载链接到集合
                    self.download_urls.add(url)
                    # logging
                    print(f'Extract links: {url}')
            except requests.exceptions.RequestException:
                # 出现异常，记录
                with open('error1.log', 'a') as f:
                    f.write(f'{self.url.format(p=p)}\n')

    def test(self):
        self.crawling_jpg_url(1)
        print(f'self.download_urls={self.download_urls}')
        self.download()

    def download(self, folder='wallpaper'):
        # 创建文件夹
        if not os.path.isdir(folder):
            os.mkdir(folder)
        # 下载文件
        for url in self.download_urls:
            try:
                content: bytes = requests.get(url=url, headers=self.headers).content
                file = os.path.join(folder, f'{url[24:-40]}.jpg')
                with open(file, 'wb') as f:
                    f.write(content)
                print(f'Finished {url}')
            except requests.exceptions.RequestException:
                # 出现异常，记录
                with open('error2.log', 'a') as f:
                    f.write(f'{url}\n')

    def run(self):
        self.crawling_jpg_url(114)
        self.download()


if __name__ == '__main__':
    s = Spider()
    s.run()
