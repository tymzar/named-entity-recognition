from typing import TypeAlias
from collections.abc import Sequence

PreSpacyDataset: TypeAlias = Sequence[tuple[str, Sequence[tuple[int, int, str, str]]]]
SpacyDataset: TypeAlias = tuple[str, Sequence[tuple[int, int, str, str]]]
