from easing_functions import *

def center_servos(hip_center, knee_center, kit):
    for servos in range(0, 6):
        kit.servo[servos].angle = hip_center

    for servos in range(6, 12):
        kit.servo[servos].angle = knee_center


def generate_servo_movement_curve(this_servo_current_position,
                                  this_servo_params,
                                  phase,
                                  hip_target_position_phase,
                                  hip_smooth_phase,
                                  knee_target_position_phase,
                                  knee_smooth_phase,
                                  phase_duration,
                                  hip_center,
                                  knee_center):

    set_a_phase = phase
    set_b_phase = (phase + 2) % 4

    # Hips
    if this_servo_params[0]:
        # Set A
        if this_servo_params[1]:
            # Right legs
            if this_servo_params[2]:
                return calculate_curve(hip_smooth_phase[set_a_phase], this_servo_current_position, hip_target_position_phase[set_a_phase], phase_duration)
            # Left legs
            if not this_servo_params[2]:
                left_servo_target_angle = get_left_leg_angle(hip_target_position_phase[set_a_phase], hip_center)
                return calculate_curve(hip_smooth_phase[set_a_phase], this_servo_current_position, left_servo_target_angle, phase_duration)
        # Set B
        if not this_servo_params[1]:
            # Right Legs
            if this_servo_params[2]:
                return calculate_curve(hip_smooth_phase[set_a_phase], this_servo_current_position, hip_target_position_phase[set_b_phase], phase_duration)
            # Left Legs
            if not this_servo_params[2]:
                left_leg_target_angle = get_left_leg_angle(hip_target_position_phase[set_b_phase], hip_center)
                return calculate_curve(hip_smooth_phase[set_a_phase], this_servo_current_position, left_leg_target_angle, phase_duration)

    # Knees
    if not this_servo_params[0]:
        # Set A
        if this_servo_params[1]:
            # Right legs
            if this_servo_params[2]:
                return calculate_curve(knee_smooth_phase[set_a_phase], this_servo_current_position, knee_target_position_phase[set_a_phase], phase_duration)
            # Left legs
            if not this_servo_params[2]:
                left_servo_target_angle = get_left_leg_angle(knee_target_position_phase[set_a_phase], knee_center)
                return calculate_curve(knee_smooth_phase[set_a_phase], this_servo_current_position, left_servo_target_angle, phase_duration)

        # Set B
        if not this_servo_params[1]:
            # Right Legs
            if this_servo_params[2]:
                return calculate_curve(knee_smooth_phase[set_b_phase], this_servo_current_position, knee_target_position_phase[set_b_phase], phase_duration)
            # Left Legs
            if not this_servo_params[2]:
                left_servo_target_angle = get_left_leg_angle(knee_target_position_phase[set_b_phase], knee_center)
                return calculate_curve(knee_smooth_phase[set_b_phase], this_servo_current_position, left_servo_target_angle, phase_duration)


def calculate_curve(curve_type, start_angle, end_angle, duration):
    # Smoothing 0 - ease both, 1 - ease out, 2 = ease in, 3 = linear
    if curve_type == 0:
        return CubicEaseInOut(start=start_angle, end=end_angle, duration=duration)
    if curve_type == 1:
        return CubicEaseOut(start=start_angle, end=end_angle, duration=duration)
    if curve_type == 2:
        return CubicEaseIn(start=start_angle, end=end_angle, duration=duration)
    if curve_type == 3:
        return LinearInOut(start=start_angle, end=end_angle, duration=duration)


def get_left_leg_angle(right_leg_angle, center):
    hip_offset = right_leg_angle - center
    left_leg_angle = center - hip_offset
    return left_leg_angle
