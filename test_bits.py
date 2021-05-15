num_servos = 12
servo_params = []

for servo in range(0, num_servos):
    servo_params.append(0)

servo_params[0] = [1, 3, 5]
servo_params[1] = [1, 3, 5]
servo_params[2] = [1, 3, 5]


print(servo_params)
