class LabelEncoder:
    def __init__(
        self, character_set: list, pad_index=0, max_len: int = None, add_padding=False
    ) -> None:
        self.character_set = character_set
        self.pad_index = pad_index
        self.max_len = max_len
        self.add_padding = add_padding

    def char2index(self, c):
        i = self.character_set.index(c)
        return i if i != -1 else self.pad_index

    def encode_text(self, text: str):
        text = text[: self.max_len] if self.max_len else text
        encoded = [self.char2index(c) for c in list(text)]

        return (
            encoded + [self.pad_index] * (self.max_len - len(encoded))
            if self.add_padding and self.max_len > len(encoded)
            else encoded
        )

    def encode(self, texts):
        return (
            [self.encode_text(text) for text in texts]
            if type(texts) is list
            else self.encode_text(texts)
        )

    def decode_text(self, text):
        return "".join([self.character_set[i] for i in text])

    def decode(self, texts):
        return [self.decode_text(t) for t in texts]

    @property
    def num_classes(self):
        return len(self.character_set)


class EnglishCharacterEncoder(LabelEncoder):
    def __init__(self, max_len: int = None, add_padding=False) -> None:
        super().__init__(
            " abcdefghijklmnopqrstuvwxyz", max_len=max_len, add_padding=add_padding
        )
