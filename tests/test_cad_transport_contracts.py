from adaptix_contracts import CadTransportLinkStatus as package_root_status
from adaptix_contracts.schemas import CadTransportLinkStatus as schema_status
from adaptix_contracts.schemas.cad_transport_contracts import CadTransportLinkContract


def test_cad_transport_link_status_reexported_from_schema_and_package_root() -> None:
    assert package_root_status is schema_status


def test_cad_transport_link_contract_uses_shared_status_enum() -> None:
    assert CadTransportLinkContract.model_fields["status"].annotation is schema_status