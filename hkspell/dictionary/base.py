class BaseDictionary:
    def __init__(self) -> None:
        pass

    def __len__(self):
        return 0

    def __contains__(self, word: str):
        return False

    def probability_of(self, word: str) -> float:
        """
        주어진 단어의 등장확률을 반환합니다
        단어가 없을 시 None
        """
        pass
