# Rollback Standard

- Revert extraction commit/PR when repo validation fails.
- Roll back runtime to prior known-good release/tag for service failures.
- Restore last-known-good contract versions on compatibility drift.
- Use tested DB restore path for migration incidents.
- Keep monorepo authority until extracted repo passes parity and deployment gates.
