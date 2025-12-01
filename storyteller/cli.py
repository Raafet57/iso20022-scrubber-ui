from __future__ import annotations

import argparse
from pathlib import Path
from pprint import pprint

from parser import load_message
from narrative import generate_narrative


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Storyteller – ISO 20022 narrative generator (offline prototype)"
    )
    parser.add_argument("xml_file", type=Path, help="Path to ISO 20022 XML file")
    parser.add_argument(
        "--mode",
        choices=["narrative", "concise"],
        default="narrative",
        help="Narrative style",
    )
    args = parser.parse_args()

    payload = load_message(args.xml_file)
    story = generate_narrative(payload, mode=args.mode)

    print("=== Generated Narrative ===\n")
    print(story)
    print("\n=== Extracted Data ===\n")
    pprint(payload)


if __name__ == "__main__":
    main()
