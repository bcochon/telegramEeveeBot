import os
import threading

from flask import Flask
from waitress import serve

PORT = os.getenv('PORT', 4000)

app = Flask('EeveeTelebot')
@app.route('/', methods=['GET'])
def run_check():
    return 'Running 🤙'


def start_app():
    serve(app, port=PORT)

def start():
    thread = threading.Thread(target=start_app)
    thread.start()