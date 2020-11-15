import torch
import torch.nn as nn
import torch.nn.functional as F


class CNNModel(nn.Module):
    def __init__(self, n_classes):
        super().__init__()

        self.n_classes = n_classes
        self.embedding_dim = 128

        self.emb = nn.Embedding(
            embedding_dim=128, num_embeddings=n_classes, padding_idx=0
        )
        self.convs = nn.Sequential(
            nn.Conv1d(128, 256, 3, padding=1),
            nn.LeakyReLU(),
            nn.Conv1d(256, 256, 3, padding=1),
            nn.LeakyReLU(),
            nn.Conv1d(256, 256, 3, padding=1),
            nn.LeakyReLU(),
        )
        self.linear = nn.Sequential(nn.Linear(256, n_classes), nn.Softmax(dim=2))

    def forward(self, X):
        X = self.emb(X).permute(0, 2, 1)
        X = self.convs(X).permute(0, 2, 1)
        X = self.linear(X)
        return X
