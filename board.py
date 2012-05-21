import json

from flask import Flask, abort, g, redirect, render_template, request, url_for
import redis


REDIS_SERVER = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


app = Flask(__name__)


@app.before_request
def before_request():
    g.rconn = redis.StrictRedis(
        host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB)


@app.route('/')
def item_list():
    items = map(json.loads, g.rconn.lrange('items', 0, 10))
    return render_template('item_list.html', items=items)


@app.route('/create', methods=['POST'])
def item_create():
    if all([
            'title' in request.form,
            'text' in request.form,
        ]):
        g.rconn.lpush('items', json.dumps({
            'title': request.form['title'],
            'text': request.form['text'],
        }))
    else:
        abort(400)
    return redirect(url_for('item_list'))


if __name__ == '__main__':
    app.run()
