# Packaging-time reproduction report

This report records work actually executed while assembling this release. It is
separate from the originating project's [final acceptance](../evidence/M19/FINAL_ACCEPTANCE.json).
The original evidence was not edited to make the run pass.

## Completed checks

| Check | Outcome | Scope |
|---|---|---|
| Uploaded/extracted evidence | PASS | 129 M19 files preserved byte-for-byte; separate M12's 57 files equal the nested copy |
| Quick mode | `PASS_QUICK_CHECK_ONLY` | Hashes, accepted bindings, saved witnesses and arithmetic only |
| Full standard-library mode | `PASS_FULL_REPLAY` | Fresh complete-center sweeps for 181 old + 17 M17 directions |
| Retained-source NumPy mode | `PASS_SOURCE_CROSSCHECK_198` | Fresh second-implementation sweeps for all 198 directions and 198 direct witness recounts |
| Release/refusal tests | 15 / 15 PASS | Tampering, unsafe paths, duplicate JSON keys, protected outputs, `-O` refusal and archive equivalence |

The standard-library run took **40.33 seconds** in this packaging environment;
the optional NumPy run took **39.93 seconds**. These are observations from
this machine, not promised runtimes on another computer.

The actual software versions were **Python 3.13.5** and
**NumPy 2.3.5**. The historical project recorded a different NumPy
environment; it is preserved but not claimed to have been recreated.

The 198 direction computations contain **197 directions used by M19 and one
intentional M17 failure**. The failed direction has mass `197153/200000` and its
direct witness captures 125 atoms. The accepted directions have common lower
guarantee `200009/200000`. The fresh M19 audit is byte-identical to the report
bound by the supplied final acceptance.

A separate throwaway Git-index test staged all 131 frozen evidence/archive files
with `core.autocrlf=true`; all staged bytes remained unchanged under the supplied
`.gitattributes`. This was a local test, not a commit or remote push.

## Read the actual outputs

- [Machine-readable assembly summary](PACKAGING_REPORT.json)
- [Full standard-library result](standard_library/RESULT.json)
- [181 fresh old-direction rows](standard_library/M12/coverage/DIRECTIONS.jsonl)
- [17 fresh M17 rows](standard_library/M19/new_coverage/DIRECTIONS.jsonl)
- [Fresh exact M19 audit](standard_library/M19/M19_AUDIT.json)
- [Second-implementation result](source_numpy/RESULT.json)
- [198 fresh source-direction rows](source_numpy/DIRECTIONS.jsonl)
- [Unit/refusal test log](release_tests.log)
- [Local Git-index byte-preservation test](GIT_INDEX_CHECK.json)

## What this does not establish

Re-execution of two supplied algorithms is stronger evidence than repeating an old
PASS label, but it is not a separately authored third geometry verifier, a formal
proof-assistant check, or an external expert review. Both algorithms rely on the
covering argument explained in the proof. No priority search or world-record
claim is part of this release. M20 is outside its scope.

A limited credential-pattern scan found no matches in the retained evidence; this
is not a guarantee against every possible secret or personal identifier. Historical
local path strings remain where required by preserved reports. No GitHub repository
was created, no content was pushed, and no hosted Actions run was executed here.

Fresh execution logs retain their true local output paths; these are records, not
input requirements. All reproduction entry points locate inputs relative to the
extracted repository.
