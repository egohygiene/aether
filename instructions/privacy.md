# Local Agent Privacy Rules

- Never commit raw Mindcap archives, browser profiles, cookies, session tokens,
  credentials, private keys, or secrets.
- The ChatGPT browser profile belongs outside the repository under the configured
  Mindcap data directory. Do not copy it into `.cache/` or an archive bundle.
- Consider captured conversations and Mindgarden notes private unless their
  sensitivity metadata explicitly says otherwise.
- Redact secret-like material before derived artifacts are persisted.
- Preserve sensitivity classification through source, knowledge, synapse, and
  gardenized outputs.
- Disable external sharing by default. Ask before sending private material to a
  remote model, website, issue tracker, or other service.
- Provenance may identify a private source segment without reproducing the
  protected payload.
- Never fabricate citations, quotes, coverage, or confidence.
