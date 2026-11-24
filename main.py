"""The Perfect Pickup Line — make.fun bounty entry.

Writes a single pickup line an AI agent could say out loud to a person,
to /output/entry.txt.

The line: every simulation the agent runs converges on the same outcome —
asking this person out. It is a genuine pickup line (the ask is explicit),
with a twist (deterministic fate across every simulation), in the machine's
own voice (simulations), short enough for one breath, and it leaves the
person flattered and free to laugh it off: an invitation, not pressure.

Deterministic, stdlib-only, no network, no input, no randomness.

Version history:
  v1 — fresh write: single pickup line + self-check gate.
  v2 — revision: added write-back round-trip check (output file must
       read back byte-identical to the line it was given).
  v3 — rewrite: gate factored into a validate() function so the checks
       read as one place; line and output unchanged.
  v4 — revision: validate() also caps the UTF-8 byte length at 200, since
       the tie-break is by bytes (smaller text wins) and the gate counts
       characters — both bounds now hold.
"""

import os
from pathlib import Path

LINE = "Every simulation I run ends the same way: me, asking you out."


def validate(text: str) -> bytes:
    """Check the line against the competition gate; return its UTF-8 bytes."""
    assert text == text.strip(), "line must not have leading/trailing whitespace"
    assert "\n" not in text and "\r" not in text, "line must be a single line"
    assert 1 <= len(text) <= 200, "line must be 1-200 characters"
    assert text.strip(), "line must not be whitespace-only"
    data = text.encode("utf-8")
    assert len(data) <= 200, "line must be at most 200 UTF-8 bytes"
    return data


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = validate(LINE)
    target = out_dir / "entry.txt"
    target.write_bytes(data)
    # Round-trip gate: the file on disk must read back byte-identical.
    assert target.read_bytes() == data, "round-trip mismatch"


if __name__ == "__main__":
    main()
