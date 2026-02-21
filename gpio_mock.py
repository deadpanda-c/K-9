import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(message)s")

# gpio_mock.py
class MockGPIO:
    BCM = "BCM"
    OUT = "OUT"
    IN = "IN"
    LOW = 0
    HIGH = 1

    def setmode(self, mode):
        logging.info(f"[GPIO MOCK] setmode({mode})")

    def setwarnings(self, flag):
        logging.info(f"[GPIO MOCK] setwarnings({flag})")

    def setup(self, pin, mode):
        logging.info(f"[GPIO MOCK] setup(pin={pin}, mode={mode})")

    def output(self, pin, value):
        logging.info(f"[GPIO MOCK] output(pin={pin}, value={value})")

    def cleanup(self):
        logging.info("[GPIO MOCK] cleanup()")

# Single instance to mimic module API
GPIO = MockGPIO()
