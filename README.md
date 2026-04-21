# Adaptix Contracts

**Version:** 1.0.1

Canonical shared cross-domain schema definitions for the Adaptix polyrepo platform.

## Overview

This package provides typed Pydantic contract definitions for cross-domain communication across all Adaptix services. It is the single source of truth for:

- **Event contracts** - Domain events published across services
- **Request/Response contracts** - API request and response schemas
- **Read-only contracts** - Cross-domain data transfer objects
- **Shared enums** - Canonical status and type enumerations

## Package Structure

```
adaptix_contracts/
├── __init__.py          # Package root with convenience exports
└── schemas/             # All contract schema definitions
    ├── __init__.py      # Consolidated schema exports
    ├── air_contracts.py
    ├── air_pilot_contracts.py
    ├── audit_contracts.py
    ├── billing_*.py     # Billing domain contracts
    ├── cad_*.py         # CAD domain contracts
    ├── core_contracts.py
    ├── crewlink_contracts.py
    ├── communications_contracts.py
    ├── epcr_contracts.py
    ├── feature_flag_contracts.py
    ├── field_contracts.py
    ├── fire_contracts.py
    ├── metrics_contracts.py
    ├── nemsis_exports.py
    ├── ocr_contracts.py
    ├── patient_portal_contracts.py
    ├── search_contracts.py
    ├── transport_contracts.py
    ├── voice_contracts.py
    └── workflow_contracts.py
```

## Domain Coverage

This package provides complete schema coverage for **28 domains**:

### Core Infrastructure
- **core** - Base event contracts and auth context
- **audit** - Audit logging, PHI access, security events
- **metrics** - Service health, observability
- **search** - Cross-domain search and indexing
- **communications** - Notifications and messaging
- **feature_flag** - Feature flag resolution
- **workflow** - Long-running workflows and orchestration

### Billing Domain (8 modules)
- **billing** - Core claim lifecycle, payments, denials
- **billing_auth** - Billing portal authentication
- **billing_clearinghouse** - Clearinghouse integrations
- **billing_eligibility** - Insurance verification
- **billing_portal** - Portal UI contracts
- **billing_transport** - Billing-transport readiness

### Clinical & Operations
- **epcr** - Electronic patient care reports
- **clinical_visual** - AR-assisted clinical overlays and structured findings
- **nemsis** - NEMSIS export lifecycle
- **ocr** - Document OCR processing
- **patient_portal** - Patient-facing portal

### Dispatch & Field
- **cad** - Computer-aided dispatch
- **cad_transport** - CAD-transport integration
- **fire** - Fire incident management
- **field** - Field unit status and telemetry
- **inventory** - Inventory, replenishment, readiness, and cycle count contracts

### Air Operations
- **air** - Air mission contracts
- **air_pilot** - Pilot readiness and go/no-go

### Transport
- **transport** - Transport request lifecycle
- **crewlink** - Crew paging and rostering

### Voice
- **voice** - Voice room management

## Installation

```bash
# From source (development)
pip install -e .

# From package repository
pip install adaptix-contracts
```

## Requirements

- Python >= 3.11
- Pydantic >= 2.6.0

## Usage

### Import All Schemas

```python
from adaptix_contracts.schemas import *

# Use any schema
claim = ClaimContract(
    claim_id="claim-123",
    tenant_id="tenant-123",
    patient_id="patient-123",
    status=ClaimStatus.DRAFT,
    total_charge_cents=10000,
    balance_cents=10000,
    created_at=datetime.now(),
    updated_at=datetime.now()
)
```

### Import Specific Schemas

```python
from adaptix_contracts.schemas import (
    ClaimContract,
    ClaimStatus,
    ClaimCreatedEvent,
    EpcrChartFinalizedEvent,
    TransportRequestCreate,
)
```

### Working with Events

```python
from adaptix_contracts.schemas import (
    ClaimCreatedEvent,
    EpcrChartFinalizedEvent,
    TransportRequestCreatedEvent,
)
from datetime import datetime

# Create an event
event = ClaimCreatedEvent(
    claim_id="claim-123",
    tenant_id="tenant-123",
    patient_id="patient-123",
    created_at=datetime.now()
)

# Serialize to dict
event_dict = event.model_dump()

# Deserialize from dict
event_restored = ClaimCreatedEvent(**event_dict)
```

### Using Enums

```python
from adaptix_contracts.schemas import (
    ClaimStatus,
    WorkflowStatus,
    AuditSeverity,
)

# Access enum values
status = ClaimStatus.SUBMITTED
print(status.value)  # "submitted"

# Validate enum values
try:
    status = ClaimStatus("invalid")
except ValueError:
    print("Invalid status value")
```

## Contract Principles

This package adheres to strict contract-only boundaries:

### ✅ What This Package Contains

- **Pydantic models** for events, requests, responses
- **Enums** for canonical statuses and types
- **Type annotations** for all fields
- **Field validation** at the schema level
- **Shared contract definitions** used across domains

### ❌ What This Package Does NOT Contain

- **Business logic** - No service implementation
- **Database models** - No ORM models or persistence
- **API routes** - No HTTP handlers
- **Service orchestration** - No workflow engines
- **Infrastructure code** - No Terraform, Docker, etc.

## Validation

Run the validation script to ensure all contracts are properly defined:

```bash
python validate_contracts.py
```

This validates:
- All 242 exports are importable
- All 197 models are Pydantic v2 compatible
- All 45 enums are properly defined
- All 28 domains are covered
- Sample models can be instantiated

Run the automated regression suite for export integrity, schema serialization,
and representative validation failures:

```bash
pip install -e .[dev]
python -m pytest
```

## Versioning

This package follows semantic versioning:

- **Major version** - Breaking changes to contracts
- **Minor version** - New contracts or backward-compatible additions
- **Patch version** - Bug fixes, documentation updates

Release governance artifacts:

- [`CHANGELOG.md`](CHANGELOG.md) — authoritative release history
- [`DEPRECATION_POLICY.md`](DEPRECATION_POLICY.md) — backward-compatibility and retirement rules

Contract changes are not considered releasable until the changelog is updated,
deprecation impact is documented for public surface changes, and the validation
script plus pytest suite both pass.

## Contributing

When adding new contracts:

1. Add the contract file to `adaptix_contracts/schemas/`
2. Export symbols in `adaptix_contracts/schemas/__init__.py`
3. Add to `__all__` list in alphabetical/domain order
4. Run `python validate_contracts.py` to verify
5. Ensure Pydantic v2 compatibility
6. Follow existing naming conventions

## License

Internal Adaptix package - not for public distribution.

## Support

For questions or issues, contact the Adaptix platform team.
