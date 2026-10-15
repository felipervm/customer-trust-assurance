# Using this work sample in a Governance and Trust application

This independent portfolio exercise maps to the Security Analyst (Governance and Trust) job description supplied for the application. All vendor policies, questionnaire answers, priorities and owner assignments are fictional. It demonstrates a small control design and review handoff, not experience operating Chainguard's systems or auditing a deployed AI agent.

## Evidence to lead with

| Responsibility in the supplied role | Repository evidence | Honest interpretation |
| --- | --- | --- |
| Maintain a current questionnaire response corpus | [Versioned knowledge library](../data/knowledge.json) | Twelve fictional topics across January and September 2026 illustrate how an answer depends on an approved source version. This is not a real questionnaire corpus. |
| Identify inconsistent or outdated customer-facing claims | [Evaluator](../src/evaluate.py), [evaluation output](../data/evaluation.json) | Separate structured claim consistency, citation ID and source freshness. The evaluator does not understand arbitrary prose or measure an LLM's accuracy. |
| Establish repeatable review and versioning processes | [Triage logic](../src/triage.py), [review queue](../data/review_queue.json), [decision brief](decision_brief.md) | Proposed owners and actions distinguish rewrites, missing evidence, stale provenance and escalation. All cases remain blocked pending human review. |
| Keep artifacts traceable and ready for handoff | [Lineage export](../data/evidence_lineage.json), [reviewer CSV](../data/review_handoff.csv), [export code](../src/operational_export.py) | Each finding carries previous/current references and a next action. SHA-256 fingerprints identify local fixture records; they do not authenticate an external policy or certification. |
| Evaluate agent behavior and prevent drift | [Counterexample tests](../tests/test_assurance.py), [triage tests](../tests/test_triage.py) | Controlled response fixtures let reviewers test maintenance rules. This is a foundation for a future agent evaluation process, not an agent integration or a production drift monitor. |
| Document changes, limitations and review outcomes | [Research and operating model](research_and_operating_model.md), [validation workflow](../.github/workflows/validation.yml) | Reproducible artifacts and drift checks help inspect the work. Actual human approvals, live documentation changes and customer publication are not implemented. |

## The hiring narrative

Lead with the operating decision: **When a source changes, identify which answers need rewriting, evidence repair or escalation before anything is shared externally.** The practical deliverable is the traceable review queue, not an accuracy headline.

The constructed baseline has six changed policies, one unsupported claim, one missing citation and four cases with unchanged claims but stale provenance. All twelve are blocked by the proposed review process. The refreshed fixtures pass the three defined evaluation checks; this does **not** constitute approval to publish. Every outgoing security assertion still requires an accountable security owner's review.

## Three-sentence application snippet

I created an independent assurance work sample using a fictional, versioned security-response corpus to explore what needs review when source information changes. The repository includes a deterministic evaluator, counterexample tests, and a change-impact queue with proposed owners, source lineage and a publication block pending human approval. I would welcome the opportunity to walk through one answer and discuss how I would adapt these controls to approved assurance content and maintained AI workflows with your Governance and Trust team.

Link the work sample alongside an accurate resume through the official application. This snippet describes project evidence, not previous employment, certifications or company access. No application or outreach was sent as part of this work.

## Interview walkthrough

1. **Start with a changed policy.** Open `AUTH-01`: SSO changes from all plans to Business and Enterprise. Show the old answer, the current source, the rewrite recommendation and the required owner approval.
2. **Show that freshness differs from truth.** Open `ENC-04`: the encryption claim is unchanged, but its provenance references a superseded version. Explain why the conservative rule asks for revalidation rather than an unnecessary factual rewrite.
3. **Challenge the answer, not just its citation.** Open `EXPORT-09`: a question about audit-log exports contains an invented ISO 27001 certification claim. A policy ID alone cannot support that unrelated assertion; the case is blocked and escalated.
4. **Explain the evidence gap.** Open `BACK-08`: the daily-backup claim still matches the fixture, but its citation is absent. Describe the evidence repair and review action.
5. **Hand off something actionable.** Inspect the CSV row, proposed owner and evidence lineage. Explain that the suggested owner must be verified with the real team and that local fingerprints do not prove authenticity.
6. **Discuss limits before extending.** The evaluator compares structured values, not unrestricted language. Describe what a specialist reviewer and a realistic regression set would need to establish before connecting an agent or trusting a publishing workflow.

## Questions for the team

- Which sources are authoritative, who owns them, and how are product or architecture changes communicated to assurance reviewers?
- How are approved response versions, exceptions and audience restrictions represented today?
- Which changes should invalidate every linked answer, and which can be revalidated without rewriting the text?
- What evidence and sign-off are required for customer publication? Who approves security, privacy and contractual claims?
- What agent regressions matter most: unsupported claims, omitted qualifications, wrong scope, stale references, or failures to abstain?
- How would the team review an instruction/prompt/reference update, compare it with a known version, and roll it back if evaluations regress?
- What false-positive rate and reviewer workload would make a pilot useful? Measure these on permissioned workflows before claiming time savings.

## Proposed next step — not implemented

Pilot the process on non-sensitive questionnaire templates and approved reference material with a security owner. Version the source corpus, retrieval configuration and agent instructions separately; record the evaluation set and release candidate. Include changed-policy, unchanged-policy, missing-evidence and unsupported-claim cases, plus cases requiring abstention. Compare candidate outputs against reviewed references, inspect disagreements and retain reviewer decisions. Require owner sign-off before release and define monitoring, rollback and access controls with the team.

The current repository does not connect an LLM, retrieval service, Trust Center, customer questionnaire platform or authenticated evidence store. It does not implement prompt releases, automated source fetching, model drift measurement, human approval persistence, customer publication, or a full GRC process. There is no claim of security certification, production assurance effectiveness, operational savings or measured model improvement.
