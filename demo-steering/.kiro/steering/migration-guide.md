---
inclusion: manual
description: "Migration guide for upgrading from v1 to v2 API — activate manually when performing migration work"
---

# Migration Guide: v1 to v2 API

## Overview

This guide covers the breaking changes between API v1 and v2, and provides step-by-step instructions for migrating existing code.

## Breaking Changes

### 1. Authentication

- **v1**: API key passed as query parameter `?api_key=xxx`
- **v2**: API key passed as `Authorization: Bearer xxx` header
- **Action**: Update all HTTP client configurations to use header-based auth

### 2. Response Format

- **v1**: Flat JSON response `{"id": "123", "name": "item"}`
- **v2**: Wrapped response `{"data": {"id": "123", "name": "item"}, "meta": {"version": "2.0"}}`
- **Action**: Update all response parsers to unwrap the `data` field

### 3. Endpoint Paths

- **v1**: `/api/items/{id}`
- **v2**: `/api/v2/items/{id}`
- **Action**: Update base URL configuration or add version prefix to all paths

### 4. Pagination

- **v1**: Offset-based `?offset=0&limit=20`
- **v2**: Cursor-based `?cursor=abc123&limit=20`
- **Action**: Replace offset tracking with cursor storage from response `meta.next_cursor`

## Migration Steps

1. Update authentication headers in HTTP client configuration
2. Add response unwrapping middleware or update individual parsers
3. Update base URL to include `/v2/` prefix
4. Replace offset-based pagination with cursor-based logic
5. Run integration tests against v2 staging endpoint
6. Update error handling for new error response format
7. Deploy and monitor for 4xx errors indicating missed endpoints

## Rollback Plan

If issues arise after migration:
1. Revert authentication to query parameter style (v1 still accepts both during transition)
2. Switch base URL back to v1 prefix
3. v1 endpoints remain available until the published deprecation date
