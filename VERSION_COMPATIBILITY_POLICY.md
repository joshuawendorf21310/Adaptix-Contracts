# Contracts Version Compatibility Policy

## Overview

`adaptix-contracts` uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
All cross-repo integrations MUST declare their supported version range explicitly.

## Versioning Rules

| Bump | Meaning | Action Required |
|------|---------|----------------|
| PATCH (0.1.x) | Bug fix only | None — fully backward-compatible |
| MINOR (0.x.0) | Additive (new fields, events) | Optional — new fields are ignored by existing consumers |
| MAJOR (x.0.0) | Breaking change | **Required** — see `BREAKING_CHANGES.md` |

## How Downstream Repos Declare Compatibility

Every consuming repo MUST declare a supported range in its `contracts.json`:

```json
{
  "repo": "adaptix-your-repo",
  "min_contract_version": "0.1.1",
  "max_contract_version": "0.2.x",
  "event_types": ["incident.created", "epcr.signed"]
}
```

At application startup, validate with:

```python
from adaptix_contracts.compat import DownstreamDeclaration

dec = DownstreamDeclaration.from_json_file("contracts.json")
dec.assert_or_raise()  # Raises RuntimeError if installed version is outside range
```

## Wildcard Matching

- `"0.2.x"` matches any `0.2.*` version (patch-level flexibility).
- A missing `max_contract_version` is treated as unbounded — **not recommended**.

## Enforcement

- `COMPATIBILITY_MATRIX.json` in this repo tracks all consumer declarations.
- CI gates reject PRs that leave any declared consumer incompatible.
- The `validate_matrix()` helper checks all entries programmatically.

## Event Envelope Versioning

`EventEnvelope.envelope_version` is frozen at `"1.0"` for the entire 0.x series.
Consumers MUST reject envelopes with an unrecognised major envelope version.
`schema_version` inside the envelope increments independently per event type
when the payload shape changes.
