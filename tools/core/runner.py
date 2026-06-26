from __future__ import annotations

from .builder import Builder
from .extractor import CoverExtractor
from .logger import get_logger
from .parser import Parser
from .scanner import Scanner
from .writer import Writer


class BuildRunner:

    def run(self) -> None:

        logger = get_logger()

        logger.info("====================================")
        logger.info("ComicReader Builder")
        logger.info("====================================")

        scanner = Scanner()
        parser = Parser()
        extractor = CoverExtractor()
        builder = Builder()
        writer = Writer()

        comics = scanner.scan()

        logger.info(f"Found {len(comics)} comic(s).")

        parsed = []

        success = 0
        failed = 0

        for comic in comics:

            try:

                metadata = parser.parse(comic)

                extractor.extract(
                    comic,
                    metadata,
                )

                parsed.append(metadata)

                success += 1

                logger.info(
                    f"[OK] {metadata.uid} | {metadata.title}"
                )

            except Exception as exc:

                failed += 1

                logger.exception(
                    f"[FAILED] {comic.filename}\n{exc}"
                )

        library = builder.build(parsed)

        writer.write_library(library)

        logger.info("")
        logger.info("====================================")
        logger.info("Build Complete")
        logger.info("====================================")
        logger.info(f"Success : {success}")
        logger.info(f"Failed  : {failed}")
        logger.info(f"Output  : data/library.json")
        logger.info(f"Covers  : covers/")