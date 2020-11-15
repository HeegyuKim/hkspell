import pytest
import torch
from torch import dtype

from hkspell.model import AlbertSpellCorrectorModel


@pytest.fixture
def model():
    model = AlbertSpellCorrectorModel(5, 5)
    model.eval()
    return model


def test_albert(model):
    X = torch.tensor([
        [0, 1, 2, 3, 4],
        [0, 1, 2, 3, 0],
    ], dtype=torch.float32)

    y = model(X)

    assert y.shape == (2, 5, 5)


