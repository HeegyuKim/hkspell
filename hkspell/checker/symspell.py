import re

from .base import BaseSpellChecker
from collections import Counter, defaultdict


def deletes(word):
    if len(word) <= 1:
        return []

    "All edits that are one edit away from `word`."
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    return [L + R[1:] for L, R in splits if R]


def levenshtein(s1, s2, debug=False):
    """
    from https://lovit.github.io/nlp/2018/08/28/levenshtein_hangle/
    :param s1:
    :param s2:
    :param debug:
    :return:
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1, debug)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))

        if debug:
            print(current_row[1:])

        previous_row = current_row

    return previous_row[-1]


class SymSpellChecker(BaseSpellChecker):
    def __init__(self, dictionary: Counter, letters: list):
        super().__init__()
        self.dictionary = dictionary
        self.letters = letters
        self.sum = sum(dictionary.values())

        delete_dict = defaultdict(list)

        for word in dictionary.keys():
            delete_dict[word].append(word)

            dels = deletes(word)
            dels.extend([d2 for d1 in dels for d2 in d1])

            for d in dels:
                delete_dict[d].append(word)

        self.delete_dict = delete_dict

    def corrections(
        self, word: str, num_result: int = 1, return_probabilities: bool = False
    ) -> list:

        dels = deletes(word)
        dels.extend([d2 for d1 in dels for d2 in d1])

        candidates = [w for d in dels for w in self.delete_dict[d]]
        candidates = [
            (k, v)
            for k, v in Counter(candidates).most_common()
            if levenshtein(k, word) <= 2
        ]

        # TODO: 만약 두 후보간 카운트가 같으면 빈도수에 따라 정렬..안해도 될 듯? ;;

        return candidates


def from_english_text(text, letters=None) -> SymSpellChecker:
    if letters is None:
        letters = list("abcdefghijklmnopqrstuvwxyz")

    words = re.findall(r"\w+", text.lower())
    checker = SymSpellChecker(Counter(words), letters)

    return checker
