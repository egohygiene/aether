# Cross-agent public evidence packets

This directory contains the deterministic reference importer and synthetic
fixtures for `aether.cross-agent-evidence-packet/v1`.

The importer validates local bytes only. It does not fetch immutable references,
execute source content, call a model, authorize a capability, or transport a
packet.

Validate the synthetic legal-source packet:

```bash
python3 catalog/evidence-packets/validate.py \
  --packet "catalog/evidence-packets/fixtures/legal-source-packet.json" \
  --attachments-root "catalog/evidence-packets/fixtures"
```

Validation establishes artifact integrity. Admission additionally fails closed
unless the caller supplies the destination, externally admitted policies, and
current session capabilities:

```bash
python3 catalog/evidence-packets/validate.py \
  --packet "catalog/evidence-packets/fixtures/legal-source-packet.json" \
  --attachments-root "catalog/evidence-packets/fixtures" \
  --admit \
  --destination "egohygiene/realm#25" \
  --admitted-policy-id "egohygiene/hygiene#39" \
  --session-capability "public-evidence-import"
```

Validate the separately reviewed outbound request:

```bash
python3 catalog/evidence-packets/validate.py \
  --request "catalog/evidence-packets/fixtures/sanitized-request.json"
```

Validate a transport projection against its packet:

```bash
python3 catalog/evidence-packets/validate.py \
  --projection "catalog/evidence-packets/fixtures/filesystem-projection.json" \
  --packet-for-projection "catalog/evidence-packets/fixtures/legal-source-packet.json"
```

Admission to a real destination still requires external policy and session
capability checks. A valid packet or projection never grants those capabilities.
