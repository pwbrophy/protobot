from easing_functions import *


def center_servos(hip_center, knee_center, kit):
    for servos in range(0, 6):
        kit.servo[servos].angle = hip_center

    for servos in range(6, 12):
        kit.servo[servos].angle = knee_center


def generate_servo_movement_curve(this_servo_current_position,    # Current position of the servo
                                  this_servo_params,              # Parameters related to this servo
                                  phase,                          # Current phase that we're in
                                  hip_target_position_phase,      # The array containing all the hip targets
                                  hip_smooth_phase,               # The array containing all the hip target smoothing
                                  knee_target_position_phase,     # The array containing all the knee targets
                                  knee_smooth_phase,              # The array containing all the knee target smoothing
                                  phase_duration,                 # How long our phase should last
                                  hip_center,                     # The center point of the hip movement
                                  knee_center,                    # The center point of the knee movement
                                  phase_offset,                   # How many phases we shift the 'b' set legs
                                  turning_speed,                  # The amount we shift adjust the legs for turning
                                  use_current_position):          # True = blend to the current position, not the array

    set_a_phase = phase
    print(phase)
    print(phase_offset)
    set_b_phase = (phase + phase_offset) % 4


    print("set a phase "+str(set_a_phase))
    print("set b phase "+str(set_b_phase))

    hip_target_position_a = hip_target_position_phase[set_a_phase]
    hip_target_position_b = hip_target_position_phase[set_b_phase]
    knee_target_position_a = knee_target_position_phase[set_a_phase]
    knee_target_position_b = knee_target_position_phase[set_b_phase]

    turning_turned_off = False      # Make sure turning is turned on


    # If the target position for the servo is set to '-1' then we're going to use the previous version
    if hip_target_position_a == -1 or use_current_position:
        hip_target_position_a = this_servo_current_position
        turning_turned_off = True
    if hip_target_position_b == -1 or use_current_position:
        hip_target_position_b = this_servo_current_position
        turning_turned_off = True
    if knee_target_position_a == -1 or use_current_position:
        knee_target_position_a = this_servo_current_position
        turning_turned_off = True
    if knee_target_position_b == -1 or use_current_position:
        knee_target_position_b = this_servo_current_position
        turning_turned_off = True

    # Turn based on the input, but only if we're not using a previous phase value which has already been turned
    if not turning_turned_off:
        hip_target_position_a = apply_turning(hip_target_position_a, turning_speed, this_servo_params[2], hip_center)
        hip_target_position_b = apply_turning(hip_target_position_b, turning_speed, this_servo_params[2], hip_center)

    # Hips
    if this_servo_params[0]:
        # Set A
        if this_servo_params[1]:
            # Right legs
            if this_servo_params[2]:
                return calculate_curve(hip_smooth_phase[set_a_phase],
                                       this_servo_current_position,
                                       hip_target_position_a,
                                       phase_duration)
            # Left legs
            if not this_servo_params[2]:
                left_servo_target_angle = get_left_leg_angle(hip_target_position_a, hip_center, turning_turned_off)
                return calculate_curve(hip_smooth_phase[set_a_phase],
                                       this_servo_current_position,
                                       left_servo_target_angle,
                                       phase_duration)
        # Set B
        if not this_servo_params[1]:
            # Right Legs
            if this_servo_params[2]:
                return calculate_curve(hip_smooth_phase[set_b_phase],
                                       this_servo_current_position,
                                       hip_target_position_b,
                                       phase_duration)
            # Left Legs
            if not this_servo_params[2]:
                left_leg_target_angle = get_left_leg_angle(hip_target_position_b, hip_center, turning_turned_off)
                return calculate_curve(hip_smooth_phase[set_b_phase],
                                       this_servo_current_position,
                                       left_leg_target_angle,
                                       phase_duration)

    # Knees
    if not this_servo_params[0]:
        # Set A
        if this_servo_params[1]:
            # Right legs
            if this_servo_params[2]:
                return calculate_curve(knee_smooth_phase[set_a_phase],
                                       this_servo_current_position,
                                       knee_target_position_a,
                                       phase_duration)
            # Left legs
            if not this_servo_params[2]:
                return calculate_curve(knee_smooth_phase[set_a_phase],
                                       this_servo_current_position,
                                       knee_target_position_a,
                                       phase_duration)

        # Set B
        if not this_servo_params[1]:
            # Right Legs
            if this_servo_params[2]:
                return calculate_curve(knee_smooth_phase[set_b_phase],
                                       this_servo_current_position,
                                       knee_target_position_b,
                                       phase_duration)
            # Left Legs
            if not this_servo_params[2]:
                return calculate_curve(knee_smooth_phase[set_b_phase],
                                       this_servo_current_position,
                                       knee_target_position_b,
                                       phase_duration)

def apply_turning(servo_angle, turning, hip_is_right, hip_center):
    # Apply turning multiplier
    # Right hips
    if hip_is_right:
        # Get the offset from the center position
        offset = servo_angle - hip_center
        if turning > 0:  # If we are turning right, slow down the right servos
            # Map the range 0 to +1 to the range +1 to -1
            right_turn_speed = (turning - 0.5)*-2
            # Multiply the offset by the input
            offset = offset * right_turn_speed
        return hip_center + offset

    # Left hips
    if not hip_is_right:
        offset = servo_angle - hip_center
        if turning < 0:
            left_turn_speed = (turning + 0.5)*-2
            offset = offset * -left_turn_speed
        return hip_center + offset

def calculate_curve(curve_type, start_angle, end_angle, duration):
    # Smoothing 0 - ease both, 1 - ease out from current, 2 = ease in to next, 3 = linear

    if curve_type == 0:
        return CubicEaseInOut(start=start_angle, end=end_angle, duration=duration)
    if curve_type == 1:
        return CubicEaseOut(start=start_angle, end=end_angle, duration=duration)
    if curve_type == 2:
        return CubicEaseIn(start=start_angle, end=end_angle, duration=duration)
    if curve_type == 3:
        return LinearInOut(start=start_angle, end=end_angle, duration=duration)


def get_left_leg_angle(right_leg_angle, center, turning_turned_off):
    left_leg_angle = right_leg_angle
    if not turning_turned_off:
        hip_offset = right_leg_angle - center
        left_leg_angle = center - hip_offset

    return left_leg_angle
