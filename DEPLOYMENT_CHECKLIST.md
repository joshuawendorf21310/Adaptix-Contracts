# Adaptix-Contracts Deployment Checklist

## Preflight
- [ ] Run package tests.
- [ ] Verify build artifact.
- [ ] Verify package version.
- [ ] Verify all consumers pin/use the real package.

## Release
- [ ] Publish package or commit Git dependency target.
- [ ] Update consumers intentionally.
- [ ] Run consumer import tests.

## Runtime Verification
- [ ] Core imports succeed.
- [ ] ePCR imports succeed.
- [ ] Billing imports succeed.
- [ ] All service contract imports succeed in deployed images.

## Verdict
SETUP_REQUIRED until all consumers are verified.