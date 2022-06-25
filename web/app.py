import traceback

import config

from flask import Flask, request, jsonify, session, render_template

app = Flask(__name__)


@app.route('/account/user')
def user_account():
    return render_template('user_account.html')


@app.route('/account/admin')
def admin_account():
    return render_template('admin_account.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


def main():
    app.run(host=config.APP_HOST, port=config.APP_PORT)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
