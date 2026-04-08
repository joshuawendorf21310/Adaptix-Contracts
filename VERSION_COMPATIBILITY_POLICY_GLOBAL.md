# Version Compatibility Policy

- adaptix-contracts uses semantic versioning.
- Breaking interface changes require explicit version bump.
- Producers publish eventVersion on all cross-repo events.
- Consumers declare supported versions explicitly.
- Repositories pin compatible core/contracts versions; do not float to main.
