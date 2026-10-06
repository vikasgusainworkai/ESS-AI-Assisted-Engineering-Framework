# Security Context

## Data Classification
- Public: none
- Internal: employee list (demo data only, fake names)
- Confidential Customer: none in this demo
- Secrets / Credentials: none; the app needs none

## Authentication
- None (demo, local only on 127.0.0.1). Adding it is an architecture change.

## Authorization
- None (demo).

## Tenant Isolation
- Single tenant.

## Forbidden AI Actions
- Expose secrets
- Access unrestricted production data
- Bypass authentication/authorization
- Disable security controls
- Commit credentials
- Edit `data/`, the ticket board, tools or the ESS control plane
