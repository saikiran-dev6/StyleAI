from styleai.utils.color_utils import (
    calculate_luminance,
    classify_skin_tone_from_luma_and_rgb,
    rgb_to_hex,
)


def test_luminance_calculation():
    # Pure white
    assert round(calculate_luminance((255, 255, 255)), 1) == 255.0
    # Pure black
    assert round(calculate_luminance((0, 0, 0)), 1) == 0.0


def test_rgb_to_hex():
    assert rgb_to_hex((255, 255, 255)) == "#ffffff"
    assert rgb_to_hex((0, 0, 0)) == "#000000"
    assert rgb_to_hex((210, 160, 140)) == "#d2a08c"


def test_classify_fair():
    rgb = (235, 205, 195)
    luma = calculate_luminance(rgb)
    assert luma >= 190
    assert classify_skin_tone_from_luma_and_rgb(luma, rgb) == "Fair"


def test_classify_medium():
    rgb = (200, 175, 160)
    luma = calculate_luminance(rgb)
    assert 155 <= luma < 190
    assert classify_skin_tone_from_luma_and_rgb(luma, rgb) == "Medium"



def test_classify_olive():
    rgb = (145, 130, 95)
    luma = calculate_luminance(rgb)
    assert 110 <= luma < 155
    assert classify_skin_tone_from_luma_and_rgb(luma, rgb) == "Olive"


def test_classify_medium_from_olive_range_low_green():
    # Luma between 110 and 155 (luma ~127), but green channel (110) < red channel (200) * 0.82
    rgb = (200, 110, 80)
    luma = calculate_luminance(rgb)
    assert 110 <= luma < 155
    assert classify_skin_tone_from_luma_and_rgb(luma, rgb) == "Medium"



def test_classify_deep():
    rgb = (80, 55, 45)
    luma = calculate_luminance(rgb)
    assert luma < 110
    assert classify_skin_tone_from_luma_and_rgb(luma, rgb) == "Deep"
