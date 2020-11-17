import pytest
import os
from hkspell.checker.peternorvig import from_english_text, PeterNorvigSpellChecker


@pytest.fixture
def checker():

    text = """
    Yesterday
    All my troubles seemed so far away
    Now it looks as though they're here to stay
    Oh, I believe in yesterday
    Suddenly
    I'm not half the man I used to be
    There's a shadow hangin' over me
    Oh, yesterday came suddenly
    Why she had to go, I don't know, she wouldn't say
    I said something wrong, now I long for yesterday
    Yesterday
    Love was such an easy game to play
    Now I need a place to hide away
    Oh, I believe in yesterday
    Why she had to go, I don't
    """

    return from_english_text(text)


def test_corrections(checker: PeterNorvigSpellChecker):

    words = ["belvie", "sometghin"]
    corrections = ["believe", "something"]

    for word, correct in zip(words, corrections):
        corrects = checker.corrections(word, 10, return_probabilities=True)

        assert len(corrects) <= 10
        assert corrects[0][0] == correct


def test_words_contains(checker: PeterNorvigSpellChecker):

    words_in = ["yesterday", "far", "play"]
    words_not_in = ["happy", "fruit", "computer"]

    for word in words_in:
        assert word in checker.dictionary

    for word in words_not_in:
        assert word not in checker.dictionary
