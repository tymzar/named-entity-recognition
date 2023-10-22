from typing import TypeAlias
from collections.abc import Sequence

PreFormatDataset: TypeAlias = Sequence[tuple[str, Sequence[tuple[int, int, str]], bool]]
SpacyDataset: TypeAlias = tuple[str, Sequence[tuple[int, int, str, str]]]
