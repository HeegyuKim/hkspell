import pytest
from hkspell.util import EnglishCharacterEncoder


def test_encoder():
    encoder = EnglishCharacterEncoder()
    text = "abc"
    assert encoder.encode(text) == [1, 2, 3]


def test_encoder_padded():
    encoder = EnglishCharacterEncoder(max_len=5, add_padding=True)
    text = "abc"
    assert encoder.encode(text) == [1, 2, 3, 0, 0]
