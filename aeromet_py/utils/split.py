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
    sentence: str, keywords: List[str], count: int = 0, space: str = ""
) -> List[str]:
    """Split the `sentence` given by the list of `keywords` without
    lost that keywords.

    Args:
        sentence (str): the sentence to split.
        keywords (List[str]): the list of keywords where the sentence will be splitted.
        count (int, optional): Number of splits of every coincidence. Defaults to 0.
        space (str, optional): take spaces in count to the left or right of every word.
            Defaults to ''. Options: `left`, `right`, `both`

    Returns:
        List[str, str]: the list of sentence splitted from the original.
    """
    for kw in keywords:
        if space == "left":
            kw = _add_space_left(kw)
        elif space == "right":
            kw = _add_space_right(kw)
        elif space == "both":
            kw = _add_space_both(kw)
        else:
            pass

        pattern = re.compile(kw)
        sentence = re.sub(
            pattern,
            "|" + kw.lstrip(),
            sentence,
            count=count,
        )
    return sentence.split("|")
