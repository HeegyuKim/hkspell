import re
from collections import Counter
from .base import BaseSpellChecker


class PeterNorvigSpellChecker(BaseSpellChecker):
    def __init__(self, dictionary: Counter, letters: list):
        super().__init__()
        self.dictionary = dictionary
        self.letters = letters
        self.sum = sum(dictionary.values())

    def probability_of(self, word: str) -> float:
        "Probability of `word`."
        return self.dictionary[word] / self.sum

    def corrections(
        self, word: str, num_result: int = 1, return_probabilities: bool = False
    ) -> list:
        "Most probable spelling correction for word."
        result = sorted(
            self.candidates(word), key=lambda x: self.probability_of(x), reverse=True
        )[:num_result]

        return (
            [(x, self.probability_of(x)) for x in result]
            if return_probabilities
            else result
        )

    def candidates(self, word: str) -> list:
        "Generate possible spelling corrections for word."
        return (
            self.known([word])
            or self.known(self.edits1(word))
            or self.known(self.edits2(word))
            or [word]
        )

    def known(self, words) -> set:
        "The subset of `words` that appear in the dictionary of words."
        return set(w for w in words if w in self.dictionary)

    def edits1(self, word) -> set:
        "All edits that are one edit away from `word`."
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in self.letters]
        inserts = [L + c + R for L, R in splits for c in self.letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))


def from_english_text(text, letters=None) -> PeterNorvigSpellChecker:
    if letters is None:
        letters = list("abcdefghijklmnopqrstuvwxyz")

    words = re.findall(r"\w+", text.lower())
    checker = PeterNorvigSpellChecker(Counter(words), letters)

    return checker
