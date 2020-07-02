from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import re
from flask_talisman import Talisman


app = Flask(__name__)


talisman = Talisman(app)


URL = 'https://api.telegram.org/bot983770057:AAEKKVOH-HlygTwvOqwAT54K60PRm-af-2Y/'


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='Hi, my Friend'):
    # 'https://api.telegram.org/bot983770057:AAEKKVOH-HlygTwvOqwAT54K60PRm-af-2Y/sendMessage'
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto[1:]


def get_price(crypto):
    url = 'https://yobit.net/api/2/{}_usd/ticker'.format(crypto)
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=header).json()
    price = r['ticker']['last']
    return price


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'/\w+'

        if re.search(pattern, message):
            price = get_price(parse_text(message))
            send_message(chat_id, text=price)

        return jsonify(r)
    return "I'm sorry! There was some sort of mistake. Please check the currency name"


if __name__ == "__main__":
    app.run()