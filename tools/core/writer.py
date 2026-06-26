from __future__ import annotations

import json

from .config import config


class Writer:

    def write_library(self, library: dict):

        config.data_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output = config.data_dir / "library.json"

        with output.open(
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                library,
                fp,
                indent=2,
                ensure_ascii=False,
            )