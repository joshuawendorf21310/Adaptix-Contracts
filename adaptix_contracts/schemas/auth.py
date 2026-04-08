from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from adaptix_contracts.utils.roles import normalize_role_claims


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None
    user_id: str | None = None
    subject_id: str | None = None
    tenant_id: str | None = None
    session_id: str | None = None
    role: str | None = None
    primary_role: str | None = None
    roles: list[str] = Field(default_factory=list)


class CurrentUser(BaseModel):
    user_id: UUID
    tenant_id: UUID
    subject_id: UUID | None = None
    session_id: str | None = None
    role: str = ""
    primary_role: str = ""
    roles: list[str] = Field(default_factory=list)

    @classmethod
    def from_claims(
        cls,
        *,
        user_id: UUID,
        tenant_id: UUID,
        role: str | None = None,
        primary_role: str | None = None,
        roles: list[str] | None = None,
        subject_id: UUID | None = None,
        session_id: str | None = None,
    ) -> "CurrentUser":
        normalized_roles = normalize_role_claims(
            primary_role=primary_role,
            role=role,
            roles=roles,
        )
        effective_primary_role = primary_role or role or (normalized_roles[0] if normalized_roles else "")

        return cls(
            user_id=user_id,
            subject_id=subject_id or user_id,
            tenant_id=tenant_id,
            session_id=session_id,
            role=effective_primary_role,
            primary_role=effective_primary_role,
            roles=normalized_roles,
        )

    @property
    def resolved_subject_id(self) -> UUID:
        return self.subject_id or self.user_id

    @property
    def resolved_primary_role(self) -> str:
        return self.primary_role or self.role or (self.roles[0] if self.roles else "")

    @property
    def resolved_roles(self) -> list[str]:
        return self.roles or normalize_role_claims(primary_role=self.primary_role, role=self.role)

    def __getitem__(self, key: str):
        """Backward compatibility with legacy dict-style access: current_user["user_id"]."""
        if key == "user_id":
            return str(self.user_id)
        if key == "tenant_id":
            return str(self.tenant_id)
        if key == "subject_id":
            return str(self.resolved_subject_id)
        if key in {"primary_role", "role"}:
            return self.resolved_primary_role
        if key == "roles":
            return self.resolved_roles
        return getattr(self, key)

    def get(self, key: str, default=None):
        """Backward compatibility with legacy dict-style .get(): current_user.get("role")."""
        try:
            return self[key]
        except AttributeError:
            return default
        except KeyError:
            return default
