from transformers import AlbertConfig, AlbertModel


class AlbertSpellCorrectorModel(AlbertModel):
    def __init__(self, vocab_size, max_len) -> None:
        super().__init__(
            AlbertConfig(
                vocab_size=vocab_size,
                hidden_size=512,
                num_attention_heads=8,
                num_hidden_layers=4,
                intermediate_size=1024,
                embedding_size=128,
                max_position_embeddings=max_len,
            )
        )
