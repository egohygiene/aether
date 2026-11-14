# Finding Classification Guide

Begin with evidence, not a preferred recommendation.

Severity describes consequence.

Confidence describes evidence strength.

A potentially critical issue may still have low confidence.

Capture strengths with the same specificity used for defects.

Normal audits produce reports only. Remediation requires separate
authorization.

## Machine dimensions

Keep the approved observation classification separate from finding `nature`.
The profile registry defines which natures a selected leaf can produce.

| Nature | Evidence boundary |
| --- | --- |
| `defect` | A confirmed defect needs an observed source/evidence reference. |
| `policy-conformance` | Explicit observed policy evidence is required; feature absence alone is insufficient. |
| `opportunity` | Useful proposed capability, with probable/needs-validation/needs-clarification status; no implied requirement. |
| `experimental-opportunity` | Explicit experimental profile; informational and recommended/unverified only. |
| `risk` / `clarification` | Preserve uncertainty, trade-offs and missing authority. |
| `positive-observation` | A specific strength is indexed by its finding ID; absence is explained. |

Every finding preserves exact source leaf ID/version, even if a composite was
requested. Do not silently combine overlapping findings and lose origin.
Severity describes consequence, impact describes potential effect, and neither
substitutes for confidence, evidence classification or actual execution.
Candidate issues remain suggestions; a reported delta or recommendation does
not grant remediation, issue creation or human acceptance authority.

New, unchanged, improved, regressed and resolved history are explicit authored
claims tied to known prior evidence. No missing row, later timestamp or unrun
check establishes resolution. Use unverified/not-compared when evidence is
missing; actual reported resolution still needs independent source review.
