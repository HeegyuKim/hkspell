import json
import re

import torch
from torch.utils.data import Dataset
import torch.nn.functional as F

from hkspell.util import EnglishCharacterEncoder


class SpellDataset(Dataset):
    def __init__(self, dataset=None) -> None:
        super().__init__()

        self.encoder = EnglishCharacterEncoder(max_len=16, add_padding=True)

        if dataset is None:
            with open("raw/dataset.json") as f:
                dataset = json.load(f)

        exp = re.compile(r"[^a-z]")
        errors = [k for k in dataset.keys() if not exp.search(k)]
        self.X = errors
        self.y = [dataset[k][0] for k in errors]

    def __len__(self) -> int:
        return len(self.X)

    def __getitem__(self, index):
        X = self.encoder.encode(self.X[index])
        y = self.encoder.encode(self.y[index])
        return (
            torch.tensor(X),
            F.one_hot(torch.tensor(y), self.encoder.num_classes).float(),
        )
