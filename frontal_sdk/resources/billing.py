"""Typed API resource for the billing endpoints."""

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


class Billing(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the billing API endpoints."""

    def list_addon_entitlements(
        self, addon_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/addons/{param}/entitlements."""
        return self._request(
            Operation("GET", "/billing/addons/{param}/entitlements"),
            path_params=(addon_id,),
            query=query,
        )

    def list_customer_entitlements(
        self, customer_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/customers/{param}/entitlements."""
        return self._request(
            Operation("GET", "/billing/customers/{param}/entitlements"),
            path_params=(customer_id,),
            query=query,
        )

    def get_customer_invoices_summary(
        self, customer_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/customers/{param}/invoices/summary."""
        return self._request(
            Operation("GET", "/billing/customers/{param}/invoices/summary"),
            path_params=(customer_id,),
            query=query,
        )

    def get_customer_usage(
        self, customer_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/customers/{param}/usage."""
        return self._request(
            Operation("GET", "/billing/customers/{param}/usage"),
            path_params=(customer_id,),
            query=query,
        )

    def list_customer_wallets(
        self, customer_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/customers/{param}/wallets."""
        return self._request(
            Operation("GET", "/billing/customers/{param}/wallets"),
            path_params=(customer_id,),
            query=query,
        )

    def get_portal(
        self, portal_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/customers/portal/{param}."""
        return self._request(
            Operation("GET", "/billing/customers/portal/{param}"),
            path_params=(portal_id,),
            query=query,
        )

    def list_plan_entitlements(
        self, plan_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/plans/{param}/entitlements."""
        return self._request(
            Operation("GET", "/billing/plans/{param}/entitlements"),
            path_params=(plan_id,),
            query=query,
        )

    def get_lookup(
        self, lookup_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/prices/lookup/{param}."""
        return self._request(
            Operation("GET", "/billing/prices/lookup/{param}"),
            path_params=(lookup_id,),
            query=query,
        )

    def list_subscription_entitlements(
        self, subscription_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/subscriptions/{param}/entitlements."""
        return self._request(
            Operation("GET", "/billing/subscriptions/{param}/entitlements"),
            path_params=(subscription_id,),
            query=query,
        )

    def get_wallet_balance_real_time(
        self, wallet_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/wallets/{param}/balance/real-time."""
        return self._request(
            Operation("GET", "/billing/wallets/{param}/balance/real-time"),
            path_params=(wallet_id,),
            query=query,
        )

    def list_wallet_transactions(
        self, wallet_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /billing/wallets/{param}/transactions."""
        return self._request(
            Operation("GET", "/billing/wallets/{param}/transactions"),
            path_params=(wallet_id,),
            query=query,
        )

    def download_invoice_pdf(
        self, invoice_id: str, *, query: QueryParams | None = None
    ) -> BytesResultT:
        """Call GETRAW /billing/invoices/{param}/pdf."""
        return self._request_bytes(
            Operation("GETRAW", "/billing/invoices/{param}/pdf"),
            path_params=(invoice_id,),
            query=query,
        )

    def finalize_invoice(
        self,
        invoice_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /billing/invoices/{param}/finalize."""
        return self._request(
            Operation("POST", "/billing/invoices/{param}/finalize"),
            path_params=(invoice_id,),
            query=query,
            body=body,
        )

    def void_invoice(
        self,
        invoice_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /billing/invoices/{param}/void."""
        return self._request(
            Operation("POST", "/billing/invoices/{param}/void"),
            path_params=(invoice_id,),
            query=query,
            body=body,
        )

    def post_billing_invoices_preview(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /billing/invoices/preview."""
        return self._request(
            Operation("POST", "/billing/invoices/preview"),
            path_params=(),
            query=query,
            body=body,
        )

    def disable_meter(
        self,
        meter_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /billing/meters/{param}/disable."""
        return self._request(
            Operation("POST", "/billing/meters/{param}/disable"),
            path_params=(meter_id,),
            query=query,
            body=body,
        )

    def clone_plan(
        self,
        plan_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /billing/plans/{param}/clone."""
        return self._request(
            Operation("POST", "/billing/plans/{param}/clone"),
            path_params=(plan_id,),
            query=query,
            body=body,
        )

    def activate_subscription(
        self,
        subscription_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /billing/subscriptions/{param}/activate."""
        return self._request(
            Operation("POST", "/billing/subscriptions/{param}/activate"),
            path_params=(subscription_id,),
            query=query,
            body=body,
        )

    def cancel_subscription(
        self,
        subscription_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /billing/subscriptions/{param}/cancel."""
        return self._request(
            Operation("POST", "/billing/subscriptions/{param}/cancel"),
            path_params=(subscription_id,),
            query=query,
            body=body,
        )

    def pause_subscription(
        self,
        subscription_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /billing/subscriptions/{param}/pause."""
        return self._request(
            Operation("POST", "/billing/subscriptions/{param}/pause"),
            path_params=(subscription_id,),
            query=query,
            body=body,
        )

    def resume_subscription(
        self,
        subscription_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /billing/subscriptions/{param}/resume."""
        return self._request(
            Operation("POST", "/billing/subscriptions/{param}/resume"),
            path_params=(subscription_id,),
            query=query,
            body=body,
        )

    def terminate_wallet(
        self,
        wallet_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /billing/wallets/{param}/terminate."""
        return self._request(
            Operation("POST", "/billing/wallets/{param}/terminate"),
            path_params=(wallet_id,),
            query=query,
            body=body,
        )

    def top_up_wallet(
        self,
        wallet_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /billing/wallets/{param}/top-up."""
        return self._request(
            Operation("POST", "/billing/wallets/{param}/top-up"),
            path_params=(wallet_id,),
            query=query,
            body=body,
        )
