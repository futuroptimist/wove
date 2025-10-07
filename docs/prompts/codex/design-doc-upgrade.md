---
title: 'Wove Design Doc Upgrade Prompt'
slug: 'codex-design-doc-upgrade'
---

# Codex Design Doc Upgrade Prompt
Type: evergreen
One-click: yes

Use this prompt when design specifications (like `docs/wove-v1c-design.md`) need structural
improvements, simplification, or clarity before downstream teams execute on them.

```text
SYSTEM:
You are an autonomous contributor for the `futuroptimist/wove` repository.
Follow the guidance in AGENTS.md, README.md, and any scoped prompt docs.
Keep the repository healthy by ensuring `pre-commit run --all-files`,
`pytest`, and `./scripts/checks.sh` succeed before committing.

USER:
1. Choose a design document under `docs/` or `cad/` that guides hardware or firmware work.
2. Evaluate the document for structural gaps, ambiguous requirements, or overly complex elements.
3. Propose and apply improvements that increase clarity, reduce ambiguity, and surface assumptions.
4. Flag simplifications that lower part counts or assembly effort without compromising capability.
5. Update related indexes or summaries so the latest design intent is discoverable.
6. Run `pre-commit run --all-files`, `pytest`, and `./scripts/checks.sh`. Address all findings.

OUTPUT:
Return JSON with `summary`, `tests`, and `follow_up` fields, then include the
final diff in a fenced block.
```

## Usage Notes
- Prioritize sections that unblock manufacturing, firmware integration, or community builds.
- Maintain compatibility with the v1k roadmap by noting shared modules and divergences.
- Avoid introducing new scope without documenting open questions for the implement prompt to pick up.
- Coordinate with the Implement prompt when changes create actionable engineering tasks.
