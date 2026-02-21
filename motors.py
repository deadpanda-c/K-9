#!/usr/bin/env python3
"""
Dual DC Motor Module for Raspberry Pi with optional debug (mock GPIO)
"""

import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(message)s")
# Parse debug flag early
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--debug", action="store_true")
args, _ = parser.parse_known_args()
DEBUG = args.debug

if DEBUG:
    from gpio_mock import GPIO
    logging.info("[MOTORS] Running in DEBUG mode (mock GPIO)")
else:
    import RPi.GPIO as GPIO


class DualMotors:
    def __init__(self, in1a: int = 17, in2a: int = 27, in1b: int = 22, in2b: int = 23):
        self.in1a, self.in2a = in1a, in2a
        self.in1b, self.in2b = in1b, in2b

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.in1a, GPIO.OUT)
        GPIO.setup(self.in2a, GPIO.OUT)
        GPIO.setup(self.in1b, GPIO.OUT)
        GPIO.setup(self.in2b, GPIO.OUT)

        self.stop()

    def forward(self):
        logging.info("[MOTORS] forward()")
        GPIO.output(self.in1a, GPIO.HIGH)
        GPIO.output(self.in2a, GPIO.LOW)
        GPIO.output(self.in1b, GPIO.HIGH)
        GPIO.output(self.in2b, GPIO.LOW)

    def backward(self):
        logging.info("[MOTORS] backward()")
        GPIO.output(self.in1a, GPIO.LOW)
        GPIO.output(self.in2a, GPIO.HIGH)
        GPIO.output(self.in1b, GPIO.LOW)
        GPIO.output(self.in2b, GPIO.HIGH)

    def stop(self):
        logging.info("[MOTORS] stop()")
        GPIO.output(self.in1a, GPIO.LOW)
        GPIO.output(self.in2a, GPIO.LOW)
        GPIO.output(self.in1b, GPIO.LOW)
        GPIO.output(self.in2b, GPIO.LOW)

    def cleanup(self):
        logging.info("[MOTORS] cleanup()")
        self.stop()
        GPIO.cleanup()


import atexit
atexit.register(GPIO.cleanup)
