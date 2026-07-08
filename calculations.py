import math

def calculate_shear(speed_high, speed_low, height_high, height_low):
    shear = math.log(speed_high / speed_low) / math.log(height_high / height_low)
    return round(shear, 4)

def calculate_delta_t(temp_high, temp_low):
    delta_t = (temp_high - temp_low) / (0.59 - 0.22)
    return round(delta_t, 4)

def calculate_delta_t_per_height(delta_t):
    delta_t_per_h = delta_t / (59 - 22) * 100
    return round(delta_t_per_h, 4)

def classify_stability(delta_t_per_h):
    if delta_t_per_h > 0:
        return "Unstable"
    elif delta_t_per_h < 0:
        return "Stable"
    else:
        return "Neutral"