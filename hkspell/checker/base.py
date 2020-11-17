class BaseSpellChecker:
    def __init__(self) -> None:
        pass

    def corrections(
        self, word: str, num_result: int = 1, return_probabilities: bool = False
    ) -> list:
        """
        후보 단어 목록
        returns: list(tuple(word: str, prob: float))

        """
        pass
