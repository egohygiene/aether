# Review and export safety

## 1. Prepare a draft

Run `prepare`. Review the packet's Identity lock, catalog lock, selected
surfaces, copied provenance, copy, claims, links, attribution, and unknown
constraints.

## 2. Record freshness verification

Consequential or production handoff requires a current check of the linked
official sources:

```bash
python3 scripts/campaign-handoff.py record-freshness \
  --packet "campaign-handoff.json" \
  --verified-by "reviewer-id" \
  --verified-at "2026-08-29T12:00:00Z" \
  --evidence "https://example.invalid/review/freshness" \
  --output "campaign-handoff.fresh.json"
```

This command records evidence; it does not fetch or rewrite the catalog.

## 3. Complete checklist evidence

Complete one item at a time while the packet is `draft` or `reviewed`:

```bash
python3 scripts/campaign-handoff.py complete-check \
  --packet "campaign-handoff.fresh.json" \
  --check-id "copy-and-claims" \
  --completed-by "reviewer-id" \
  --completed-at "2026-08-29T12:10:00Z" \
  --evidence "https://example.invalid/review/copy" \
  --output "campaign-handoff.checked.json"
```

Do not mark a check complete without inspectable evidence.

## 4. Record review

```bash
python3 scripts/campaign-handoff.py transition \
  --packet "campaign-handoff.checked.json" \
  --to-state "reviewed" \
  --actor "reviewer-id" \
  --occurred-at "2026-08-29T12:20:00Z" \
  --reason "Human review completed; export approval remains pending." \
  --review-notes "Reviewed every selected channel and candidate claim." \
  --output "campaign-handoff.reviewed.json"
```

Compute the reviewed digest:

```bash
python3 scripts/campaign-handoff.py digest \
  --packet "campaign-handoff.reviewed.json"
```

## 5. Approve the exact reviewed packet for export

Create a separate approval record based on the template documented by the
contract. Its `reviewed_packet_digest` must equal the previous command's value.
Then run:

```bash
python3 scripts/campaign-handoff.py transition \
  --packet "campaign-handoff.reviewed.json" \
  --to-state "approved-for-export" \
  --actor "approver-id" \
  --occurred-at "2026-08-29T12:30:00Z" \
  --reason "Exact reviewed packet approved for immutable export." \
  --approval-record "campaign-approval.json" \
  --output "campaign-handoff.approved.json"
```

Approval changes copy and claim status only because the approval is bound to
the exact reviewed packet. It grants `immutable-export-only` authority.

## 6. Export, publish, or supersede

An approved packet may be handed to a separate adapter. This skill does not
accept credentials and refuses `--to-state "published"`. A publishing adapter
must preserve the packet, operate under its own authorization, and append a
receipt before the packet can validate as `published`.

To withdraw or replace a packet:

```bash
python3 scripts/campaign-handoff.py transition \
  --packet "campaign-handoff.approved.json" \
  --to-state "superseded" \
  --actor "reviewer-id" \
  --occurred-at "2026-08-29T13:00:00Z" \
  --reason "Replaced after a catalog or campaign revision." \
  --superseded-by "campaign/replacement" \
  --output "campaign-handoff.superseded.json"
```
