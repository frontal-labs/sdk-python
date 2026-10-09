"""Cursor pagination helpers shared by every API domain."""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from typing import TypeVar

from frontal_sdk.core.errors import FrontalError
from frontal_sdk.models import PageResult, QueryParams, QueryValue

ItemT = TypeVar("ItemT")
PageFetcher = Callable[[QueryParams], PageResult[ItemT]]
AsyncPageFetcher = Callable[[QueryParams], Awaitable[PageResult[ItemT]]]


def paginate(
    fetch_page: PageFetcher[ItemT],
    *,
    query: QueryParams | None = None,
    cursor_param: str = "cursor",
    max_pages: int | None = None,
) -> Iterator[ItemT]:
    """Yield items from successive cursor pages.

    ``fetch_page`` receives the original query on the first call and that query
    plus the returned cursor on each following call.
    """
    _validate_pagination(cursor_param, max_pages)
    params: dict[str, QueryValue] = dict(query or {})
    seen_cursors: set[str] = set()
    page_number = 0
    while True:
        page = fetch_page(params)
        yield from page.data
        page_number += 1
        if not page.pagination.has_more or (
            max_pages is not None and page_number >= max_pages
        ):
            return
        cursor = page.pagination.cursor
        if not cursor or cursor in seen_cursors:
            raise FrontalError("The API returned a missing or repeated page cursor")
        seen_cursors.add(cursor)
        params[cursor_param] = cursor


async def async_paginate(
    fetch_page: AsyncPageFetcher[ItemT],
    *,
    query: QueryParams | None = None,
    cursor_param: str = "cursor",
    max_pages: int | None = None,
) -> AsyncIterator[ItemT]:
    """Asynchronously yield items from successive cursor pages."""
    _validate_pagination(cursor_param, max_pages)
    params: dict[str, QueryValue] = dict(query or {})
    seen_cursors: set[str] = set()
    page_number = 0
    while True:
        page = await fetch_page(params)
        for item in page.data:
            yield item
        page_number += 1
        if not page.pagination.has_more or (
            max_pages is not None and page_number >= max_pages
        ):
            return
        cursor = page.pagination.cursor
        if not cursor or cursor in seen_cursors:
            raise FrontalError("The API returned a missing or repeated page cursor")
        seen_cursors.add(cursor)
        params[cursor_param] = cursor


def _validate_pagination(cursor_param: str, max_pages: int | None) -> None:
    if not isinstance(cursor_param, str) or not cursor_param.strip():
        raise ValueError("cursor_param must not be empty")
    if max_pages is not None:
        if isinstance(max_pages, bool) or not isinstance(max_pages, int):
            raise TypeError("max_pages must be an integer")
        if max_pages < 1:
            raise ValueError("max_pages must be positive")
