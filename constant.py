BERITA_INDO_API_URL = 'https://berita-indo-api.vercel.app/v1'
BERITA_INDO_API_ENDPOINTS_GROUP = {
    "antara-news":[
        "terkini",
        "top-news",
        "politik",
        "hukum",
        "ekonomi",
        "metro",
        "sepakbola",
        "olahraga",
        "humaniora",
        "lifestyle",
        "hiburan",
        "dunia",
        "infografik",
        "tekno",
        "otomotif",
        "warta-bumi",
        "rilis-pers",
    ],
    # 'cnbc-news': [
    #     "market",
    #     "investment",
    #     "news",
    #     "entrepreneur",
    #     "syariah",
    #     "tech",
    #     "lifestyle"
    # ],
    'cnn-news': [
        "nasional",
        "internasional",
        "ekonomi",
        "olahraga",
        "teknologi",
        "hiburan",
        "gaya-hidup"
    ],
    # 'republika-news': [
    #     "news",
    #     "nusantara",
    #     "khazanah",
    #     "islam-digest",
    #     "internasional",
    #     "ekonomi",
    #     "sepakbola",
    #     "leisure",
    # ],
}

INTERNAL_NEWS_PROVIDER_GROUP = {
    "cnn-news": {
        "url": "https://www.cnnindonesia.com",
        "endpoints": [
            "nasional",
            "internasional",
            "ekonomi",
            "olahraga",
            "teknologi",
            "hiburan",
            "gaya-hidup"            
        ]
    }
}
