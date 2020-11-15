import re
import random
from collections import Counter


def from_txt(path):
    return Counter(words(open(path).read()))

def words(text): 
    return re.findall(r'\w+', text.lower())

def P(WORDS, word, N=None): 
    "Probability of `word`."
    if N is None:
        N = sum(WORDS.values())

    return WORDS[word] / N

def correction(WORDS, word): 
    "Most probable spelling correction for word."
    return max(WORDS, candidates(WORDS, word), key=lambda x: P(WORDS, x))

def corrections(WORDS, word, k): 
    "Most probable spelling correction for word."
    return sorted(candidates(WORDS, word), key=lambda x: P(WORDS, x), reverse=True)[:k]

def candidates(WORDS, word): 
    "Generate possible spelling corrections for word."
    return (known(WORDS, [word]) or known(WORDS, edits1(word)) or known(WORDS, edits2(word)) or [word])

def known(WORDS, words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def edit1_random(word, n=1):
    "Random edits that are one edit away from `word`."
    edits = edits1(word)
    return random.sample(edits, n)

def edit2_random(word, n=1):
    "Random edits that are two edit away from `word`."
    return (e2 for e1 in edit1_random(word, n) for e2 in edit1_random(e1, n))