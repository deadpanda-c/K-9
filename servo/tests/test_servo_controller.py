import pytest
from servo_controller import ServoController

class MockPWM:
    def __init__(self, pin, freq):
        self.pin = pin
        self.freq = freq
        self.last_value = 0
        self.started = False

    def start(self, val):
        self.started = True
        self.last_value = val

    def ChangeDutyCycle(self, val):
        print(f"MockPWM: ChangeDutyCycle called with {val}")
        self.last_value = val  # <-- critical fix here

    def stop(self):
        self.started = False


class MockGPIO:
    BOARD = "BOARD"
    OUT = "OUT"

    def __init__(self):
        self.pins = {}
        self.PWM = MockPWM  # direct reference to our mock

    def setmode(self, mode):
        print(f"MockGPIO: setmode({mode})")

    def setup(self, pin, mode):
        self.pins[pin] = mode
        print(f"MockGPIO: setup({pin}, {mode})")

    def cleanup(self):
        print("MockGPIO: cleanup()")


def test_move_to_angle_valid(monkeypatch):
    mock_gpio = MockGPIO()
    monkeypatch.setattr("servo_controller.GPIO", mock_gpio)

    controller = ServoController(servo_pin=11)

    last_value = controller.move_to_angle(0)
    assert last_value == 0


def test_move_to_angle_min(monkeypatch):
    mock_gpio = MockGPIO()
    monkeypatch.setattr("servo_controller.GPIO", mock_gpio)

    controller = ServoController(servo_pin=11)
    pwm = controller.pwm

    last_value = controller.move_to_angle(-90)
    assert last_value == -90


def test_move_to_angle_max(monkeypatch):
    mock_gpio = MockGPIO()
    monkeypatch.setattr("servo_controller.GPIO", mock_gpio)

    controller = ServoController(servo_pin=11)

    last_value = controller.move_to_angle(90)
    assert last_value == 90


def test_move_to_angle_out_of_range(monkeypatch):
    mock_gpio = MockGPIO()
    monkeypatch.setattr("servo_controller.GPIO", mock_gpio)

    controller = ServoController(servo_pin=11)

    with pytest.raises(ValueError):
        controller.move_to_angle(200)

