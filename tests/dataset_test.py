from json import load
import pytest
from torch.utils.data import DataLoader
from hkspell.dataset import SpellDataset


def test_dataset():
    ds = SpellDataset()
    print(ds[0], ds.X[0], ds.y[0])
    print(ds.X[20:25], ds.y[20:25])

def test_dataset_with_loader():
    ds = SpellDataset()
    loader = DataLoader(ds, 10)

    X, y = next(iter(loader))
    print("with loader")
    print(X)
    print(y)