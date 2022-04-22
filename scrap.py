from requests import get
from dateutil import parser
from bs4 import BeautifulSoup

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
    
    def query_cnn(self, url):
        data = []
        try:
            req = get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            tag = soup.find('div', class_="detail_text")
            gambar = soup.find('div', class_='media_artikel').find('img').get('src')
            judul = soup.find('h1', class_='title').text
            body = tag.text
            data.append({
                "judul": judul.strip(),
                "poster": gambar.strip(),
                "body": body.replace("\n","<br>").strip(),
            })
        except:
            data.append({
                "message": "network error or invalid url ({})".format(url),
            })

        return data
        

if __name__ != '__main__':
    scrapper = Script()