# Research context and operating model

This is an independent exercise prompted by Chainguard's **Security Analyst (Governance and Trust)** job description. The vacancy describes maintaining customer-facing security assurance answers, Trust Center materials and the prompts/reference content used by AI-enabled workflows. It also specifies regular audit, versioning and drift checks.

## Public context

- [Chainguard Trust Center](https://trust.chainguard.dev/) — public-facing security assurance materials and requests. Access and content may change.
- [Chainguard](https://www.chainguard.dev/) — public company and product context.

These links establish why the general workflow is relevant, **not** a finding that Chainguard has an outdated answer, missing review control or agent failure.

## Proposed decision flow

1. Version the approved source document and capture a stable reference identifier.
2. Find questionnaire responses linked to the changed topic.
3. Separate contradicted claims from missing citations and unchanged claims with stale provenance.
4. Create a human review ticket with previous/current evidence and a proposed accountable team.
5. Keep external publication blocked until a human security owner verifies and explicitly approves.
6. Preserve the previous answer, decision and source reference for follow-up audits.

## Prototype evidence

The implementation uses 12 fictitious policies, two document snapshots, deterministic simulated answers, a review queue and a CSV handoff. The policy examples, owner assignments, severity tiers and performance metrics are not Chainguard data. A content hash is a local integrity fingerprint, not independent verification of a real security claim. No customer content is transmitted to an LLM.

## Practical next step

A real pilot would require approved non-sensitive documents, a human GRC/security owner, clearly defined ownership and publication gates, and a sampled evaluation of both misses and unnecessary escalations before any workflow is used for customer assurances.
