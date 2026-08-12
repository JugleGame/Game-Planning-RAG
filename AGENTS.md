# RAG Card Repository Rules

This repository owns only research-card collection, validation, link auditing, retrieval, and search-mirror synchronization. Specification writing, Unity implementation, and QA adjudication belong elsewhere.

Markdown is the source of truth. Postgres/pgvector is a rebuildable mirror; never edit it by hand.

## Task routing

| Situation | Read or run |
|---|---|
| Scout research topics | `prompts/0_scout.md` |
| Research a card | `prompts/1_researcher.md` |
| Write a card | `prompts/2_writer.md` and one matching template |
| Validate a card | `prompts/3_validator.md` |
| Reflect a digest | `prompts/4_updater.md` |
| After merging a card | `python scripts/audit_links.py --for <ID>`; read `prompts/5_linker.md` only when findings require it |
| Audit repository links | `python scripts/audit_links.py`; fix `hard` findings and inspect `soft` findings in context |
| Find existing cards | `research/_index.md` → one relevant type index → at most two card bodies |
| Read the same section across cards | `python tools/read_section.py <cards> "<section title>"` |
| Find similar or counterexample cards | On a current mirror, `python tools/search_cards.py "<query>"`; narrow with `--kind` or `--section-key` |
| Check card format | One matching template and `card_schema.py`; never guess a section title |
| Check section splitting | `python scripts/check_sections.py` |
| Source an ARCH card | Read only the required section in `reference/unity_project_baseline_active.md` or `reference/qa_verification_policy_active.md`; Korean archives are for human source comparison only |
| Change retrieval | Run `python scripts/eval_retrieval.py` before and after |
| Recheck a translation | `python scripts/migrate_card_lang.py --verify <cards>` |

## Reading budget

1. Read only the prompt selected by the routing table for the current stage.
2. Open at most two existing card bodies per task. Prefer `search_cards.py` or `read_section.py` when possible.
3. Do not read all of `research/` at once. Listing files is allowed.
4. Do not read `db/`, `bridge/`, or `tools/*.py` source unless changing the mirror layer; use their CLIs normally.
5. `reference/*_active.md` files are English citation sources. Korean archives are neither execution instructions nor normal agent input.

## Card contract

- Write new titles, summaries, headings, and prose in English, preserving the selected template's exact section names and order.
- Mark facts with `[source: ..., as of YYYY-MM-DD]` and inference with `[interpretation]`.
- Keep required but unsupported sections as `<!-- No evidence: ... -->`.
- Check `research/_index.md` for duplicate IDs, then assign the next unused number for that type. Never edit generated `_index*.md` files by hand.
- Reference only exact registered IDs. Do not invent IDs or manually repair the database.
- Treat existing `research/signals/` files as append-only records.

## Validation and completion

Validate card changes in this order:

```powershell
python scripts/lint_card.py <changed-cards> --index research/_index.md
python scripts/check_sections.py
python scripts/audit_links.py --for <new-card-id>
```

After creating, deleting, renaming, or digest-reflecting cards, run M-stage in this exact order:

```powershell
python tools/build_index.py
python tools/sync_db.py
python tools/embed_cards.py
python tools/verify_db.py
```

- `embed_cards.py` reads synchronized `cards` and `card_sections`, so it must follow `sync_db.py`.
- Default `--transport auto` falls back from 5432 to the 443/HTTPS bridge. Report the transport used.
- Mirroring is complete only when `verify_db.py` reports `unresolved_refs: 0`.
- If DB access fails, preserve valid Markdown and report `card complete / mirroring failed (<reason>)`.
- Never use `tools/init_db.py` for mirroring or recovery; it drops tables.

## Change safety

- Apply only human-approved JSON through `scripts/apply_patch.py`.
- Do not automatically fix `soft` link-audit findings; they may describe deliberate comparisons or exclusions.
- Run M-stage only when card data changes. Documentation, prompts, templates, and tool changes do not require it.
- Commit or push only when the user asks or an active workflow explicitly requires it.
