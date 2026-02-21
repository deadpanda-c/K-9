#!/usr/bin/env python3
"""
Robot Web Controller with external HTML template
"""

import argparse
import threading
import logging
import time
import datetime
import os
import dotenv

from flask import Flask, render_template
from flask_socketio import SocketIO, emit


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


# Load environment variables from .env file
dotenv.load_dotenv()


parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Mock GPIO (no hardware)")
args = parser.parse_args()
DEBUG = args.debug

logging.info(f"[WEB] Starting in {'DEBUG' if DEBUG else 'LIVE'} mode")

# Import modules (they auto-detect DEBUG)
from motors import DualMotors
from ultrasonic import Ultrasonic

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
socketio = SocketIO(app, cors_allowed_origins="*")

motors = DualMotors()
sensor = Ultrasonic()

status = {
    'motors': 'stopped',
    'distance': 0.0,
    'debug': DEBUG
}

def sensor_loop():
    while True:
        distance = sensor.measure()
        if distance:
            status['distance'] = round(distance, 1)
        socketio.emit('status_update', status)
        time.sleep(0.5)

threading.Thread(target=sensor_loop, daemon=True).start()


# Better: use Flask's render_template
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('status_update', status)
    logging.info(f"[WEB] Client connected")

@socketio.on('motor_command')
def handle_motor(cmd):
    print(f"[WEB] Command: {cmd}")
    if cmd == 'forward':
        motors.forward()
        status['motors'] = 'forward'
    elif cmd == 'backward':
        motors.backward()
        status['motors'] = 'backward'
    elif cmd == 'stop':
        motors.stop()
        status['motors'] = 'stopped'
    emit('status_update', status)

if __name__ == '__main__':
    logging.info(f"[WEB] Web server started on http://0.0.0.0:5000")
    logging.info(f"[WEB] Press Ctrl+C to exit")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)

