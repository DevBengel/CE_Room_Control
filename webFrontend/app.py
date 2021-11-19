import random
import json
import re
import sys
from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import time
import requests



app = Flask(__name__)
turbo = Turbo(app)

def get_Lampstate():
    lampstate_data=requests.get('http://127.0.0.1:5001/')
    data=json.loads(lampstate_data.text)
    lampstate= (str(data['switch_State']))
    return lampstate

def get_Blinds_in_Percent():
    blinds_data=requests.get('http://127.0.0.1:5001/')
    data=json.loads(blinds_data.text)
    blinds_in_Percent=(str(data['dimmer_State']))
    return f'{blinds_in_Percent}%'


def update_load():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('dashboard.html'), 'load'))
            
@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def inject_state():
    state = [int(random.random() * 100) / 100 for _ in range(3)]
    return {'lampstate': get_Lampstate(), 'blinds_in_percent': get_Blinds_in_Percent(), 'temperature': state[2]}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True,use_reloader=True)