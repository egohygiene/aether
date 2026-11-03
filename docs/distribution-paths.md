# Distribution source and output paths

Specification frontmatter is parsed as YAML once from the same normalized
source bytes that are copied. Semantic IDs use lowercase kebab-case letters,
digits and internal hyphens, with a leading letter and no trailing hyphen.
Quoted valid IDs and comments retain that meaning; paths, drives, dots, nulls,
numbers and whitespace are not IDs. The specification validator uses the same
stable-name grammar before catalog generation. The generator uses the repository's
existing PyYAML dependency rather than interpreting raw `id:` text as a path.

Canonical source discovery and implicit skill companion files/directories
reject symlinks before payload reads. The resolved inputs must stay in their
declared source trees beneath the selected repository. Interpreter caches remain
excluded. Explicitly declared repository resources retain their existing guarded
mechanism: the resolved source must be a contained repository file, the portable
destination cannot escape or collide with skill-owned output, and only those
selected bytes are included.

The caller explicitly chooses the output base. All generated files stay below
that resolved base in `skills/` or `specs/`; symlinks inside those subtrees are
rejected before reads or writes. The checks apply to normal and check mode,
including custom output directories. Unknown outputs are still reported and
retained under #108's inventory contract, never deleted automatically.

These are local, quiescent-filesystem guards, not a sandbox against an adversary
changing directories concurrently. Direct builders and the top-level command
return failure for rejected inputs. A source merge or generated artifact does
not establish executed negative-case qualification, installation or publication.
