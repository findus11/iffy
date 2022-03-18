from typing import TypeVar

# self types soon plz
Self = TypeVar("Self", bound="Span")

class Span:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def __add__(self, other: Self) -> Self:
        start = min(self.start, other.start)
        end = max(self.end, other.end)
        return Span(start, end)
