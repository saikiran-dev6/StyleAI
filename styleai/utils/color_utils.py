from typing import Tuple


def calculate_luminance(rgb: Tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def classify_skin_tone_from_luma_and_rgb(luma: float, rgb: Tuple[int, int, int]) -> str:
    r, g, b = rgb

    if luma >= 190:
        return "Fair"
    elif 155 <= luma < 190:
        return "Medium"
    elif 110 <= luma < 155:
        # Olive skin check: green channel is not materially lower than red channel (g / (r + 1e-5) > 0.85)
        if g >= (r * 0.82):
            return "Olive"
        return "Medium"
    else:
        return "Deep"
