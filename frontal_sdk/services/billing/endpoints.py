"""Generated endpoint catalog for the billing service."""

from frontal_sdk.utils.operation import Endpoint


class BillingEndpoint(Endpoint):
    """Known billing API operations."""

    GET_BILLING_ADDONS_PARAM_1_ENTITLEMENTS = (
        "GET",
        "/billing/addons/{param}/entitlements",
    )
    GET_BILLING_CUSTOMERS_PARAM_1_ENTITLEMENTS = (
        "GET",
        "/billing/customers/{param}/entitlements",
    )
    GET_BILLING_CUSTOMERS_PARAM_1_INVOICES_SUMMARY = (
        "GET",
        "/billing/customers/{param}/invoices/summary",
    )
    GET_BILLING_CUSTOMERS_PARAM_1_USAGE = ("GET", "/billing/customers/{param}/usage")
    GET_BILLING_CUSTOMERS_PARAM_1_WALLETS = (
        "GET",
        "/billing/customers/{param}/wallets",
    )
    GET_BILLING_CUSTOMERS_PORTAL_PARAM_1 = ("GET", "/billing/customers/portal/{param}")
    GET_BILLING_PLANS_PARAM_1_ENTITLEMENTS = (
        "GET",
        "/billing/plans/{param}/entitlements",
    )
    GET_BILLING_PRICES_LOOKUP_PARAM_1 = ("GET", "/billing/prices/lookup/{param}")
    GET_BILLING_SUBSCRIPTIONS_PARAM_1_ENTITLEMENTS = (
        "GET",
        "/billing/subscriptions/{param}/entitlements",
    )
    GET_BILLING_WALLETS_PARAM_1_BALANCE_REAL_TIME = (
        "GET",
        "/billing/wallets/{param}/balance/real-time",
    )
    GET_BILLING_WALLETS_PARAM_1_TRANSACTIONS = (
        "GET",
        "/billing/wallets/{param}/transactions",
    )
    GETRAW_BILLING_INVOICES_PARAM_1_PDF = ("GETRAW", "/billing/invoices/{param}/pdf")
    POST_BILLING_INVOICES_PARAM_1_FINALIZE = (
        "POST",
        "/billing/invoices/{param}/finalize",
    )
    POST_BILLING_INVOICES_PARAM_1_VOID = ("POST", "/billing/invoices/{param}/void")
    POST_BILLING_INVOICES_PREVIEW = ("POST", "/billing/invoices/preview")
    POST_BILLING_METERS_PARAM_1_DISABLE = ("POST", "/billing/meters/{param}/disable")
    POST_BILLING_PLANS_PARAM_1_CLONE = ("POST", "/billing/plans/{param}/clone")
    POST_BILLING_SUBSCRIPTIONS_PARAM_1_ACTIVATE = (
        "POST",
        "/billing/subscriptions/{param}/activate",
    )
    POST_BILLING_SUBSCRIPTIONS_PARAM_1_CANCEL = (
        "POST",
        "/billing/subscriptions/{param}/cancel",
    )
    POST_BILLING_SUBSCRIPTIONS_PARAM_1_PAUSE = (
        "POST",
        "/billing/subscriptions/{param}/pause",
    )
    POST_BILLING_SUBSCRIPTIONS_PARAM_1_RESUME = (
        "POST",
        "/billing/subscriptions/{param}/resume",
    )
    POST_BILLING_WALLETS_PARAM_1_TERMINATE = (
        "POST",
        "/billing/wallets/{param}/terminate",
    )
    POST_BILLING_WALLETS_PARAM_1_TOP_UP = ("POST", "/billing/wallets/{param}/top-up")
