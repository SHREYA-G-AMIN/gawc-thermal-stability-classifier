import math
import pandas as pd


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
    return "Neutral"


def calculate_stability_percentages(
    df: pd.DataFrame,
    class_column="Class"
):
    if class_column not in df.columns:
        raise ValueError(f"Column '{class_column}' not found.")

    valid_values = df[class_column].dropna()
    total = len(valid_values)

    if total == 0:
        return {
            "Stable": 0.0,
            "Unstable": 0.0,
            "Neutral": 0.0
        }

    counts = valid_values.value_counts()

    return {
        "Stable": round(counts.get("Stable", 0) / total * 100, 2),
        "Unstable": round(counts.get("Unstable", 0) / total * 100, 2),
        "Neutral": round(counts.get("Neutral", 0) / total * 100, 2)
    }