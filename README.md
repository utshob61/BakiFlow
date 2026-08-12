# 🇧🇩 BakiFlow v1.0
### Premium SME Receivables & Collection Intelligence Platform

BakiFlow is a production-grade financial platform engineered for Bangladeshi SMEs. It transitions businesses from informal "Baki" (credit) notebooks to a high-integrity, data-driven system. Featuring a **Premium Apple-Style Interface**, BakiFlow combines rigorous credit ledger management with deterministic intelligence to optimize cash flow and collection efficiency.

---

## 🌟 What's New in v1.0
*   **🌓 Adaptive Dark Mode:** A sophisticated, Apple-inspired dark theme with zero-flash initialization.
*   **📱 Mobile-First Perfection:** Fully responsive layout designed for the smartphone, the primary tool of SME owners.
*   **🎨 Premium UI/UX:** Glassmorphism navigation, native-feel list views, and high-impact fintech typography.
*   **🛍️ Customer Portal:** Dedicated secure portal for customers to track their own outstanding balances and transaction history.
*   **⚡ Performance Boost:** Optimized static file delivery using WhiteNoise and instant theme state management.

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
       │ (Logic & Events) │      │ (Reliability & Priority) │
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
| **Static Files** | WhiteNoise (High-performance delivery) |
| **Styling** | Custom Apple-Fintech CSS (v1.0), Bootstrap 5 Grid |
| **Logic** | Service-based Architecture (FIFO Allocation) |
| **Security** | 256-bit SSL Ready, Atomic Transactions |

---

## 🚀 Core Features

### 1. High-Integrity Credit Ledger
*   **FIFO Payment Allocation:** Payments automatically clear the oldest outstanding sales first.
*   **Decimal Precision:** Zero floating-point errors. Every Paisa is accounted for using `Decimal` fields.
*   **Overpayment Prevention:** Built-in validation prevents payments exceeding a customer's total outstanding balance.

### 2. Collection Intelligence
*   **Payment Reliability Score (0-100):** A behavioral metric based on on-time payment frequency and average delay days.
*   **Collection Priority Engine:** Ranks overdue accounts (Critical, High, Medium, Low) to tell owners who to call today.
*   **Reliability Progress Bars:** Instant visual indicators of customer trustworthiness in the directory.

### 3. SME Multi-Tenancy
*   **Business Data Isolation:** Robust scoping ensures Business A can never access Business B's customers or financials.
*   **Role-Based Access:** Support for Owners, Staff, and Customers with tailored dashboards.

---

## 🔍 Intelligence Engines

### Payment Reliability Score
- **On-time Payments (30 pts):** Percentage of sales settled before the due date.
- **Consistency (20 pts):** Regularity of repayment behavior over 90 days.
- **Delay Mean (20 pts):** Average number of days past due for late payments.

### Collection Priority Logic
- **Amount Overdue:** Higher balances trigger higher priority levels.
- **Duration:** Ranks accounts by the oldest unpaid invoice age.
- **Behavior Trend:** Factors in the customer's recent Reliability Score.

---

## 🚦 Getting Started

### Prerequisites
*   Python 3.12+
*   PostgreSQL (optional, defaults to SQLite for dev)

### Installation
1. **Clone & Enter:**
   ```bash
   git clone <https://github.com/utshob61/BakiFlow>
   cd BakiFlow
   ```
2. **Setup Environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   cp .env.example .env
   ```
3. **Database & Demo Data:**
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
| `GET` | `/api/v1/customers/` | List business customers with reliability scores |
| `POST` | `/api/v1/credit-sales/` | Log a new credit (Baki) transaction |
| `POST` | `/api/v1/payments/` | Record cash reception & trigger FIFO allocation |
| `GET` | `/api/v1/customers/export_csv/` | Generate exportable Baki ledger |

---

## 🛡 Security & Financial Integrity
*   **Atomic Transactions:** Uses `transaction.atomic()` to ensure data consistency during allocation.
*   **Tenant Isolation:** Middleware ensures all querysets are scoped to the authenticated user's business.
*   **Audit Trail:** Immutable `CreditEvent` log for every single financial movement.

---

## 📈 Roadmap
*   [ ] **AlphaSMS Integration:** Automatic overdue reminders via SMS.
*   [ ] **WhatsApp Ledger:** Export and send customer statements via WhatsApp.
*   [ ] **AI Forecasting:** Cash flow prediction using historical seasonal trends.

---

## 🇧🇩 Proudly Built for Bangladesh
BakiFlow is localized for the unique SME ecosystem in Bangladesh, prioritizing simplicity, speed, and financial transparency.
