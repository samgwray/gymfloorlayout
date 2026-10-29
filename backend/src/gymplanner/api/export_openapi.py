"""Write the OpenAPI document to a file: ``python -m gymplanner.api.export_openapi out.json``."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from gymplanner.api.app import create_app


def main(argv: list[str]) -> None:
    target = Path(argv[1] if len(argv) > 1 else "openapi.json")
    target.write_text(json.dumps(create_app().openapi(), indent=2) + "\n", encoding="utf-8")
    print(f"wrote {target}")


if __name__ == "__main__":
    main(sys.argv)
