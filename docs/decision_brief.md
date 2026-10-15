# Decision brief — When a security source changes, what needs review?

**Felipe Mattos · Independent work sample · 15 October 2026**

### The business question

A customer asks for a security answer. The approved source has changed since the answer was drafted. Does the assurance team need to rewrite it, verify its evidence, or block it for investigation? An AI assistant should not make that decision alone.

### Why I chose this question

Chainguard already operates a Trust Center, and on October 7, 2026 announced its Compliance Dashboard with more directly accessible, digest-specific compliance evidence. Its Governance & Trust job description emphasizes accurate questionnaire content and AI-agent maintenance. Those are public observations, not proof of internal inefficiencies.

### What I tested

I built a fully fictional 12-policy questionnaire corpus with two versions, then evaluated stale example answers and generated a review queue with source references, reasons, proposed owners and next actions. The evaluation is deterministic; no real LLM was used.

### What the simulated queue showed

- **1 unsupported claim:** block and escalate.
- **6 changed policies:** rewrite against the current source and ask the security owner to approve.
- **1 missing citation:** repair the evidence and ask the owner to verify.
- **4 unchanged claims with stale provenance:** refresh the source record and obtain confirmation.

All **12/12** baseline answers remain blocked pending security-owner review; **20/20** automated tests pass. These are results from deliberately constructed fixtures, not customer incident counts, operational savings or AI-model benchmarks.

### Recommendation

Maintain a source-to-answer map, invalidate affected answers when an authoritative reference changes, and route each exception based on whether it is a factual conflict, an evidence gap or only a provenance refresh. Record reviewer decisions and never let an AI-generated response approve its own release.

### What I'd validate with a real team

The volume and types of actual documentation changes, reviewer sign-off criteria, false-positive rate for change impact, and whether reviewers consider the queue helpful. I would only measure time saved after establishing a real baseline with permissioned workflow data.

**Research and limitations:** [See the research and operating model](research_and_operating_model.md). All policy content in the demo is fictitious and is not a claim about Chainguard.