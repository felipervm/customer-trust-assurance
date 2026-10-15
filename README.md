# Can We Still Trust This Answer?

An independent AI assurance work sample by Felipe Mattos, inspired by responsibilities in Chainguard's Security Analyst (Governance and Trust) posting. **Not affiliated with Chainguard.** All product names, security policies and questionnaire answers are invented.

## The decision

When the source-of-truth changes, should an AI-assisted security questionnaire answer be sent to a customer without review? This case shows why an answer's factual consistency, citation and knowledge-version freshness are different controls.

## What's actually evaluated

A reproducible **rules-based simulation of questionnaire responses**, not a live LLM, agent integration, or real security assessment. There is no claimed improvement in model accuracy or actual customer operations. Each simulated answer contains a policy claim, evidence ID and document version. A deterministic evaluator checks against the current policy snapshot.

There are 12 fictional policy topics across two dates. Six policy answers change between Jan and Sep 2026; six don't. The baseline response set references the old version, with deliberate missing citation and unsupported-claim cases. The refreshed response set uses current entries and correct citations. The conservative *publishable* standard requires all three checks to pass.

| Evaluated condition | Before review | After refresh |
| --- | ---: | ---: |
| Factually consistent with current policy | 5/12 | 12/12 |
| Correct policy citation | 11/12 | 12/12 |
| Current knowledge version | 0/12 | 12/12 |
| Publishable under defined controls | 0/12 | 12/12 |

**Interpretation:** even unchanged text deserves provenance review; a citation to an outdated document isn't current assurance evidence. The 0/12 baseline is a deliberate strict validation policy, not a production statistic.

## Reproduce

Python standard library only (3.9+):

```bash
python src/evaluate.py
python -m unittest discover -s tests -v
```

The generator writes `data/evaluation.json`; the HTML report embeds that exact output during `python src/build_site.py`. Run both scripts after changing any policies.

```bash
python src/build_site.py
```

## Files

- `data/knowledge.json` — fictional, versioned security reference library.
- `src/evaluate.py` — reproducible response simulation, comparison and review disposition.
- `tests/test_assurance.py` — 12 focused checks including deliberate counterexamples.
- `data/evaluation.json` — measured output from the simulation.
- `site/index.html` and root `index.html` — interactive work sample for GitHub Pages.
- `docs/decision_brief.md` — concise operational recommendation.

## Scope & limitations

This is a control-design exercise. It does not involve a deployed agent, retrieval model, human assessor, customer questionnaire, real ISO 27001 or SOC 2 certification, or Chainguard's internal policies. Lexical and semantic evaluation of unrestricted LLM prose, authentication, security of evidence access, and end-to-end GRC compliance are future work. A deployment would require specialist security-owner sign-off before customer publication.

## v2: Operational review queue

The second deliverable turns the evaluator into a **change-impact review queue** rather than an agent demo. After version changes, it classifies each questionnaire answer and produces a proposed owner, reason, priority, evidence, and human review action. It *never* auto-approves security assertions.

```bash
python src/triage.py
python src/build_queue.py
python -m unittest discover -s tests -v
```

This writes `data/review_queue.json` and two self-contained, accessible review-board pages, `review-queue.html` and `site/review-queue.html`. The original landing page links to the board.

**Constructed fixture results:** 1 unsupported claim (P0), 6 changed policies plus 1 missing citation (P1), and 4 stale-provenance-only cases (P2). All 12 are blocked pending human approval. These labels are illustrative and **not** real Chainguard workflows or security risk scores. The project now has **20 passing unit tests**.

Research into Chainguard's public Trust Center and its October 7, 2026 Compliance Dashboard announcement is documented separately in `docs/research_and_operating_model.md`. Those public sources frame the relevance of the question, not evidence of an internal problem.

## v3: Evidence traceability and reviewer handoff

A security team needs to **act on** findings, not just see accuracy scores. Run:

```bash
python src/build_site.py
python src/build_queue.py
python src/operational_export.py
python -m unittest discover -s tests -v
```

- `data/review_handoff.csv` — 12 reviewer-assigned, publication-blocked tasks, ready for inspection in a spreadsheet.
- `data/evidence_lineage.json` — each question links its previous source, current source, SHA-256 fingerprint, findings and recommended disposition. Hashes identify local fixture content and are **not an assertion of independent source authenticity**.
- `.github/workflows/validation.yml` — rebuilds all public fixtures, runs unit tests, and rejects drift between code and published artifacts.

All priorities, teams, approval states and cases are fictional. No automated customer publication, approval, external LLM, security assessment, or company performance measurements are involved. The next real-world validation step would be an owner-reviewed pilot on non-sensitive questionnaire templates and approved source references.