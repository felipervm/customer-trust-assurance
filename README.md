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

**Constructed fixture results:** 1 unsupported claim (P0), 6 changed policies plus 1 missing citation (P1), and 4 stale-provenance-only cases (P2). All 12 are blocked pending human approval. These labels are illustrative and **not** real Chainguard workflows or security risk scores. The automated tests cover the assurance checks, triage decisions and operational exports.

Public company context and the proposed operating model are documented in `docs/research_and_operating_model.md`. This exercise follows the supplied role responsibilities; it does not establish any internal company problem.

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
## Presentation redesign

The presentation now follows the operational decision: inspect a source change, separate four review patterns, and follow the evidence into a reviewer handoff. The opening artwork is an original HTML/CSS diagram inspired by the editorial composition of TWKS and Chainguard's violet/black palette. It is not a company product screenshot.

The landing page includes four representative cases, stale/refreshed fixture comparison, three independent checks, an all-12-topic selector, and a persistent human-review gate. Queue category links open the corresponding reason filter. The full board retains all priority filters and source/action details; every item remains publication-blocked.

Edit `site/template.html`, `site/styles.css` and `site/app.js` for the landing page. The board uses `site/queue-template.html`, `site/queue-theme.css` and `site/queue-app.js`. Run `python src/build_site.py` and `python src/build_queue.py` after presentation changes. Both root and `/site/` pages embed their assets and data and remain byte-identical, with no external runtime dependencies. Do not edit generated HTML directly.

The supplied author portrait is stored at `site/assets/felipe-mattos.jpg`. `docs/application_notes.md` maps the supplied role to actual repository evidence and offers an application snippet and interview walkthrough. It does not imply prior employment, production agent maintenance or real customer outcomes.

Presentation tests additionally check payload/source agreement, exact rebuilds, local link targets and safe JSON embedding. Existing assurance, triage and export tests remain in place. Refreshed fixtures passing the three defined checks still require human security-owner approval; they are not authorized customer responses.

## Further presentation refinement

The landing page now includes original ImageGen concept artwork, locally embedded Manrope typography, a source-to-answer scroll story and additional interactive explanations. The copy uses natural questions and short first-person explanations while retaining the rules-based simulation boundary. Asset provenance and the full generation prompt are documented in `docs/visual_direction.md`.

The image and font are built from `site/assets/trust-records.jpg` and `site/assets/fonts/manrope-latin.woff2`; their data URIs are embedded alongside the author portrait, CSS, JavaScript and fixture JSON. Both published entry points still rebuild identically. The research model, review-queue classifications and mandatory human approval boundary remain authoritative.
