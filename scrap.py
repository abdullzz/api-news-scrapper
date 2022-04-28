from requests import get
from dateutil import parser
from bs4 import BeautifulSoup
import asyncio
from threading import Thread
from pendulum import local
import pyppeteer
from requests_html import HTMLSession, AsyncHTMLSession
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import constant


class Script:
    def info(self):
        datas = []
        for k, v in constant.BERITA_INDO_API_ENDPOINTS_GROUP.items():
            datas.append({
                "endpoint": "/v1/{}/".format(k),
                "status": "active",
                "info": "{} scrapper index endpoint".format(k),
                "provider": "berita-indo-api"
            })
            for value in v:
                datas.append({
                    "endpoint": "/v1/{}/{}".format(k, value),
                    "status": "active",
                    "info": "{} scrapper categorical endpoint".format(k),
                    "provider": "berita-indo-api"
                })
        for k, v in constant.INTERNAL_NEWS_PROVIDER_GROUP.items():
            datas.append({
                "endpoint": "/v2/{}/".format(k),
                "status": "active",
                "info": "{} scrapper index endpoint".format(k),
                "provider": "internal"
            })
            for endpoint in v['endpoints']:
                datas.append({
                    "endpoint": "/v2/{}/{}".format(k, endpoint),
                    "status": "active",
                    "info": "{} scrapper categorical endpoint".format(k),
                    "provider": "internal"
                })
        datas.append({
            "endpoint": "/v2/cnn-news/detail/?url=",
            "status": "active",
            "info": "cnn article specific scrapper",
            "provider": "internal"
        })
        return datas

    def query(self, url):
        response = get(url)
        response = response.json()
        datas = []
        for d in response["data"]:
            datas.append({
                "judul": d["title"],
                "link": d["link"],
                "tanggal": parser.parse(d["isoDate"])
            })
        return datas

    def query_cnn(self, url):
        data = []
        try:
            req = get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            tag = soup.find('div', class_="detail_text")
            gambar = soup.find('div', class_='media_artikel').find(
                'img').get('src')
            judul = soup.find('h1', class_='title').text
            body = tag.text
            data.append({
                "judul": judul.strip(),
                "poster": gambar.strip(),
                "body": body.replace("\n", "<br>").strip().replace("<br><br>","<br>").replace("<br><br><br>","<br>"),
            })
        except:
            if url:
                data.append({
                    "message": "network error or invalid url ({})".format(url),
                })
            else:
                data.append({
                    "message": "error, please provide target url argument",
                })

        return data

    def query_v2(self, url_target):
        data = []

        async def get_post(url):
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            session = AsyncHTMLSession()
            browser = await pyppeteer.launch({
                'ignoreHTTPSErrors': True,
                'headless': True,
                'handleSIGINT': False,
                'handleSIGTERM': False,
                'handleSIGHUP': False,
                'args': [
                    '--proxy-server="direct://"',
                    '--proxy-bypass-list=*',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            })
            session._browser = browser
            resp_page = await session.get(url)
            await resp_page.html.arender(timeout=20)
            return resp_page

        loop = asyncio.new_event_loop()
        url = url_target
        asyncio.set_event_loop(loop)
        print(url)
        result = loop.run_until_complete(get_post(url))
        article = result.html.find('article')
        counter = 0
        for info in article:
            judul = info.xpath('//h2/text()')
            link = info.xpath('//a/@href')
            tanggal = info.xpath("//span[contains(@class, 'date')]/text()")
            if len(judul) > 0 and len(link) > 0 and len(tanggal) > 0:
                waktu = tanggal[0].replace("\u2022", "").strip()
                if waktu.lower() != "promoted":
                    data.append({
                        "judul": judul[0],
                        'link': link[0],
                        'waktu': waktu,
                        'tanggal': self.substract_date(waktu)
                    })
                    counter += 1
        return data

    def substract_date(self, value):
        now = datetime.now(timezone(timedelta(hours=7)))
        values = value.split(" ")
        hour_minute = int(values[0])
        types = value[1]
        past = timedelta(hours=hour_minute) if types == "jam" else timedelta(
            minutes=hour_minute)
        return str((now - past).strftime('%a, %m %Y %H:%M:%S'))


if __name__ != '__main__':
    scrapper = Script()
