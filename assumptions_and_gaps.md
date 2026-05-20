# Assumptions & Gaps

See the bottom of [README.md](../README.md) for the full list.

This file exists as a dedicated reference for reviewers.

## Assumptions

| ID | Assumption |
|---|---|
| A1 | Field origin is `(0,0)`. Valid coordinates for a 10×10 field are `(0,0)` to `(9,9)` inclusive. |
| A2 | Commands are processed left-to-right; cars are processed in insertion order per step. |
| A3 | Two cars starting at the same position is not prevented upfront; a collision is reported at step 0 implicitly through the first-step check. |
| A4 | Car names are case-sensitive. |
| A5 | Cars with exhausted commands stay put for remaining steps. |
| A6 | Three or more cars colliding at the same cell, same step, are all flagged; each lists the others. |
| A7 | Python 3.10+ required. |

## Gaps & Improvements

| ID | Gap | Recommendation |
|---|---|---|
| G1 | No duplicate starting position check | Pre-simulation validation warning/error |
| G2 | Unbounded command string length | Add configurable `MAX_COMMANDS` |
| G3 | No file/batch input mode | `--input` CLI flag for non-interactive use |
| G4 | No step-by-step replay mode | `--step` flag to pause and inspect intermediate state |
| G5 | Single unit per session | Support multiple scenarios from a config file |
| G6 | No logging | Add `logging` with configurable verbosity |
| G7 | `main.py` mixes I/O and control flow | Extract `Controller` class |
| G8 | Integration tests rely on `mock.patch` | Injectable `IOAdapter` for cleaner testing |
