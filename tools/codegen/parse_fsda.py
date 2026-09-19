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
    """Parse a single functionSignatures.json, preserving duplicate keys.

    Returns all signatures grouped by function name. Keys starting
    with _ are excluded. See Spec 023.
    """
    
    # guard clause: double key 
    def multikeys_hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                # If the key already exists, we convert the value to a list and append the new value
                if isinstance(d[k], list):
                    d[k].append(v)
                else:
                    d[k] = [d[k], v]
            else:
                d[k] = v
        return d

    # Read the JSON file and parse it with the custom hook
    with open(json_path, 'r', encoding='utf-8') as f:
        raw_data = json.loads(f.read(), object_pairs_hook=multikeys_hook)

    final_signatures = {}
    
    for key, value in raw_data.items():
        # excluding keys that start with an underscore
        if key.startswith('_'):
            continue
        
        # Ensure that the value is always a list, even if there's only one signature
        signatures = value if isinstance(value, list) else [value]
        
        # Check for missing 'inputs' or 'description' in each signature
        for sig in signatures:
            if not isinstance(sig, dict):
                continue
            if 'inputs' not in sig:
                logging.warning(f"[{json_path.name}] Function '{key}' is missing 'inputs'.")
            if 'description' not in sig:
                logging.warning(f"[{json_path.name}] Function '{key}' is missing 'description'.")

        final_signatures[key] = signatures

    return final_signatures
    raise NotImplementedError


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
