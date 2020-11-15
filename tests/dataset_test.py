import pytest
from torch.utils.data import DataLoader
from hkspell.dataset import SpellDataset


@pytest.fixture
def dataset():
    return SpellDataset(
        {
            "aple": ["able", "apple", "apply"],
            "correctd": ["corrects", "correct"],
            "helpp": ["help", "helped"],
        }
    )


def test_dataset_with_loader(dataset):

    loader = DataLoader(dataset, 2)

    X, y = next(iter(loader))
    print("with loader")
    print(X)
    print(y)
