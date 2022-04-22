from requests import get
from dateutil import parser

class Script:
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

if __name__ != '__main__':
    scrapper = Script()