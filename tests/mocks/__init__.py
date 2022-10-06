from dataclasses import dataclass


@dataclass
class ToVerifyCavok:
    code: str
    should_be: bool
