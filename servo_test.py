from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

servos = []

for servo in range(12):
    servos.append(servo)

for servo in servos:
    kit.servo[servo].angle = 0
    for i in range(3):
        for angle in range(0, 180, 1):
            kit.servo[servo].angle = angle
            time.sleep(0.01)
        for angle in range(180, 0, 1):
            kit.servo[servo].angle = angle
            time.sleep(0.01)
    time.sleep(2)
    kit.servo[servo].angle = None

