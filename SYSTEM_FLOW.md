# InsuraFlow System Flow & Architecture

## 1. System Architecture
InsuraFlow is a modern insurance management system built with:
- **Backend:** Django REST Framework (DRF) with PostgreSQL/SQLite.
- **Frontend:** SvelteKit with TailwindCSS and Lucide icons.
- **Auth:** JWT-based authentication with Email OTP verification.

## 2. Roles & Permissions (RBAC)
- **Admin:** Full system access. Manages users, providers, agents, and surveyors. Approves/rejects claims and assigns surveyors.
- **Provider (Insurer):** Manages the policy catalog. Creates and updates policy plans. Views claims related to their policies.
- **Agent:** Manages assigned customers and their policies. Assists in purchase and claim filing.
- **Surveyor:** Inspects claims. Submits inspection reports (damage level, estimated loss, remarks, images).
- **Customer (User):** Browses and buys policies. Files claims for owned policies. Tracks status in dashboard.

## 3. Core Data Models
### A. Policy System
- **Policy (Catalog):** The public offering. Belongs to a **Provider**. Contains title, type, coverage, and premium.
- **UserPolicy (Instance):** A policy purchased by a **User**. Links a user to a catalog policy. Has a unique policy number, start/end dates, and status (active/expired).

### B. Claim System
- **Claim:** Filed by a **User** against a **UserPolicy**. Contains reason, amount, and documents.
- **InspectionReport:** Submitted by a **Surveyor** for a specific claim.
- **Settlement:** Final payment details created by **Admin** for approved claims.

## 4. Lifecycle Flows

### Purchase Flow
1. **Browse:** Customer explores the **Policies Page** (Catalog).
2. **Compare:** Customer selects up to 3 policies to compare side-by-side.
3. **Buy:** Customer clicks "Buy Now". Backend creates a **UserPolicy** instance.
4. **Dashboard:** New policy appears in the Customer's **Dashboard**.

### Claim Flow
1. **File:** Customer selects an active **UserPolicy** and files a **Claim**.
2. **Assign:** Admin views the new claim and assigns a **Surveyor**. Status becomes `under_review`.
3. **Survey:** Surveyor views assigned claims and submits an **InspectionReport**.
4. **Approval:** Admin reviews the report and **Approves** or **Rejects** the claim.
5. **Settlement:** For approved claims, Admin creates a **Settlement**. Status becomes `settled`.

## 5. Page Responsibilities
- **Homepage:** High-level overview and featured policies.
- **Policies Page:** Advanced exploration, filtering, comparison, and purchase.
- **Dashboard:** Role-specific workspace. Shows owned/managed data only.
- **Claims Page:** Management of claims (filing for customers, reviewing for others).

## 6. Security
- Strict RBAC enforced at the API level via custom DRF permissions.
- Users can only access data they own or are assigned to (e.g., Agents see their clients, Surveyors see assigned claims).
