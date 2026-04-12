"""Adaptix auth contracts and utilities."""

from .permissions import (
    get_all_permissions,
    get_permission_description,
    permission_exists,
    register_permissions,
)

__all__ = [
    "get_all_permissions",
    "get_permission_description",
    "permission_exists",
    "register_permissions",
]
