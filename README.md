# InsuraFlow

InsuraFlow is a full-stack insurance management system for customers, providers, agents, surveyors, and admins. It combines a Django REST API with a SvelteKit frontend to manage policy discovery, policy ownership, claims, user verification, and role-based dashboards.

## Current Stack

### Backend
- Django 6
- Django REST Framework
- PostgreSQL
- JWT auth with `djangorestframework-simplejwt`
- `django-filter` for filtering and search
- Swagger/ReDoc via `drf-yasg`
- Gunicorn for production serving

### Frontend
- SvelteKit 2 / Svelte 5
- Tailwind CSS 4
- Axios for API calls
- `@sveltejs/adapter-node` for deployable SSR output
- Lucide icons

### Infrastructure
- Docker Compose
- PostgreSQL 16
- Redis 7

## Repository Layout

```text
InsuraFlow/
|- client/   # SvelteKit frontend
|- server/   # Django backend
|- compose.yml
|- README.md
|- SYSTEM_FLOW.md
```

## Roles In The Current App

- `customer`: browse policies, buy coverage, file claims for owned policies, view personal dashboard and profile
- `provider`: manage only their own policies, view customers for those policies, view related claims, assign surveyors, manage agents
- `agent`: view agent-managed policies and claims, assist customers, assign surveyors, file claims on behalf of policy owners through the API
- `surveyor`: view assigned claims, create inspection reports, approve or reject assigned claims
- `admin`: manage users, verify or reject registrations, access all policies, claims, settlements, providers, agents, surveyors, and service providers

## Main Features

- Public policy catalog with search, filters, sorting, and side-by-side comparison
- Role-specific dashboard under the protected app shell
- JWT-based login, refresh, logout, and current-user profile editing
- Admin user management with verification and rejection flows
- Policy purchase flow that creates `UserPolicy` records
- Claim filing, assignment, approval/rejection, inspection reports, and settlements
- Swagger docs at `/swagger/` and ReDoc at `/redoc/`

## Environment Variables

There are currently three places to be aware of:

### Root `.env`
Used by `docker compose`.

Typical keys:
- `DB_NAME`
- `DB_USER`
- `DB_PASS`
- `SECRET_KEY`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `RESEND_API_KEY` if you use Resend

### `server/.env`
Loaded by Django when you run the backend directly.

Common keys:
- `DB_NAME`
- `DB_USER`
- `DB_PASS`
- `DB_HOST`
- `DB_PORT`
- `SECRET_KEY`
- `FRONTEND_URL`
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`
- `CSRF_TRUSTED_ORIGINS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `RESEND_API_KEY`
- `ADMIN_SECRET_KEY`
- `AGENT_SECRET_KEY`
- `PROVIDER_SECRET_KEY`
- `SURVEYOR_SECRET_KEY`

### `client/.env`
Used by the SvelteKit frontend.

Required key:
- `PUBLIC_API_URL`

Example:

```env
PUBLIC_API_URL=http://127.0.0.1:8000/api
```

Do not keep production secrets or personal mail credentials committed in real deployments. Replace them with environment-specific values.

## Docker Setup

### Prerequisites

- Docker Desktop or another Docker engine with Compose support
- The Docker engine must be running
- A populated root `.env`

### Start The Stack

```bash
docker compose up --build
```

Services started by `compose.yml`:

- PostgreSQL on `5432`
- Redis on `6379`
- Django API on `8000`
- SvelteKit frontend on `5173`

Current container behavior:

- Backend runs migrations, then starts Gunicorn
- Frontend builds and serves the SvelteKit Node output
- Frontend expects the API at `PUBLIC_API_URL=http://localhost:8000/api` inside Compose

## Manual Local Setup

### Backend

Prerequisites:
- Python 3.12
- PostgreSQL running locally

Steps:

```bash
cd server
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The backend will be available at `http://127.0.0.1:8000`.

### Frontend

Prerequisites:
- Node.js 20+
- npm

Steps:

```bash
cd client
npm install
npm run dev
```

The frontend will be available at `http://127.0.0.1:5173`.

## API Surface

Important current endpoints:

- `POST /api/token/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `POST /api/auth/register/`
- `GET/PATCH /api/auth/me/`
- `GET /api/users/`
- `PATCH /api/users/{id}/verify/`
- `PATCH /api/users/{id}/reject/`
- `GET /api/policies/`
- `POST /api/policies/{id}/buy/`
- `GET /api/policies/{id}/customers/`
- `GET /api/user-policies/`
- `GET/POST /api/claims/`
- `POST /api/claims/{id}/assign_surveyor/`
- `POST /api/claims/{id}/approve/`
- `POST /api/claims/{id}/reject/`
- `GET/POST /api/reports/`
- `GET/POST /api/settlements/`

## Deployment Notes

- The frontend now uses `@sveltejs/adapter-node`, so `npm run build` creates `client/build/` for Node-based deployment.
- The backend is configured for PostgreSQL in `server/config/settings.py`; the docs should not assume SQLite fallback.
- For production, set a strong `SECRET_KEY` and configure:
  - `ALLOWED_HOSTS`
  - `FRONTEND_URL`
  - `CORS_ALLOWED_ORIGINS`
  - `CSRF_TRUSTED_ORIGINS`
  - `PUBLIC_API_URL`
- The current Django deploy checks still warn if `SECRET_KEY` is weak or HSTS is not configured.

## Diagnostics

Backend checks:

```bash
cd server
python manage.py check
python manage.py check --deploy
```

Frontend checks:

```bash
cd client
npm run check
npm run build
```

## Current Notes

- There is no `seed_data` management command in the current repository.
- Registration for privileged roles requires secret keys configured in Django settings.
- Protected frontend routes live under `client/src/routes/(app)` and redirect unauthenticated users to `/login`.
