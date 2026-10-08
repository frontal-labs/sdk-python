"""Pydantic models for cursor-paginated API responses."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import Field

from frontal_sdk.models.types import APIModel, JSONValue

ItemT = TypeVar("ItemT")


class PaginationMeta(APIModel):
    """Cursor and count metadata returned with a page of API results."""

    cursor: str | None = None
    has_more: bool = Field(alias="hasMore")
    total: int | None = None
    limit: int | None = None
    offset: int | None = None


class PageResult(APIModel, Generic[ItemT]):
    """A typed data page with its pagination metadata."""

    data: list[ItemT]
    pagination: PaginationMeta
    meta: JSONValue | None = None
