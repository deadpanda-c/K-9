import RPi.GPIO as GPIO
from time import sleep


class ServoController:
    def __init__(self, servo_pin=11, frequency=50):
        self.servo_pin = servo_pin
        self.frequency = frequency

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.servo_pin, self.frequency)
        self.pwm.start(0)
        self.last_value = 0

        self.left = 2.5     # -90 degrees
        self.neutral = 7.5  # 0 degrees
        self.right = 12     # +90 degrees

        print("ServoController initialized on pin", self.servo_pin)

    def move_to_duty_cycle(self, duty_cycle, duration=1):
        print(f"Moving servo to duty cycle {duty_cycle}%")
        self.pwm.ChangeDutyCycle(duty_cycle)
        sleep(duration)

        self.pwm.ChangeDutyCycle(0)

    def move_to_angle(self, angle, duration=1):
        if angle < -90 or angle > 90:
            raise ValueError("Angle must be between -90 and +90 degrees")

        duty_cycle = ((angle + 90) / 180) * (self.right - self.left) + self.left
        print(f"Moving to angle {angle}°, duty cycle = {duty_cycle:.2f}%")
        self.move_to_duty_cycle(duty_cycle, duration)
        return angle

    def test_servo(self):
        print("Beginning test sequence...")
        self.move_to_duty_cycle(self.left)
        self.move_to_duty_cycle(self.neutral)
        self.move_to_duty_cycle(self.right)
        print("Test sequence complete!")

    def cleanup(self):
        print("Stopping PWM and cleaning up GPIO")
        self.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    servo = ServoController(servo_pin=11)

    try:
         servo.test_servo()
         servo.move_to_angle(45)
         servo.move_to_angle(-45)
    finally:
        servo.cleanup()

