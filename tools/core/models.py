from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ComicFile:
    filename: str
    filepath: Path
    filesize: int
    modified: float


@dataclass(slots=True)
class ComicMetadata:

    uid: int

    filename: str

    filepath: str

    english_title: str = ""

    japanese_title: str = ""

    title: str = ""

    series: str = ""

    translator: str = ""

    format: str = ""

    language: str = ""

    page_count: int = 0

    favorites: int = 0

    upload_date: int = 0

    year: int = 0

    month: int = 0

    day: int = 0

    web: str = ""

    tags: list[str] = field(default_factory=list)

    parody: list[str] = field(default_factory=list)

    category: list[str] = field(default_factory=list)

    artists: list[str] = field(default_factory=list)