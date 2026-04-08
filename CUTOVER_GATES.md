# Cutover Gates

Gate A — Extraction readiness
- ownership mapped
- dependencies mapped
- rollback written
- baseline captured

Gate B — Repo validity
- builds independently
- tests independently
- env contract documented
- no private path imports

Gate C — Functional parity
- critical workflows verified
- auth works
- event flow works
- observability present

Gate D — Authority transfer
- release tag exists
- rollback drill completed
- compatibility pinned

Gate E — Legacy retirement
- two successful independent deploys
- old path deprecated
- duplicate contracts removed
