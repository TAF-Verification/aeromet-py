import re
from typing import List


def _add_space_left(word: str) -> str:
    """Add space to the left of word."""
    return " " + word


def _add_space_right(word: str) -> str:
    """Add space to the right of word."""
    return word + " "


def _add_space_both(word: str) -> str:
    """Add space to the left and right of words."""
    word = _add_space_left(word)
    return _add_space_right(word)


def split_sentence(
    sentence: str, words: List[str], count: int = 0, space: str = ""
) -> List[str]:
    """Split the `sentence` given by the list of `words` without
    lost that words.

    Args:
        sentence (str): the sentence to split.
        words (List[str]): the list of words where the sentence will be splitted.
        count (int, optional): Number of splits of every coincidence. Defaults to 0.
        space (str, optional): take spaces in count to the left or right of every word.
            Defaults to ''. Options: `left`, `right`, `both`

    Returns:
        List[str, str]: the list of sentence splitted from the original.
    """
    for word in words:
        if space == "left":
            word = _add_space_left(word)
        elif space == "right":
            word = _add_space_right(word)
        elif space == "both":
            word = _add_space_both(word)
        else:
            pass

        pattern = re.compile(word)
        sentence = re.sub(
            pattern,
            "|" + word.lstrip(),
            sentence,
            count=count,
        )
    return sentence.split("|")
