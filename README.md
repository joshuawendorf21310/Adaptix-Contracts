# Adaptix Contracts

**Version:** 1.1.0

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
├── py.typed             # PEP 561 type hint marker
└── schemas/             # All contract schema definitions
    ├── __init__.py      # Consolidated schema exports
    ├── admin_contracts.py
    ├── ai_contracts.py
    ├── air_contracts.py
    ├── air_pilot_contracts.py
    ├── audit_contracts.py
    ├── billing_*.py     # Billing domain contracts
    ├── cad_*.py         # CAD domain contracts
    ├── calendar_contracts.py
    ├── clinical_visual_contracts.py
    ├── command_center_contracts.py
    ├── communications_contracts.py
    ├── continuity_contracts.py
    ├── contract_onboarding_contracts.py
    ├── core_contracts.py
    ├── crewlink_contracts.py
    ├── crm_contracts.py
    ├── duty_auth_contracts.py
    ├── epcr_contracts.py
    ├── feature_flag_contracts.py
    ├── field_contracts.py
    ├── fire_contracts.py
    ├── founder_contracts.py
    ├── graph_contracts.py
    ├── intake_contracts.py
    ├── inventory_contracts.py
    ├── labor_contracts.py
    ├── legal_execution_contracts.py
    ├── medications_contracts.py
    ├── metrics_contracts.py
    ├── narcotic.py
    ├── nemsis_exports.py
    ├── ocr_contracts.py
    ├── patient_portal_contracts.py
    ├── search_contracts.py
    ├── service_registry.py
    ├── signature_compliance_contracts.py
    ├── telnyx_contracts.py
    ├── tenant_contracts.py
    ├── transport_contracts.py
    ├── voice_contracts.py
    ├── workflow_contracts.py
    └── workforce_contracts.py
```

## Domain Coverage

This package provides complete schema coverage for **48 domains**:

### Core Infrastructure
- **core** - Base event contracts and auth context
- **admin** - Administrative operations
- **audit** - Audit logging, PHI access, security events
- **calendar** - Scheduling and calendar events
- **communications** - Notifications and messaging
- **feature_flag** - Feature flag resolution
- **graph** - Graph-based relationships and queries
- **metrics** - Service health, observability
- **search** - Cross-domain search and indexing
- **service_registry** - Service discovery and registration
- **workflow** - Long-running workflows and orchestration

### Billing Domain
- **billing** - Core claim lifecycle, payments, denials
- **billing_auth** - Billing portal authentication
- **billing_clearinghouse** - Clearinghouse integrations
- **billing_eligibility** - Insurance verification
- **billing_portal** - Portal UI contracts
- **billing_transport** - Billing-transport readiness

### Clinical & Operations
- **ai** - AI/ML inference and model contracts
- **clinical_visual** - AR-assisted clinical overlays and structured findings
- **continuity** - Continuity of care contracts
- **epcr** - Electronic patient care reports
- **medications** - Medication tracking and administration
- **narcotic** - Controlled substance tracking
- **nemsis** - NEMSIS export lifecycle
- **ocr** - Document OCR processing
- **patient_portal** - Patient-facing portal
- **signature_compliance** - Signature and compliance validation

### Dispatch & Field
- **cad** - Computer-aided dispatch
- **cad_transport** - CAD-transport integration
- **command_center** - Command center operations
- **field** - Field unit status and telemetry
- **fire** - Fire incident management
- **intake** - Intake and triage workflows
- **inventory** - Inventory, replenishment, readiness, and cycle count contracts

### Air Operations
- **air** - Air mission contracts
- **air_pilot** - Pilot readiness and go/no-go

### Transport
- **transport** - Transport request lifecycle
- **crewlink** - Crew paging and rostering

### Voice & Communications
- **telnyx** - Telephony integrations
- **voice** - Voice room management

### Identity & Access
- **duty_auth** - Duty session and field authentication
- **tenant** - Multi-tenant configuration

### Business Operations
- **contract_onboarding** - Contract onboarding workflows
- **crm** - Customer relationship management
- **founder** - Founder-specific contracts
- **labor** - Labor and workforce management
- **legal_execution** - Legal contract execution
- **workforce** - Workforce scheduling and management

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
- All 572 exports are importable
- All 461 models are Pydantic v2 compatible
- All 103 enums are properly defined
- All 48 domains are covered
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

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full license text.

## Support

For questions or issues, contact the Adaptix platform team.
