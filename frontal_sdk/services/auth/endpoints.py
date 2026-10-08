"""Generated endpoint catalog for the auth service."""

from frontal_sdk.utils.operation import Endpoint


class AuthEndpoint(Endpoint):
    """Known auth API operations."""

    DELETE_AUTH_ACCOUNT_MFA_PARAM_1 = ("DELETE", "/auth/account/mfa/{param}")
    DELETE_AUTH_ACCOUNT_PROFILE = ("DELETE", "/auth/account/profile")
    DELETE_AUTH_ACCOUNT_SECURITY_API_KEYS_PARAM_1 = (
        "DELETE",
        "/auth/account/security/api-keys/{param}",
    )
    DELETE_AUTH_ACCOUNT_SECURITY_DEVICES_PARAM_1 = (
        "DELETE",
        "/auth/account/security/devices/{param}",
    )
    DELETE_AUTH_ACCOUNT_SESSIONS_PARAM_1 = ("DELETE", "/auth/account/sessions/{param}")
    DELETE_AUTH_ADMIN_USERS_PARAM_1 = ("DELETE", "/auth/admin/users/{param}")
    DELETE_AUTH_ADMIN_USERS_PARAM_1_FACTORS_PARAM_2 = (
        "DELETE",
        "/auth/admin/users/{param}/factors/{param}",
    )
    DELETE_AUTH_FACTORS_PARAM_1 = ("DELETE", "/auth/factors/{param}")
    DELETE_AUTH_USER_IDENTITIES_PARAM_1 = ("DELETE", "/auth/user/identities/{param}")
    GET_AUTH_ACCOUNT_AUDIT_LOG = ("GET", "/auth/account/audit-log")
    GET_AUTH_ACCOUNT_MFA = ("GET", "/auth/account/mfa")
    GET_AUTH_ACCOUNT_MFA_PARAM_1 = ("GET", "/auth/account/mfa/{param}")
    GET_AUTH_ACCOUNT_PROFILE = ("GET", "/auth/account/profile")
    GET_AUTH_ACCOUNT_SECURITY_API_KEYS = ("GET", "/auth/account/security/api-keys")
    GET_AUTH_ACCOUNT_SECURITY_API_KEYS_PARAM_1 = (
        "GET",
        "/auth/account/security/api-keys/{param}",
    )
    GET_AUTH_ACCOUNT_SECURITY_DEVICES = ("GET", "/auth/account/security/devices")
    GET_AUTH_ACCOUNT_SECURITY_DEVICES_PARAM_1 = (
        "GET",
        "/auth/account/security/devices/{param}",
    )
    GET_AUTH_ACCOUNT_SESSIONS = ("GET", "/auth/account/sessions")
    GET_AUTH_ADMIN_USERS = ("GET", "/auth/admin/users")
    GET_AUTH_ADMIN_USERS_PARAM_1 = ("GET", "/auth/admin/users/{param}")
    GET_AUTH_ADMIN_USERS_PARAM_1_FACTORS = ("GET", "/auth/admin/users/{param}/factors")
    GET_AUTH_AUTH_SESSION = ("GET", "/auth/auth/session")
    GET_AUTH_FACTORS = ("GET", "/auth/factors")
    GET_AUTH_USER = ("GET", "/auth/user")
    GET_AUTH_USER_IDENTITIES = ("GET", "/auth/user/identities")
    POST_AUTH_ACCOUNT_MFA = ("POST", "/auth/account/mfa")
    POST_AUTH_ACCOUNT_MFA_PARAM_1_CHALLENGE = (
        "POST",
        "/auth/account/mfa/{param}/challenge",
    )
    POST_AUTH_ACCOUNT_MFA_PARAM_1_VERIFY = ("POST", "/auth/account/mfa/{param}/verify")
    POST_AUTH_ACCOUNT_PASSWORD = ("POST", "/auth/account/password")
    POST_AUTH_ACCOUNT_SECURITY_API_KEYS = ("POST", "/auth/account/security/api-keys")
    POST_AUTH_ACCOUNT_SECURITY_DEVICES = ("POST", "/auth/account/security/devices")
    POST_AUTH_ACCOUNT_SECURITY_DEVICES_PARAM_1_TRUST = (
        "POST",
        "/auth/account/security/devices/{param}/trust",
    )
    POST_AUTH_ACCOUNT_SESSIONS_PARAM_1_EXTEND = (
        "POST",
        "/auth/account/sessions/{param}/extend",
    )
    POST_AUTH_ADMIN_GENERATE_LINK = ("POST", "/auth/admin/generate_link")
    POST_AUTH_ADMIN_LOGOUT = ("POST", "/auth/admin/logout")
    POST_AUTH_ADMIN_USERS = ("POST", "/auth/admin/users")
    POST_AUTH_AUTH_SESSION = ("POST", "/auth/auth/session")
    POST_AUTH_AUTHORIZE = ("POST", "/auth/authorize")
    POST_AUTH_FACTORS = ("POST", "/auth/factors")
    POST_AUTH_FACTORS_PARAM_1_CHALLENGE = ("POST", "/auth/factors/{param}/challenge")
    POST_AUTH_FACTORS_PARAM_1_VERIFY = ("POST", "/auth/factors/{param}/verify")
    POST_AUTH_INVITE = ("POST", "/auth/invite")
    POST_AUTH_LOGOUT = ("POST", "/auth/logout")
    POST_AUTH_OTP = ("POST", "/auth/otp")
    POST_AUTH_REAUTHENTICATE = ("POST", "/auth/reauthenticate")
    POST_AUTH_RECOVER = ("POST", "/auth/recover")
    POST_AUTH_RESEND = ("POST", "/auth/resend")
    POST_AUTH_SIGNUP = ("POST", "/auth/signup")
    POST_AUTH_SSO = ("POST", "/auth/sso")
    POST_AUTH_TOKEN_GRANT_TYPE_ID_TOKEN = ("POST", "/auth/token?grant_type=id_token")
    POST_AUTH_TOKEN_GRANT_TYPE_PASSWORD = ("POST", "/auth/token?grant_type=password")
    POST_AUTH_TOKEN_GRANT_TYPE_PKCE = ("POST", "/auth/token?grant_type=pkce")
    POST_AUTH_TOKEN_GRANT_TYPE_REFRESH_TOKEN = (
        "POST",
        "/auth/token?grant_type=refresh_token",
    )
    POST_AUTH_USER_IDENTITIES = ("POST", "/auth/user/identities")
    POST_AUTH_VERIFY = ("POST", "/auth/verify")
    PUT_AUTH_ACCOUNT_PROFILE = ("PUT", "/auth/account/profile")
    PUT_AUTH_ACCOUNT_SECURITY_API_KEYS_PARAM_1 = (
        "PUT",
        "/auth/account/security/api-keys/{param}",
    )
    PUT_AUTH_ADMIN_USERS_PARAM_1 = ("PUT", "/auth/admin/users/{param}")
    PUT_AUTH_USER = ("PUT", "/auth/user")
