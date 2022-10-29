import contrib_scribe


def test_font_size():
    for char, crepr in contrib_scribe.FONT.items():
        assert len(crepr) == 7, f'"{char}" is taller than 7 pixels'
