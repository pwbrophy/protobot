from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

servos = []

for servo in range(12):
    servos.append(servo)

for servo in servos:
    kit.servo[servo].angle = 0
    for i in range(4):
        for angle in range(0, 180, 5):
            kit.servo[servo].angle = angle
            time.sleep(0.05)
        time.sleep(0.1)
        for angle in range(180, 0, -5):
            kit.servo[servo].angle = angle
            time.sleep(0.05)
        time.sleep(0.1)
    time.sleep(1)
    kit.servo[servo].angle = None

