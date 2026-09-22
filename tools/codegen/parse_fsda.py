"""Parse FSDA toolbox metadata into an intermediate representation.

See docs/DESIGN-codegen-parser.md for the full specification.
Specs 022, 023, 024 define the individual components.
"""

import argparse
from pathlib import Path
import json
import logging


def enumerate_toolbox(fsda_root: Path) -> list:
    """Walk the FSDA toolbox tree and return the function inventory.

    Discovers Contents.m files per subfolder, records functionSignatures.json
    paths where they exist, and excludes private/ directories.
    Does not open JSON files. See Spec 022.
    """
    raise NotImplementedError


def parse_json_signatures(json_path: Path) -> dict:
    """Parse a single functionSignatures.json, preserving duplicate keys.

    Returns all signatures grouped by function name. Keys starting
    with _ are excluded. See Spec 023.
    """
    def multikeys_hook(pairs):
        d = {}
        # Track keys that we have explicitly converted into a list of duplicates
        dupes = set()
        
        for k, v in pairs:
            if k in d:
                # If we already marked this key as a duplicate, just append
                if k in dupes:
                    d[k].append(v)
                # Otherwise, wrap the existing value and the new one in a new list
                else:
                    d[k] = [d[k], v]
                    dupes.add(k)
            else:
                d[k] = v
        return d

    with open(json_path, 'r', encoding='utf-8') as f:
        raw_data = json.loads(f.read(), object_pairs_hook=multikeys_hook)

    # Filter out system keys and normalize every function entry to a list
    return {
        key: (value if isinstance(value, list) else [value])
        for key, value in raw_data.items()
        if not key.startswith('_')
    }


def extract_m_prose(m_path: Path) -> dict:
    """Extract prose from a single .m file's preamble.

    Returns long description, per-parameter descriptions, outputs,
    see-also references, and citations. See Spec 024.
    """
    raise NotImplementedError


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse FSDA metadata into an intermediate representation.",
    )
    parser.add_argument(
        "--fsda-root",
        type=Path,
        required=True,
        help="Path to the FSDA toolbox root directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("IntRep.json"),
        help="Where should the output be written (default: ./IntRep.json)",
    )
    args = parser.parse_args()
