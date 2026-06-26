from __future__ import annotations

from dataclasses import dataclass

from .config import config


@dataclass(slots=True)
class BuildContext:
    config = config