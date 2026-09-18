# Exact global lower bound s(17) >= 4.59000459

See PROOF.md for the complete argument and ATTRIBUTION.md for origin and changes.

Portable proof replay, Python 3.12+ standard library only, from any directory:

    python -X utf8 -B /path/to/M12_global_lower_bound/replay.py --output /new/output/directory

It reruns all 181 exact finite directions (about 33 seconds on the original host), verifies source/scaled output agreement, reruns independent geometric fixtures, and binds all 1184 scaled atoms. It does not run optimization or third-party code. Stored source-faithful runs used Python 3.12 and NumPy 2.5.3 with an explicitly recorded CPU-count API shim and one worker; see the retained T1 report. Their immutable source closure and environment lock are included as provenance, not required by portable replay.

The directory mirrors selected original workspace paths so the frozen independent audit resolves its inputs without edits. The independent code and all prior failure records are retained. No world-record or priority claim.
