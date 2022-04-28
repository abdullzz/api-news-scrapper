from flask import Flask, request
from scrap import scrapper
from template import not_found, success, errors
import constant

app = Flask(__name__)


@app.route('/')
def index():
    try:
        response = scrapper.info()
        return success(response)
    except Exception as e:
        errors(e)


@app.route('/health')
def health():
    return success("OK")


@app.route('/v2/cnn-news/detail/')
def detail_cnn():
    target_url = request.args.get('url')
    try:
        response = scrapper.query_cnn(target_url)
        return success(response)
    except Exception as e:
        return errors(e)


@app.route('/v1/<berita_indo_api_key>/')
@app.route('/v1/<berita_indo_api_key>/<berita_indo_api_path>/')
def v1(berita_indo_api_key, berita_indo_api_path=None):
    if berita_indo_api_key in constant.BERITA_INDO_API_ENDPOINTS_GROUP.keys():
        if berita_indo_api_path is None:
            target_path = \
                "{}/{}/"\
                .format(
                    constant.BERITA_INDO_API_URL,
                    berita_indo_api_key
                )
            try:
                response = scrapper.query(target_path)
                return success(response)
            except Exception as e:
                return errors(e)
        elif berita_indo_api_path in constant.BERITA_INDO_API_ENDPOINTS_GROUP[berita_indo_api_key]:
            target_path = \
                "{}/{}/{}"\
                .format(
                    constant.BERITA_INDO_API_URL,
                    berita_indo_api_key,
                    berita_indo_api_path
                )
            try:
                response = scrapper.query(target_path)
                return success(response)
            except Exception as e:
                return errors(e)
        else:
            return not_found({
                "message": "news provider {} found, but path not found".format(berita_indo_api_key),
                "suggestion": "available {} path here : {}".format(berita_indo_api_key, constant.BERITA_INDO_API_ENDPOINTS_GROUP[berita_indo_api_key])
            })
    else:
        return not_found([{
            "message": "invalid endpoint '{}'".format(berita_indo_api_key),
            "suggestion": "available endpoint here : {}"
            .format([x for x in constant.BERITA_INDO_API_ENDPOINTS_GROUP.keys()])
        }])


@app.route('/v2/<news_provider>/')
@app.route('/v2/<news_provider>/<path>/')
def v2(news_provider, path=None):
    if news_provider in constant.INTERNAL_NEWS_PROVIDER_GROUP.keys():
        if path is None:
            target_path = \
                "{}/"\
                .format(
                    constant.INTERNAL_NEWS_PROVIDER_GROUP[news_provider]['url']
                )
            try:
                response = scrapper.query_v2(target_path)
                return success(response)
            except Exception as e:
                return errors(e)
        elif path in constant.INTERNAL_NEWS_PROVIDER_GROUP[news_provider]['endpoints']:
            target_path = \
                "{}/{}"\
                .format(
                    constant.INTERNAL_NEWS_PROVIDER_GROUP[news_provider]['url'],
                    path
                )
            try:
                response = scrapper.query_v2(target_path)
                return success(response)
            except Exception as e:
                return errors(e)
        else:
            return not_found({
                "message": "news provider {} found, but path not found".format(news_provider),
                "suggestion": "available {} path here : {}"
                .format(news_provider, constant.INTERNAL_NEWS_PROVIDER_GROUP[news_provider]['endpoints'])
            })
    else:
        return not_found([{
            "message": "invalid endpoint '{}'".format(news_provider),
            "suggestion": "available endpoint here : {}"
            .format([x for x in constant.INTERNAL_NEWS_PROVIDER_GROUP.keys()])
        }])


if __name__ == "__main__":
    app.run(debug=True)
