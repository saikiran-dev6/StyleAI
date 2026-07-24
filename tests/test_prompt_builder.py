from styleai.services.prompt_builder import build_fallback_recommendations, build_system_prompt, build_user_prompt


def test_build_prompts():
    sys_prompt = build_system_prompt()
    assert "JSON-only" in sys_prompt

    usr_prompt = build_user_prompt(gender="Female", skin_tone="Olive", median_rgb=[140, 130, 100])
    assert "Female" in usr_prompt
    assert "Olive" in usr_prompt
    assert "[140, 130, 100]" in usr_prompt


def test_build_fallback_all_skin_tones():
    for tone in ["Fair", "Medium", "Olive", "Deep"]:
        for gender in ["Male", "Female"]:
            fb = build_fallback_recommendations(gender=gender, skin_tone=tone)
            assert fb["skin_tone"] == tone
            assert "palette" in fb
            assert "outfits" in fb
            assert "shopping_queries" in fb
