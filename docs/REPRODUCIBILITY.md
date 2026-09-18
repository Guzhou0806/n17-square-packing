# Reproducing M19

## Environment and trust boundary

The main entry point requires Python 3.10 or newer and only the standard library.
It launches frozen programs with `-B -S`, UTF-8 mode and assertions enabled.
The driver rejects optimized execution. No original workspace, online lookup,
model access, optimizer, or credential is needed.

The adapter is newly added packaging code. It is not a third geometric algorithm.
The original standard-library sweep and the different retained upstream NumPy
sweep remain separately attributable. All input files are immutable in this
snapshot; outputs go to a **new** directory outside frozen evidence.

## A. Quick check — no coverage recomputation

```bash
python -X utf8 -B verify.py --quick --output .replay-runs/quick-001
```

Checks the new evidence manifest, both original manifests, the final-acceptance
bindings, all saved witness counts and the exact M19 arithmetic. Expected status:
`PASS_QUICK_CHECK_ONLY`. This mode performs zero full-center coverage sweeps.

## B. Full standard-library replay — default

```bash
python -X utf8 -B verify.py --output .replay-runs/full-001
```

It performs the following, in order:

1. Integrity and acceptance-binding checks before execution.
2. Nested M12 replay: all 181 old directions, geometric/static fixtures, the
   1,184-atom scaling binding, and comparison with saved source/scaled outputs.
3. Original M19 replay: complete center-domain sweeps for all 17 M17 trial
   directions (16 passes and one expected failure), then exact 197-node and
   endpoint checks.
4. Comparison of all 198 fresh direction records with the supplied records and
   of the fresh M19 audit bytes with the hash named by final acceptance.
5. Integrity checks again after execution.

Expected status: `PASS_FULL_REPLAY`.

The console includes `FAIL_FIXED_REFINED_NET_COVERAGE` in the **M17** child log.
This is intentional: it is the retained counterexample to a different experiment.
The wrapper only passes when that expected failure and the valid M19 subset both
match. A process timeout or incomplete direction set is never interpreted as a
mathematical success.

Outputs include `RESULT.json`, `M12/coverage/DIRECTIONS.jsonl`,
`M19/new_coverage/DIRECTIONS.jsonl`, `M19/M19_AUDIT.json`, and execution logs.

## C. Optional second-implementation replay

The pinned upstream `model.py` and `sweep.py` are already bundled. Only NumPy is
optional. In a separate environment with NumPy available, run:

```bash
python -X utf8 -B scripts/source_crosscheck.py --output .replay-runs/source-001
```

Do not add `-S` to this optional command: it needs to import NumPy.
The release's optional environment specification is `requirements-optional.txt`.
Installing it is an explicit user action; no replay command installs anything.

The adapter installs namespace packages to avoid unrelated upstream initialization,
then calls the **unchanged** retained integer two-dimensional difference sweep on
all 181 old plus 17 M17 directions. It compares exact minima, independently recounts
each returned witness, and checks legal centers. Expected status:
`PASS_SOURCE_CROSSCHECK_198`.

This adapter records the actual NumPy version. It does not claim to recreate the
original project's NumPy 2.5.3 environment. The two algorithms still share the
underlying covering theorem, so agreement is not a substitute for reviewing that
theorem.

## Tests and repeatability

```bash
python -X utf8 -B -S -m unittest discover -s tests -v
```

Those tests check the release adapter, byte preservation and refusal behavior;
they do not independently establish universal geometric coverage.
Use a different output directory for every replay. Do not remove old reports just
to rerun the same command.

The programs have historical limits: M12 checks a 600-second budget between
directions; M17 uses a 120-second limit. The wrapper has a 750-second subprocess
limit. On a sufficiently slow machine this may fail as incomplete. Do not change
frozen code or call partial output a certificate; document any separate budget-only
adapter before using it.

## Publication scope

The recorded acceptance is the originating project's result. Fresh execution in
this release is a reproducibility check, not an expert endorsement, formal-kernel
proof, priority search, or proof of an optimal packing. The interval in the README
bounds $S_{19}$, not $s(17)$.
