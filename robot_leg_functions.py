

def center_servos(hip_center, knee_center, kit):
    for servos in range(0, 6):
        kit.servo[servos].angle = hip_center

    for servos in range(6, 12):
        kit.servo[servos].angle = knee_center