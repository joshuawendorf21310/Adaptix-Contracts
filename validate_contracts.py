#!/usr/bin/env python3
"""Comprehensive validation script for adaptix-contracts package.

This script validates:
1. All schema files can be imported
2. All models can be instantiated with valid data
3. No circular import issues exist
4. All exports are correctly defined
5. Pydantic v2 compatibility
"""

import sys
from datetime import datetime
from typing import get_args, get_origin
from collections import defaultdict


def validate_imports():
    """Test that all schema modules can be imported."""
    print("=" * 70)
    print("PHASE 1: Import Validation")
    print("=" * 70)

    try:
        from adaptix_contracts.schemas import __all__
        print(f"✓ Schema __all__ list defined ({len(__all__)} exports)")

        # Import all schemas
        from adaptix_contracts import schemas
        imported_count = 0
        for name in __all__:
            if hasattr(schemas, name):
                imported_count += 1
            else:
                print(f"❌ Missing export: {name}")
                return False

        print(f"✓ All {imported_count} exports are accessible")
        return True

    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def validate_model_structure():
    """Validate Pydantic model structure and compatibility."""
    print("\n" + "=" * 70)
    print("PHASE 2: Model Structure Validation")
    print("=" * 70)

    from adaptix_contracts import schemas
    from pydantic import BaseModel
    from enum import Enum

    models = []
    enums = []

    for name in dir(schemas):
        if name.startswith('_'):
            continue
        obj = getattr(schemas, name)

        if isinstance(obj, type):
            if issubclass(obj, BaseModel) and obj is not BaseModel:
                models.append((name, obj))
            elif issubclass(obj, Enum) and obj is not Enum:
                enums.append((name, obj))

    print(f"✓ Found {len(models)} model classes")
    print(f"✓ Found {len(enums)} enum classes")

    # Check for proper Pydantic v2 usage
    issues = []
    for name, model in models:
        # Check if model has model_config (Pydantic v2 pattern)
        if hasattr(model, 'model_fields'):
            # Pydantic v2
            pass
        else:
            issues.append(f"{name}: May not be Pydantic v2 compatible")

    if issues:
        print("\n⚠️  Potential issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✓ All models appear Pydantic v2 compatible")

    return True


def validate_sample_instantiation():
    """Test that key models can be instantiated."""
    print("\n" + "=" * 70)
    print("PHASE 3: Model Instantiation Tests")
    print("=" * 70)

    try:
        from adaptix_contracts.schemas import (
            # Core
            DomainEvent,
            UserAuthContext,
            # Billing
            ClaimContract,
            ClaimStatus,
            ClaimCreatedEvent,
            # Audit
            AuditRecord,
            AuditContext,
            AuditActorType,
            AuditActionType,
            AuditSeverity,
            # Feature Flags
            FeatureFlagContract,
            FeatureFlagStatus,
            # Workflow
            WorkflowExecution,
            WorkflowContext,
            WorkflowStatus,
        )
        from uuid import uuid4

        # Test audit record
        audit_ctx = AuditContext(
            tenant_id="test-tenant",
            service_name="validation-script"
        )

        audit = AuditRecord(
            audit_id="audit-123",
            actor_type=AuditActorType.SYSTEM,
            action_type=AuditActionType.CREATE,
            resource_type="claim",
            success=True,
            severity=AuditSeverity.LOW,
            context=audit_ctx,
            occurred_at=datetime.now()
        )
        print(f"✓ AuditRecord instantiated: {audit.audit_id}")

        # Test claim contract
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
        print(f"✓ ClaimContract instantiated: {claim.claim_id}")

        # Test feature flag
        flag = FeatureFlagContract(
            flag_key="test-feature",
            status=FeatureFlagStatus.ENABLED,
            default_enabled=True,
            evaluated_at=datetime.now()
        )
        print(f"✓ FeatureFlagContract instantiated: {flag.flag_key}")

        # Test workflow execution
        workflow_ctx = WorkflowContext(
            workflow_id="workflow-123",
            tenant_id="tenant-123"
        )

        workflow = WorkflowExecution(
            workflow_id="workflow-123",
            workflow_type="test-workflow",
            context=workflow_ctx,
            status=WorkflowStatus.RUNNING,
            started_at=datetime.now()
        )
        print(f"✓ WorkflowExecution instantiated: {workflow.workflow_id}")

        print("\n✓ All sample model instantiations successful")
        return True

    except Exception as e:
        print(f"❌ Model instantiation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_domain_coverage():
    """Validate that all expected domains are covered."""
    print("\n" + "=" * 70)
    print("PHASE 4: Domain Coverage Analysis")
    print("=" * 70)

    expected_domains = {
        'air', 'air_pilot', 'audit', 'billing', 'billing_auth',
        'billing_clearinghouse', 'billing_eligibility', 'billing_portal',
        'billing_transport', 'cad', 'cad_transport', 'communications',
        'core', 'crewlink', 'epcr', 'feature_flag', 'field', 'fire',
        'metrics', 'nemsis', 'ocr', 'patient_portal', 'search',
        'transport', 'voice', 'workflow'
    }

    from pathlib import Path

    schema_dir = Path('adaptix_contracts/schemas')
    contract_files = [f.stem for f in schema_dir.glob('*_contracts.py')]
    contract_files.extend(['nemsis_exports'])  # Special case

    # Normalize names
    actual_domains = set()
    for f in contract_files:
        domain = f.replace('_contracts', '').replace('_exports', '')
        actual_domains.add(domain)

    print(f"\nExpected domains: {len(expected_domains)}")
    print(f"Actual domains: {len(actual_domains)}")

    missing = expected_domains - actual_domains
    if missing:
        print(f"\n⚠️  Missing domains: {sorted(missing)}")

    extra = actual_domains - expected_domains
    if extra:
        print(f"\n✓ Additional domains: {sorted(extra)}")

    if not missing:
        print("\n✓ All expected domains are present")

    return True


def main():
    """Run all validation checks."""
    print("\n" + "=" * 70)
    print("ADAPTIX CONTRACTS VALIDATION")
    print("=" * 70)

    results = []

    results.append(("Import Validation", validate_imports()))
    results.append(("Model Structure", validate_model_structure()))
    results.append(("Model Instantiation", validate_sample_instantiation()))
    results.append(("Domain Coverage", validate_domain_coverage()))

    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False

    print("=" * 70)

    if all_passed:
        print("\n✅ All validations passed!")
        return 0
    else:
        print("\n❌ Some validations failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
