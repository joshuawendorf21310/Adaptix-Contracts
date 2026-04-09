from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

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
    permissions: list[str] = Field(default_factory=list)
    scopes: list[str] = Field(default_factory=list)
    email: EmailStr | None = None


class AuthContext(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    tenant_id: UUID
    user_id: UUID
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    scopes: list[str] = Field(default_factory=list)


class CurrentUser(AuthContext):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    subject_id: UUID | None = None
    session_id: str | None = None
    role: str = "viewer"
    primary_role: str | None = None
    email: EmailStr | None = None

    @classmethod
    def from_claims(
        cls,
        *,
        user_id: UUID,
        tenant_id: UUID,
        role: str | None = None,
        primary_role: str | None = None,
        roles: list[str] | None = None,
        permissions: list[str] | None = None,
        scopes: list[str] | None = None,
        subject_id: UUID | None = None,
        session_id: str | None = None,
        email: EmailStr | str | None = None,
    ) -> "CurrentUser":
        normalized_roles = normalize_role_claims(
            primary_role=primary_role,
            role=role,
            roles=roles,
        )
        effective_primary_role = primary_role or role or (normalized_roles[0] if normalized_roles else "viewer")

        return cls(
            user_id=user_id,
            subject_id=subject_id or user_id,
            tenant_id=tenant_id,
            session_id=session_id,
            role=effective_primary_role or "viewer",
            primary_role=effective_primary_role or "viewer",
            roles=normalized_roles,
            permissions=[str(item).strip() for item in (permissions or []) if str(item).strip()],
            scopes=[str(item).strip() for item in (scopes or []) if str(item).strip()],
            email=email,
        )

    @property
    def resolved_subject_id(self) -> UUID:
        return self.subject_id or self.user_id

    @property
    def resolved_primary_role(self) -> str:
        return str(self.primary_role or self.role or (self.roles[0] if self.roles else "viewer"))

    @property
    def resolved_roles(self) -> list[str]:
        ordered: list[str] = []
        for candidate in [self.resolved_primary_role, self.role, *self.roles]:
            value = str(candidate or "").strip()
            if value and value not in ordered:
                ordered.append(value)
        return ordered or ["viewer"]

    def __getitem__(self, key: str):
        value = getattr(self, key)
        return str(value) if isinstance(value, UUID) else value

    def get(self, key: str, default=None):
        value = getattr(self, key, default)
        return str(value) if isinstance(value, UUID) else value
