"""Typed API resource for the auth endpoints."""

from __future__ import annotations

from typing import Generic

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import QueryParams
from frontal_sdk.models.requests import UNSET, RequestBodyInput
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    JSONResultT,
    StreamResultT,
)


class Auth(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the auth API endpoints."""

    def delete_mfa(
        self, mfa_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /auth/account/mfa/{param}."""
        return self._request(
            Operation("DELETE", "/auth/account/mfa/{param}"),
            path_params=(mfa_id,),
            query=query,
        )

    def delete_auth_account_profile(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /auth/account/profile."""
        return self._request(
            Operation("DELETE", "/auth/account/profile"),
            path_params=(),
            query=query,
        )

    def delete_api_key(
        self, api_key_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /auth/account/security/api-keys/{param}."""
        return self._request(
            Operation("DELETE", "/auth/account/security/api-keys/{param}"),
            path_params=(api_key_id,),
            query=query,
        )

    def delete_device(
        self, device_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /auth/account/security/devices/{param}."""
        return self._request(
            Operation("DELETE", "/auth/account/security/devices/{param}"),
            path_params=(device_id,),
            query=query,
        )

    def delete_session(
        self, session_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /auth/account/sessions/{param}."""
        return self._request(
            Operation("DELETE", "/auth/account/sessions/{param}"),
            path_params=(session_id,),
            query=query,
        )

    def delete_user(
        self, user_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /auth/admin/users/{param}."""
        return self._request(
            Operation("DELETE", "/auth/admin/users/{param}"),
            path_params=(user_id,),
            query=query,
        )

    def delete_factor_for_user(
        self, user_id: str, factor_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /auth/admin/users/{param}/factors/{param}."""
        return self._request(
            Operation("DELETE", "/auth/admin/users/{param}/factors/{param}"),
            path_params=(user_id, factor_id),
            query=query,
        )

    def delete_factor(
        self, factor_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /auth/factors/{param}."""
        return self._request(
            Operation("DELETE", "/auth/factors/{param}"),
            path_params=(factor_id,),
            query=query,
        )

    def delete_identity(
        self, identity_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /auth/user/identities/{param}."""
        return self._request(
            Operation("DELETE", "/auth/user/identities/{param}"),
            path_params=(identity_id,),
            query=query,
        )

    def get_auth_account_audit_log(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /auth/account/audit-log."""
        return self._request(
            Operation("GET", "/auth/account/audit-log"),
            path_params=(),
            query=query,
        )

    def get_auth_account_mfa(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /auth/account/mfa."""
        return self._request(
            Operation("GET", "/auth/account/mfa"),
            path_params=(),
            query=query,
        )

    def get_mfa(self, mfa_id: str, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /auth/account/mfa/{param}."""
        return self._request(
            Operation("GET", "/auth/account/mfa/{param}"),
            path_params=(mfa_id,),
            query=query,
        )

    def get_auth_account_profile(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /auth/account/profile."""
        return self._request(
            Operation("GET", "/auth/account/profile"),
            path_params=(),
            query=query,
        )

    def list_api_keys(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /auth/account/security/api-keys."""
        return self._request(
            Operation("GET", "/auth/account/security/api-keys"),
            path_params=(),
            query=query,
        )

    def get_api_key(
        self, api_key_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /auth/account/security/api-keys/{param}."""
        return self._request(
            Operation("GET", "/auth/account/security/api-keys/{param}"),
            path_params=(api_key_id,),
            query=query,
        )

    def list_devices(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /auth/account/security/devices."""
        return self._request(
            Operation("GET", "/auth/account/security/devices"),
            path_params=(),
            query=query,
        )

    def get_device(
        self, device_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /auth/account/security/devices/{param}."""
        return self._request(
            Operation("GET", "/auth/account/security/devices/{param}"),
            path_params=(device_id,),
            query=query,
        )

    def list_sessions(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /auth/account/sessions."""
        return self._request(
            Operation("GET", "/auth/account/sessions"),
            path_params=(),
            query=query,
        )

    def list_users(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /auth/admin/users."""
        return self._request(
            Operation("GET", "/auth/admin/users"),
            path_params=(),
            query=query,
        )

    def get_user(
        self, user_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /auth/admin/users/{param}."""
        return self._request(
            Operation("GET", "/auth/admin/users/{param}"),
            path_params=(user_id,),
            query=query,
        )

    def list_user_factors(
        self, user_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /auth/admin/users/{param}/factors."""
        return self._request(
            Operation("GET", "/auth/admin/users/{param}/factors"),
            path_params=(user_id,),
            query=query,
        )

    def get_auth_auth_session(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /auth/auth/session."""
        return self._request(
            Operation("GET", "/auth/auth/session"),
            path_params=(),
            query=query,
        )

    def list_factors(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /auth/factors."""
        return self._request(
            Operation("GET", "/auth/factors"),
            path_params=(),
            query=query,
        )

    def get_auth_user(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /auth/user."""
        return self._request(
            Operation("GET", "/auth/user"),
            path_params=(),
            query=query,
        )

    def list_identities(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /auth/user/identities."""
        return self._request(
            Operation("GET", "/auth/user/identities"),
            path_params=(),
            query=query,
        )

    def post_auth_account_mfa(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/account/mfa."""
        return self._request(
            Operation("POST", "/auth/account/mfa"),
            path_params=(),
            query=query,
            body=body,
        )

    def challenge_mfa(
        self,
        mfa_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /auth/account/mfa/{param}/challenge."""
        return self._request(
            Operation("POST", "/auth/account/mfa/{param}/challenge"),
            path_params=(mfa_id,),
            query=query,
            body=body,
        )

    def verify_mfa(
        self,
        mfa_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /auth/account/mfa/{param}/verify."""
        return self._request(
            Operation("POST", "/auth/account/mfa/{param}/verify"),
            path_params=(mfa_id,),
            query=query,
            body=body,
        )

    def post_auth_account_password(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/account/password."""
        return self._request(
            Operation("POST", "/auth/account/password"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_api_key(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/account/security/api-keys."""
        return self._request(
            Operation("POST", "/auth/account/security/api-keys"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_device(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/account/security/devices."""
        return self._request(
            Operation("POST", "/auth/account/security/devices"),
            path_params=(),
            query=query,
            body=body,
        )

    def trust_device(
        self,
        device_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /auth/account/security/devices/{param}/trust."""
        return self._request(
            Operation("POST", "/auth/account/security/devices/{param}/trust"),
            path_params=(device_id,),
            query=query,
            body=body,
        )

    def extend_session(
        self,
        session_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /auth/account/sessions/{param}/extend."""
        return self._request(
            Operation("POST", "/auth/account/sessions/{param}/extend"),
            path_params=(session_id,),
            query=query,
            body=body,
        )

    def post_auth_admin_generate_link(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/admin/generate_link."""
        return self._request(
            Operation("POST", "/auth/admin/generate_link"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_admin_logout(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/admin/logout."""
        return self._request(
            Operation("POST", "/auth/admin/logout"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_user(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/admin/users."""
        return self._request(
            Operation("POST", "/auth/admin/users"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_auth_session(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/auth/session."""
        return self._request(
            Operation("POST", "/auth/auth/session"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_authorize(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/authorize."""
        return self._request(
            Operation("POST", "/auth/authorize"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_factor(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/factors."""
        return self._request(
            Operation("POST", "/auth/factors"),
            path_params=(),
            query=query,
            body=body,
        )

    def challenge_factor(
        self,
        factor_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /auth/factors/{param}/challenge."""
        return self._request(
            Operation("POST", "/auth/factors/{param}/challenge"),
            path_params=(factor_id,),
            query=query,
            body=body,
        )

    def verify_factor(
        self,
        factor_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /auth/factors/{param}/verify."""
        return self._request(
            Operation("POST", "/auth/factors/{param}/verify"),
            path_params=(factor_id,),
            query=query,
            body=body,
        )

    def post_auth_invite(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/invite."""
        return self._request(
            Operation("POST", "/auth/invite"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_logout(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/logout."""
        return self._request(
            Operation("POST", "/auth/logout"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_otp(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/otp."""
        return self._request(
            Operation("POST", "/auth/otp"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_reauthenticate(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/reauthenticate."""
        return self._request(
            Operation("POST", "/auth/reauthenticate"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_recover(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/recover."""
        return self._request(
            Operation("POST", "/auth/recover"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_resend(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/resend."""
        return self._request(
            Operation("POST", "/auth/resend"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_signup(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/signup."""
        return self._request(
            Operation("POST", "/auth/signup"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_sso(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/sso."""
        return self._request(
            Operation("POST", "/auth/sso"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_token_query_grant_type_id_token(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/token?grant_type=id_token."""
        return self._request(
            Operation("POST", "/auth/token?grant_type=id_token"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_token_query_grant_type_password(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/token?grant_type=password."""
        return self._request(
            Operation("POST", "/auth/token?grant_type=password"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_token_query_grant_type_pkce(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/token?grant_type=pkce."""
        return self._request(
            Operation("POST", "/auth/token?grant_type=pkce"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_token_query_grant_type_refresh_token(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/token?grant_type=refresh_token."""
        return self._request(
            Operation("POST", "/auth/token?grant_type=refresh_token"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_identity(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/user/identities."""
        return self._request(
            Operation("POST", "/auth/user/identities"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_auth_verify(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /auth/verify."""
        return self._request(
            Operation("POST", "/auth/verify"),
            path_params=(),
            query=query,
            body=body,
        )

    def put_auth_account_profile(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call PUT /auth/account/profile."""
        return self._request(
            Operation("PUT", "/auth/account/profile"),
            path_params=(),
            query=query,
            body=body,
        )

    def update_api_key(
        self,
        api_key_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /auth/account/security/api-keys/{param}."""
        return self._request(
            Operation("PUT", "/auth/account/security/api-keys/{param}"),
            path_params=(api_key_id,),
            query=query,
            body=body,
        )

    def update_user(
        self,
        user_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /auth/admin/users/{param}."""
        return self._request(
            Operation("PUT", "/auth/admin/users/{param}"),
            path_params=(user_id,),
            query=query,
            body=body,
        )

    def put_auth_user(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call PUT /auth/user."""
        return self._request(
            Operation("PUT", "/auth/user"),
            path_params=(),
            query=query,
            body=body,
        )
