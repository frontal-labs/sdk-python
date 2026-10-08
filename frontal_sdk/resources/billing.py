"""Typed API resource for the billing endpoints."""

from __future__ import annotations

from typing import Generic

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import QueryParams, RequestBody
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    JSONResultT,
    StreamResultT,
)


class Billing(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the billing API endpoints."""

    def get_billing_addons_by_param_1_entitlements(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/addons/{param}/entitlements."""
        return self._request(
            Operation("GET", "/billing/addons/{param}/entitlements"),
            path_params=(param_1,),
            query=query,
        )

    def get_billing_customers_by_param_1_entitlements(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/customers/{param}/entitlements."""
        return self._request(
            Operation("GET", "/billing/customers/{param}/entitlements"),
            path_params=(param_1,),
            query=query,
        )

    def get_billing_customers_by_param_1_invoices_summary(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/customers/{param}/invoices/summary."""
        return self._request(
            Operation("GET", "/billing/customers/{param}/invoices/summary"),
            path_params=(param_1,),
            query=query,
        )

    def get_billing_customers_by_param_1_usage(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/customers/{param}/usage."""
        return self._request(
            Operation("GET", "/billing/customers/{param}/usage"),
            path_params=(param_1,),
            query=query,
        )

    def get_billing_customers_by_param_1_wallets(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/customers/{param}/wallets."""
        return self._request(
            Operation("GET", "/billing/customers/{param}/wallets"),
            path_params=(param_1,),
            query=query,
        )

    def get_billing_customers_portal_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/customers/portal/{param}."""
        return self._request(
            Operation("GET", "/billing/customers/portal/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_billing_plans_by_param_1_entitlements(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/plans/{param}/entitlements."""
        return self._request(
            Operation("GET", "/billing/plans/{param}/entitlements"),
            path_params=(param_1,),
            query=query,
        )

    def get_billing_prices_lookup_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/prices/lookup/{param}."""
        return self._request(
            Operation("GET", "/billing/prices/lookup/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_billing_subscriptions_by_param_1_entitlements(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/subscriptions/{param}/entitlements."""
        return self._request(
            Operation("GET", "/billing/subscriptions/{param}/entitlements"),
            path_params=(param_1,),
            query=query,
        )

    def get_billing_wallets_by_param_1_balance_real_time(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/wallets/{param}/balance/real-time."""
        return self._request(
            Operation("GET", "/billing/wallets/{param}/balance/real-time"),
            path_params=(param_1,),
            query=query,
        )

    def get_billing_wallets_by_param_1_transactions(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/wallets/{param}/transactions."""
        return self._request(
            Operation("GET", "/billing/wallets/{param}/transactions"),
            path_params=(param_1,),
            query=query,
        )

    def download_billing_invoices_by_param_1_pdf(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> BytesResultT:
        """Call GETRAW /billing/invoices/{param}/pdf."""
        return self._request_bytes(
            Operation("GETRAW", "/billing/invoices/{param}/pdf"),
            path_params=(param_1,),
            query=query,
        )

    def post_billing_invoices_by_param_1_finalize(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /billing/invoices/{param}/finalize."""
        return self._request(
            Operation("POST", "/billing/invoices/{param}/finalize"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_billing_invoices_by_param_1_void(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /billing/invoices/{param}/void."""
        return self._request(
            Operation("POST", "/billing/invoices/{param}/void"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_billing_invoices_preview(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /billing/invoices/preview."""
        return self._request(
            Operation("POST", "/billing/invoices/preview"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_billing_meters_by_param_1_disable(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /billing/meters/{param}/disable."""
        return self._request(
            Operation("POST", "/billing/meters/{param}/disable"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_billing_plans_by_param_1_clone(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /billing/plans/{param}/clone."""
        return self._request(
            Operation("POST", "/billing/plans/{param}/clone"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_billing_subscriptions_by_param_1_activate(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /billing/subscriptions/{param}/activate."""
        return self._request(
            Operation("POST", "/billing/subscriptions/{param}/activate"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_billing_subscriptions_by_param_1_cancel(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /billing/subscriptions/{param}/cancel."""
        return self._request(
            Operation("POST", "/billing/subscriptions/{param}/cancel"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_billing_subscriptions_by_param_1_pause(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /billing/subscriptions/{param}/pause."""
        return self._request(
            Operation("POST", "/billing/subscriptions/{param}/pause"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_billing_subscriptions_by_param_1_resume(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /billing/subscriptions/{param}/resume."""
        return self._request(
            Operation("POST", "/billing/subscriptions/{param}/resume"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_billing_wallets_by_param_1_terminate(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /billing/wallets/{param}/terminate."""
        return self._request(
            Operation("POST", "/billing/wallets/{param}/terminate"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_billing_wallets_by_param_1_top_up(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /billing/wallets/{param}/top-up."""
        return self._request(
            Operation("POST", "/billing/wallets/{param}/top-up"),
            path_params=(param_1,),
            query=query,
            body=body,
        )
