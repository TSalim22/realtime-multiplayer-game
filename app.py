import os
import json
import re
import threading
import time
from flask import Flask, render_template, request
from flask_sock import Sock
from game import Game


def create_app():
    app = Flask(__name__)
    app.config.update(APP_TITLE='Coin Race',APP_DESCRIPTION='Collect coins with friends in a shared room.',SOCK_SERVER_OPTIONS={'ping_interval':20,'max_message_size':1024})
    sock = Sock(app)
    rooms = {}
    lock = threading.Lock()

    @app.get('/')
    def index():
        return render_template('index.html',title='Coin Race')

    @sock.route('/ws')
    def socket(ws):
        room = request.args.get('room','lobby')
        name = request.args.get('name','Player').strip()
        origin = request.headers.get('Origin')
        if origin and origin not in (f'http://{request.host}',f'https://{request.host}'):
            ws.close()
            return
        if not re.fullmatch(r'[a-zA-Z0-9_-]{1,30}',room):
            ws.send(json.dumps({'error':'Use a room name with 1–30 letters, numbers, underscores or dashes.'}))
            return
        identifier = None
        try:
            with lock:
                if room not in rooms and len(rooms)>=100:
                    raise ValueError('Too many rooms.')
                game = rooms.setdefault(room,Game())
                identifier = game.join(name)
            last_move = 0
            while True:
                message = ws.receive(timeout=.1)
                if message:
                    try:
                        data = json.loads(message)
                    except (ValueError,TypeError):
                        data = {}
                    now = time.monotonic()
                    if isinstance(data,dict) and now-last_move >= .08:
                        with lock:
                            game.move(identifier,data.get('direction'))
                        last_move = now
                with lock:
                    snapshot = json.dumps(game.snapshot(identifier))
                ws.send(snapshot)
        except ValueError as error:
            ws.send(json.dumps({'error':str(error)}))
        except Exception:
            # Closing a browser tab ends its WebSocket.
            pass
        finally:
            with lock:
                if identifier:
                    game.leave(identifier)
                    if not game.players:
                        rooms.pop(room,None)

    return app


if __name__ == '__main__':
    create_app().run(host=os.getenv('HOST','127.0.0.1'),port=5000,threaded=True)
