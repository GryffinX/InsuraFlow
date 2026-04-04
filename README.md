# InsuraFlow 🛡️

InsuraFlow is a modern, full-stack insurance management ecosystem designed to streamline the lifecycle of insurance policies and claims. Built with a high-performance **Django REST Framework** backend and a reactive **SvelteKit 5** frontend, it provides a seamless experience for customers, providers, agents, and surveyors.

---

## 🎨 Design Philosophy
InsuraFlow features a sophisticated **Purple, Emerald, and Amber** theme, focusing on:
*   **Trust:** Deep purple accents for core professional interactions.
*   **Vitality:** Emerald green for success states and active coverage.
*   **Clarity:** Amber for pending actions and critical alerts.
*   **Modernity:** A "glassmorphism" UI with Inter typography and smooth micro-interactions.

---

## 👥 User Roles & Capabilities

### 🏢 Provider (Insurer)
*   **Catalog Management:** Create, edit, and delete insurance policy plans.
*   **Oversight:** View all claims filed against their specific policies.
*   **Customer Insights:** Access lists of all users who have purchased their coverage.
*   **Claim Processing:** Assign registered surveyors to new claims to begin the review phase.

### 🤝 Agent
*   **Policy Creation:** Design and add new policy plans on behalf of their assigned provider.
*   **Customer Assistance:** View managed policies and track customer claim statuses.
*   **Operational Support:** Assign surveyors to claims to expedite the processing flow.

### 🔍 Surveyor
*   **Task Management:** View a dedicated dashboard of claims specifically assigned to them.
*   **Decision Making:** Approve or Reject claims based on inspection findings.

### 👤 Customer
*   **Discovery:** Browse and search the global policy catalog.
*   **Acquisition:** Purchase insurance plans instantly.
*   **Self-Service:** File claims for owned policies and track their status in real-time.
*   **Profile:** Manage personal information and security settings.

### 🔑 Admin
*   **System Oversight:** Full CRUD access to all users, policies, and claims.
*   **User Verification:** Act as the gatekeeper by approving or rejecting new registrations.

---

## 🚀 Technical Stack

### Backend (Django)
*   **Architecture:** RESTful API with Django REST Framework (DRF).
*   **Security:** JWT (SimpleJWT) with `withCredentials` session persistence.
*   **Database:** PostgreSQL (Production) / SQLite (Local).

### Frontend (SvelteKit 5)
*   **Framework:** Svelte 5 (Runes) for reactive state management.
*   **Styling:** Tailwind CSS 4.0 with a custom-engineered modern theme.
*   **Icons:** Lucide-Svelte for consistent visual language.

---

## 🐳 Docker Setup (Recommended)

The easiest way to run InsuraFlow is using Docker Compose.

### 1. Prerequisites
*   Docker and Docker Compose installed.
*   A `.env` file in the root directory (see `.env.example`).

### 2. Launch the Ecosystem
```bash
docker-compose up --build
```

This will start:
*   **PostgreSQL:** Port `5432`
*   **Redis:** Port `6379`
*   **Django Backend:** Port `8000`
*   **SvelteKit Frontend:** Port `5173`

### 3. Initialize Data
Once the containers are running, open a new terminal and run:
```bash
docker exec -it insuraflow_backend python manage.py seed_data
```

---

## 🛠️ Manual Local Setup

### Backend Setup
1. Navigate to the `/server` directory.
2. Create a virtual environment: `python -m venv venv`.
3. Activate the venv: `source venv/bin/activate` (Mac/Linux) or `.\venv\Scripts\activate` (Windows).
4. Install dependencies: `pip install -r requirements.txt`.
5. Run migrations: `python manage.py migrate`.
6. Start the server: `python manage.py runserver`.

### Frontend Setup
1. Navigate to the `/client` directory.
2. Install dependencies: `npm install`.
3. Start the development server: `npm run dev`.

---

## 🔒 Security Gatekeepers
To maintain platform integrity, privileged roles are protected by **Secret Keys**. These must be provided during registration:
*   **Admin Key:** `admin-secret-2026`
*   **Agent Key:** `agent-secret-2026`
*   **Provider Key:** `provider-secret-2026`
*   **Surveyor Key:** `surveyor-secret-2026`

---

## 🧪 Diagnostic Checks
*   **Backend:** `python manage.py check`
*   **Frontend:** `npm run check`
