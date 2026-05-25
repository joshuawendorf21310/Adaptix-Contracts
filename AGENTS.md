# LOCAL ADAPTIX REPO GOVERNANCE

This repository inherits global governance from:

Adaptix-Governance/AGENTS.md

## Local repo scope

Repo name: Adaptix-Contracts
Domain: Contracts
Owner service: adaptix-contracts

## Local execution rule

This repo must comply with:

- GLOBAL_EXECUTION_POLICY.md
- GLOBAL_CHANGE_CLASSIFICATION.md
- GLOBAL_NO_FAKE_SUCCESS_POLICY.md
- GLOBAL_PRODUCTION_READINESS.md
- GLOBAL_ROUTE_POLICY.md
- GLOBAL_SERVICE_POLICY.md
- GLOBAL_AUTH_POLICY.md
- GLOBAL_TENANT_POLICY.md
- GLOBAL_SCHEMA_POLICY.md
- GLOBAL_OBSERVABILITY_POLICY.md
- GLOBAL_SECURITY_POLICY.md
- GLOBAL_EVIDENCE_POLICY.md

## First rollout restriction

This local AGENTS.md file is governance inheritance only.

Do not modify production logic as part of this first rollout.

## Local override rule

Local rules may be stricter than global rules.

Local rules may never weaken global rules.

## Bedrock Remote Repair And Deployment Rule

All Bedrock audit, repair, validation, and deployment work must run through GitHub-hosted workflows and pull requests. Do not leave Bedrock-generated fixes, audit results, deployment changes, or conflict resolutions local-only. Every Bedrock-generated change must be pushed to a remote branch, checked for merge conflicts against main, validated by required CI/security checks, merged to main only after green checks, and deployed only through the approved AWS deployment workflow with recorded evidence. If a repository does not have the Bedrock workflow or required AWS/GitHub variables, report it as BLOCKED instead of claiming repair, deployment, or production readiness.
