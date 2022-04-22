from flask import Flask, request
from scrap import scrapper
from template import not_found, success
import constant

app = Flask(__name__)

@app.route('/')
def index():
    path = "/"
    target_path = "{}{}".format(constant.BASE_URL, path)
    response = scrapper.query(target_path)
    return success(response)

@app.route('/<path>')
def non_index(path):
    path = "/" + path
    if path in constant.ENDPOINTS:
        target_path = "{}{}".format(constant.BASE_URL, path)
        response = scrapper.query(target_path)
        return success(response)
    else:
        return not_found([{"message": "invalid endpoint"}])
    
if __name__ == "__main__":
    app.run(debug=True)