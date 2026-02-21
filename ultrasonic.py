#!/usr/bin/env python3
"""
Ultrasonic HC-SR04 Module with optional debug mode
"""

import argparse
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(message)s")

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--debug", action="store_true")
args, _ = parser.parse_known_args()
DEBUG = args.debug

if DEBUG:
    from gpio_mock import GPIO
    logging.info("ULTRASONIC: Debug mode enabled")
else:
    import RPi.GPIO as GPIO


class Ultrasonic:
    def __init__(self, trig: int = 23, echo: int = 24):
        self.trig = trig
        self.echo = echo
        self.speed_of_sound = 0.034
        self.timeout = 0.05

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trig, False)
        time.sleep(0.2)

    def measure(self):
        if DEBUG:
            # Return fake distance for local testing
            fake_distance = 42.0
            logging.info(f"ULTRASONIC: Fake distance: {fake_distance}")
            return fake_distance

        # Real measurement
        try:
            GPIO.output(self.trig, True)
            time.sleep(0.00001)
            GPIO.output(self.trig, False)

            timeout_start = time.time()
            while GPIO.input(self.echo) == 0:
                pulse_start = time.time()
                if pulse_start - timeout_start > self.timeout:
                    return None

            timeout_start = time.time()
            while GPIO.input(self.echo) == 1:
                pulse_end = time.time()
                if pulse_end - timeout_start > self.timeout:
                    return None

            pulse_duration_us = (pulse_end - pulse_start) * 1_000_000
            distance_cm = (self.speed_of_sound * pulse_duration_us) / 2
            return distance_cm

        except:
            return None

    def cleanup(self):
        GPIO.cleanup()


import atexit
atexit.register(GPIO.cleanup)
