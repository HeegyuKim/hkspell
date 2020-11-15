import pytest
import torch

from hkspell.model import CNNModel


def test_cnn_model():
    X = torch.LongTensor([[1, 2, 3, 0, 0], [3, 2, 5, 1, 0]])
    model = CNNModel(10)

    y = model(X)
    # print(X, y)

    assert y.shape == (2, 5, 10)
