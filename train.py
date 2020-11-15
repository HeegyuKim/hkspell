
from hkspell.model import CNNModel
from hkspell.dataset import SpellDataset

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader



def train(model, dataset, epochs = 1, dev="cuda"):
    loader = DataLoader(dataset, 512, True)
    optimizer = torch.optim.Adam(model.parameters())
    criterion = torch.nn.BCELoss()

    losses = []

    for epoch in range(1, epochs + 1):
        model.train()
        model.to(dev)

        for X, y in loader:
            X = X.to(dev)
            y = y.to(dev)

            y_pred = model(X)

            optimizer.zero_grad()
            loss = criterion(y_pred, y)
            loss.backward()
            optimizer.step()

            losses.append(loss.item())

        print(f"Mean loss of epoch {epoch}: {np.mean(losses)}")
        torch.save(model.state_dict(), f"saved_models/test-{epoch:02d}.pt")
        print()

        test(model, dataset)


def test(model, dataset, dev="cpu"):
    model.eval()
    model.to(dev)

    n_test = 10

    X, _ = dataset[:n_test]
    y_pred = torch.argmax(model(X), dim=2)
    y_pred_text = dataset.encoder.decode(y_pred)

    for i in range(n_test):
        X_text = dataset.X[i]
        y_text = dataset.y[i]

        print(f"Item: {y_text}({X_text}), predicted: {y_pred_text[i]}")


def main():
    dataset = SpellDataset()
    model = CNNModel(n_classes=dataset.encoder.num_classes)
    dev = "cuda"
    
    model.to(dev)

    print("Start training...")
    train(model, dataset, 100)

    torch.save(model.state_dict(), "saved_models/test.pt")

if __name__ == "__main__":
    main()