# BakiFlow System Architecture

BakiFlow is designed with a **Service-Oriented Monolith** architecture. This ensures that while the codebase is easy to manage as a single unit, the business logic is decoupled from the web views, making it testable and robust.

## 🏗 High-Level Structure

```text
┌─────────────────────────────────┐
│        Web / Mobile Client      │
└────────────────┬────────────────┘
                 │
        REST API / HTML Views
                 │
┌────────────────▼────────────────┐
│         Service Layer           │ (Core Logic: FIFO, Scoring)
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│         Domain Models           │ (Relational Data)
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│         PostgreSQL Database     │
└─────────────────────────────────┘
```

## 🛠 Core Components

### 1. Service Layer
All critical financial operations live in service functions (e.g., `apps.credit.services.record_payment`). 
- **Atomic Transactions**: Services use `@transaction.atomic` to ensure data integrity.
- **Side Effects**: Recording a payment automatically triggers FIFO allocation and intelligence score updates.

### 2. Multi-Tenancy (Isolation)
Tenant isolation is enforced at the **QuerySet level**.
- **TenantMixin**: Automatically filters data based on the authenticated user's business membership.
- **Middleware**: Ensures that no cross-business data leakage occurs.

### 3. Financial Integrity
- **Decimal Precision**: All monetary values use `DecimalField` with 2 decimal places to avoid floating-point errors.
- **Audit Logs**: The `audit` app records every `CreditEvent` (Creation, Payment, Adjustment) to maintain a forensic history of all transactions.

### 4. Intelligence Engines
Deterministic algorithms calculate risk and behavior scores asynchronously or on-demand after transactions.
- **Reliability Engine**: Evaluates payment history.
- **Priority Engine**: Determines collection urgency.

## 🚀 Infrastructure
- **Serverless Runtime**: Optimized for **Vercel Python**.
- **Static Assets**: Served via **WhiteNoise** with GZip compression.
- **Security**: 256-bit SSL, CSRF protection, and role-based access control (RBAC).
