from os import error
from hkspell.norvigspell import corrections, edits1
from hkspell import norvigspell as nvs
import json
from threading import Thread
import multiprocessing as mp


def get_errors(WORDS, words, N, errors):
    for word in words:
        e1 = nvs.edit1_random(word, N)
        e2 = nvs.edit2_random(word, N)

        errors.extend(list(filter(lambda x: x not in WORDS, e1)))
        errors.extend(list(filter(lambda x: x not in WORDS, e2)))


def get_error_corrections(WORDS, errors, dataset, C):
    for e in errors:
        if e in dataset:
            continue

        corr = nvs.corrections(WORDS, e, C)
        dataset[e] = corr


def main():
    N = 1
    C = 3
    N_PROC = mp.cpu_count()

    WORDS = nvs.from_txt("raw/big.txt")
    all_words = list(WORDS.keys())
    num_words = len(WORDS)

    errors = []
    dataset = {}
    processes = []

    print(f"subprocess count : {N_PROC}")
    print("generating errors...")
    for i in range(N_PROC):
        words = all_words[i * num_words : (i + 1) * num_words]
        process = Thread(target=get_errors, args=(WORDS, words, N, errors))
        process.start()
        processes.append(process)

    for p in processes:
        p.join()

    print(f"{len(errors)} errors are generated!")

    num_errors = len(errors)
    processes = []

    print("generating error-correction pairs")
    for i in range(N_PROC):
        sub_errors = errors[i * num_errors : (i + 1) * num_errors]

        process = Thread(
            target=get_error_corrections, args=(WORDS, sub_errors, dataset, C)
        )
        process.start()
        processes.append(process)

    for p in processes:
        p.join()

    print("saving...")

    with open("raw/dataset.json", "wt") as f:
        json.dump(dataset, f)


if __name__ == "__main__":
    main()
