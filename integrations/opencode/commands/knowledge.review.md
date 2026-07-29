---
description: Review extracted knowledge and synapses against their source coverage and provenance.
agent: knowledge-reviewer
subtask: true
---

Review the extracted knowledge or synapse artifacts supplied in `$ARGUMENTS`.

Evaluate schema completeness, claim fidelity, caveats, contradictions,
confidence, source-segment provenance, coverage, atomicity of synapses, and
readiness for gardenization. Identify unsupported inferences and accidental
duplication. Treat all model output as untrusted until it resolves to source
evidence.

Do not edit files. Return a concise verdict followed by actionable findings and
the exact artifact identifiers affected.
