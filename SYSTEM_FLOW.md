# InsuraFlow System Flow

## 1. Architecture Overview

InsuraFlow is split into two applications:

- `server/`: Django REST API with role-based permissions and PostgreSQL persistence
- `client/`: SvelteKit frontend that consumes the API through Axios

Runtime flow:

1. The user interacts with the SvelteKit frontend.
2. The frontend sends requests to `PUBLIC_API_URL`.
3. Django authenticates requests with JWT bearer tokens.
4. Role and verification permissions control access to mutations.
5. PostgreSQL stores users, policies, claims, reports, and settlements.

Redis is present in Docker Compose for infrastructure support, although the current checked-in code does not depend on it for core user flows.

## 2. Authentication And Access Model

### Authentication

- Registration: `POST /api/auth/register/`
- Login: `POST /api/token/` or `POST /api/auth/login/`
- Token refresh: `POST /api/auth/refresh/`
- Current user profile: `GET/PATCH /api/auth/me/`

The frontend stores `access_token`, `refresh_token`, and serialized user data in local storage.

### Verification

Privileged roles are gated by secret keys during registration:

- `admin`
- `provider`
- `agent`
- `surveyor`

Many write operations also require `is_verified = true`. Admins can verify or reject users from the user management screen and API.

## 3. Role Responsibilities In The Current Implementation

### Admin

- Full access to users, policies, claims, settlements, providers, agents, surveyors, and service providers
- Can verify or reject users
- Can create and manage policies
- Can assign surveyors to claims
- Can approve or reject claims
- Can create settlements

### Provider

- Can only manage policies owned by their provider profile
- Can view customers for their own policies
- Can view claims tied to their policies
- Can assign surveyors to claims
- Can manage agents

### Agent

- Sees claims connected to policies they manage
- Can assign surveyors to claims
- Can file claims on behalf of a policy owner through the API
- Can buy a policy on behalf of a customer through the API if `user_id` is supplied
- Does not currently have API permission to create policies, even though the frontend contains a create-policy entry point

### Surveyor

- Sees only claims assigned to them
- Can create inspection reports
- Can approve or reject claims assigned to them

### Customer

- Can browse the public policy catalog
- Can buy policies for themselves
- Can view their own `UserPolicy` records
- Can file claims only against their own active policies
- Can manage their own profile

## 4. Core Domain Models

### User

Custom Django user model with:

- `email` as username field
- `role`
- `phone`
- `address`
- `dob`
- `is_verified`

### Provider / Agent / Surveyor

Role-specific profile models linked to a user.

### Policy

Catalog entry created by a provider or admin with:

- title
- description
- policy type
- coverage amount
- premium amount
- provider
- active flag

### UserPolicy

Purchased instance of a catalog policy:

- linked user
- linked policy
- generated policy number
- purchase/start/end dates
- status
- optional managing agent

### Claim

Filed against a `UserPolicy`:

- customer
- selected user policy
- optional service provider
- claim amount
- claim reason
- documents
- status
- assigned surveyor

### InspectionReport

Created by a surveyor for a claim:

- claim
- surveyor
- inspection date
- damage level
- estimated loss
- remarks
- optional images

### Settlement

Admin-managed payout record:

- claim
- approved amount
- settlement date
- payment mode
- payment status

Creating a settlement automatically marks the claim as `settled`.

## 5. Primary User Flows

### Registration And Verification

1. A user registers through `/register`.
2. If the role is `customer`, no special key is required.
3. If the role is privileged, the matching secret key must be provided.
4. The account is created.
5. Admin can later verify or reject that user from `/users`.

### Login And Session Flow

1. User logs in from `/login`.
2. Frontend receives JWT access and refresh tokens.
3. Frontend fetches `/api/auth/me/`.
4. User data is cached locally.
5. Protected frontend routes under `(app)` redirect to `/login` if there is no authenticated user.

### Policy Discovery And Purchase

1. Public users browse `/` or `/policies`.
2. Policies can be searched, filtered, sorted, and compared in the frontend.
3. Customer purchases a policy through `POST /api/policies/{id}/buy/`.
4. Backend creates a `UserPolicy` with generated policy number and 1-year coverage window.
5. Purchased policy becomes visible in dashboard and policy-related views.

### Claim Filing And Review

1. Customer opens `/claims/new`.
2. They select one of their active `UserPolicy` records.
3. Backend creates a claim with initial status `filed`.
4. Admin, provider, or agent can assign a surveyor.
5. Assignment changes status to `under_review`.
6. Assigned surveyor can inspect, report, and approve or reject the claim.
7. Admin can also approve or reject claims.
8. Admin can create a settlement, which moves the claim to `settled`.

## 6. Frontend Route Map

### Public Routes

- `/`
- `/login`
- `/register`

### Protected App Routes

- `/dashboard`
- `/policies`
- `/policies/new`
- `/policies/edit/[id]`
- `/policies/[id]`
- `/policies/apply`
- `/claims`
- `/claims/new`
- `/claims/[id]`
- `/users`
- `/profile`

## 7. API Grouping

### Accounts

- registration
- login
- token refresh
- current user profile
- admin user management

### Insurance

- providers
- agents
- surveyors
- service providers
- policies
- user policies

### Claims

- claims
- inspection reports
- settlements

## 8. Permission Rules Worth Noting

- Public users can list and view policies.
- Most write operations require both authentication and verification.
- Providers can only update or delete their own policies.
- Customers cannot file claims against policies they do not own.
- Surveyors can only act on claims assigned to them.
- Agents only see user policies linked to their `agent_profile`.

## 9. Current Implementation Notes

- The current docs should treat the backend as PostgreSQL-based.
- Swagger is available at `/swagger/`; ReDoc is available at `/redoc/`.
- The current frontend is deployed as a Node server build, not a static export.
- Some UI affordances are ahead of the API in a few places; when in doubt, backend permissions are the source of truth.
