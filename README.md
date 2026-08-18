# 🇧🇩 BakiFlow v1.0
### Premium SME Receivables & Collection Intelligence Platform

BakiFlow is a production-grade financial platform engineered for Bangladeshi SMEs. It transitions businesses from informal "Baki" (credit) notebooks to a high-integrity, data-driven system. Featuring a **Premium Apple-Style Interface**, BakiFlow combines rigorous credit ledger management with deterministic intelligence to optimize cash flow and collection efficiency.

---

## 🌟 Key Highlights of v1.0
*   **🤖 Intelligent AI Assistant:** Real-time financial insights via a contextual chatbot—ask about totals, top debtors, or collections.
*   **🌓 Adaptive Dark Mode:** A sophisticated, Apple-inspired dark theme with zero-flash initialization and persistent state management.
*   **📱 Mobile-First Perfection:** Fully responsive layouts (stat cards, grids, and stackable lists) optimized for SME owners on the go.
*   **🎨 High-End Design:** Glassmorphism navigation, native-feel iOS-style list views, and high-impact fintech typography (Inter Extra Bold).
*   **🔐 Atomic Registration:** One-click business onboarding that creates an owner account and business profile in a single atomic transaction.
*   **🛍️ Customer Portal:** Dedicated secure portal where customers can track their own Baki balances and personal transaction history.
*   **⚡ Performance Optimized:** Versioned static assets and high-performance delivery using WhiteNoise.

---

## 🏗 Architecture
BakiFlow utilizes a **Clean Service-Oriented Architecture** within a modular Django monolith to ensure financial logic remains deterministic and testable.

```text
       ┌──────────────────┐
       │   Web Frontend   │ (Django Templates + Vanilla JS + Apple CSS)
       └────────┬─────────┘
                │
       ┌────────▼─────────┐
       │    REST API      │ (Django REST Framework V1)
       └────────┬─────────┘
                │
       ┌────────▼─────────┐      ┌──────────────────────────┐
       │  Service Layer   │─────▶│   Intelligence Engines   │
       │ (Logic & Events) │      │ (Reliability & AI Bot)   │
       └────────┬─────────┘      └──────────────┬───────────┘
                │                               │
       ┌────────▼─────────┐                     │
       │   Domain Models  │◀────────────────────┘
       │ (PostgreSQL/Decimal)
       └──────────────────┘
```

---

## 🛠 Tech Stack
| Layer | Technology |
| :--- | :--- |
| **Backend** | Django 5.0 (Python 3.12+) |
| **API** | Django REST Framework (DRF) |
| **Database** | PostgreSQL (Production), SQLite (Dev) |
| **AI Engine** | Context-Aware Financial Logic (ProcessBot) |
| **Static Files** | WhiteNoise (High-performance delivery) |
| **Styling** | Custom Apple-Fintech CSS (v1.1), Bootstrap 5 Grid |
| **Logic** | Service-based Architecture (FIFO Allocation) |
| **Security** | 256-bit SSL Ready, Atomic Transactions, Tenant Isolation |

---

## 🚀 Core Features

### 1. High-Integrity Credit Ledger
*   **FIFO Payment Allocation:** Automated payment matching against the oldest outstanding sales.
*   **Monetary Precision:** Strict use of `Decimal` for all calculations—zero floating-point errors.
*   **Overpayment Protection:** Real-time validation preventing payments beyond the current balance.

### 2. 🤖 Intelligence Assistant (Chatbot)
*   **Contextual Queries:** Owners can ask natural questions like *"Who owes me the most?"* or *"Total baki summary"*.
*   **Spelling Tolerance:** Handles common SME misspellings (e.g., "debotors") and provides direct, data-driven answers.
*   **Safe Scoping:** The AI only ever sees data belonging to the authenticated business owner.

### 3. Collection Intelligence
*   **Reliability Score (0-100):** Behavioral analysis based on historical payment consistency.
*   **Priority Engine:** Automated ranking (Critical, High, Medium, Low) for daily collection tasks.
*   **Visual Progress:** High-integrity reliability bars embedded directly in customer lists.

### 4. SME Enterprise Multi-Tenancy
*   **Strict Isolation:** Business data is cryptographically and logically isolated between tenants.
*   **Role Hierarchy:** Native support for Owners, Staff, Accountants, and Customers.

---

## 🔍 Intelligence Engines

### Payment Reliability Score
- **On-time Payments (30 pts):** % of sales cleared before the due date.
- **Consistency (20 pts):** Regularity of repayment behavior over the last 90 days.
- **Delay Average (20 pts):** Mean days past due for late payments.

### Collection Priority Logic
- **Amount & Duration:** Weights higher balances and older debts with higher priority.
- **Behavioral Input:** Integrates the customer's reliability trend into the ranking.

---

## 🚦 Getting Started

### Prerequisites
*   Python 3.12+
*   PostgreSQL (Recommended)

### Installation
1. **Clone & Enter:**
   ```bash
   git clone https://github.com/utshob61/BakiFlow.git
   cd BakiFlow
   ```
2. **Setup Environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   cp .env.example .env
   ```
3. **Database Initialization:**
   ```bash
   python manage.py migrate
   python manage.py seed_demo_data
   ```
4. **Run Server:**
   ```bash
   python manage.py runserver
   ```

---

## 📖 API Documentation (V1)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/customers/` | List customers with intelligence metrics |
| `POST` | `/api/v1/chatbot/ask/` | Interact with the AI Financial Assistant |
| `POST` | `/api/v1/payments/` | Record collection & trigger FIFO matching |
| `GET` | `/api/v1/customers/export_csv/` | Export high-integrity ledger as CSV |

---

## 🛡 Security & Integrity
*   **Atomic Transactions:** Guaranteed ledger consistency using `transaction.atomic()`.
*   **Tenant Scoping:** Automatic queryset filtering to prevent cross-business data leaks.
*   **Audit Trail:** Immutable `CreditEvent` logs for every financial movement.

---

## 📈 Roadmap
*   [ ] **AlphaSMS Gateway:** Automated payment reminders via SMS.
*   [ ] **WhatsApp Connect:** Direct sending of statements via WhatsApp.
*   [ ] **Forecasting:** Cash flow prediction using historical seasonal trends.

---

## 🚀 Deployment (Vercel)
BakiFlow is configured for one-click deployment to Vercel.

1.  **Push to GitHub**: Ensure all changes are committed.
2.  **Connect to Vercel**: Import the repository.
3.  **Environment Variables**: Add the following in Vercel:
    *   `SECRET_KEY`: Your production secret.
    *   `DEBUG`: `False`
    *   `DATABASE_URL`: Your PostgreSQL connection string (e.g., Supabase or Neon).
    *   `ALLOWED_HOSTS`: `*`

### 🏗️ Database Migration (Vercel)
Since Vercel is serverless, you need to run migrations against your production database. You can do this by:
1.  Running `python manage.py migrate` locally after pointing your `DATABASE_URL` to your production host.
2.  Or using a temporary build step (though manual migration is safer).
4.  **Build Settings**: Use the default settings; `vercel.json` will handle the routing.

---

## 🇧🇩 Proudly Built for Bangladesh
BakiFlow is localized for the unique SME ecosystem in Bangladesh, prioritizing simplicity, speed, and high-trust financial transparency.
