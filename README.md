# ⚡ BakiFlow v1.0 — Receivables Intelligence for SMEs
A premium, high-integrity financial platform designed specifically for Bangladeshi traders to manage informal credit (Baki), improve cash flow, and grow their businesses through data-driven collection intelligence.

🔴 [Live Demo](https://baki-flow.vercel.app/) · 📸 [Screenshots](#-visuals) · 🚀 [Getting Started](#-getting-started) · 🎨 [Style Guide](#-style-guide) · 📖 [API Docs](#-api-documentation)

---

## 📋 Table of Contents
- [✨ About The Project](#-about-the-project)
- [📊 Information Tables](#-information-tables)
- [🧠 Intelligence Engines](#-intelligence-engines)
- [🛠 Tech Stack](#-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [🎨 Style Guide](#-style-guide)
- [🛡 Security & Integrity](#-security--integrity)
- [📚 Extended Documentation](#-extended-documentation)
- [📖 API Documentation](#-api-documentation)
- [📈 Roadmap](#-roadmap)

---

## ✨ About The Project
BakiFlow transitions traditional businesses from paper notebooks and scattered records to a structured, audit-ready financial system. Built with a **Premium Apple-Style Interface**, it provides owners with a sophisticated tool to track receivables, identify collection risks, and interact with an **AI Financial Assistant**.

### 🌟 Key Highlights
*   **Production-Grade Ledger:** Atomic FIFO allocation ensures every Paisa is tracked correctly.
*   **Adaptive Theme:** Seamless transition between zero-flash Light and Dark fintech modes.
*   **SME Multi-Tenancy:** Complete logical isolation between different business entities.
*   **AI Chatbot:** Real-time business insights via a context-aware financial assistant.

---

## 📊 Information Tables

### Page Routes & Access
| Page | Route | Description | Access |
| :--- | :--- | :--- | :--- |
| 🏠 Home | `/` | Responsive landing page and login | Public |
| 📊 Dashboard | `/` (Auth) | Business overview, KPIs, and AI Bot | Owner/Staff |
| 👥 Customers | `/customers/` | CRM directory with reliability scores | Owner/Staff |
| 📖 Ledger | `/credit/` | Transaction history and Baki sales | Owner/Staff |
| 💰 Payments | `/payments/` | Collection records and FIFO tracking | Owner/Staff |
| 🛍️ Portal | `/` (Customer) | Private view for clients to see their balance | Customer |

### CRM Roles & Permissions
| Role | Capabilities | Primary Goal |
| :--- | :--- | :--- |
| **Owner** | Full control, analytics, staff management | Growth & Cash Flow |
| **Staff** | Record sales, add customers, view lists | Operations |
| **Customer** | View personal balance and payment history | Transparency |

---

## 🧠 Intelligence Engines

### 1. Payment Reliability Score (0-100)
Calculated deterministically using behavioral data from the last 90 days.
*   **On-time Payments (30 pts):** % of invoices cleared before the due date.
*   **Consistency (20 pts):** Regularity of repayment intervals.
*   **Delay Mean (20 pts):** Average number of days past due for late payments.

### 2. Collection Priority Engine
Dynamic ranking system used to generate the "Daily Collection Queue."
*   **Critical:** High balance + >30 days overdue + low reliability.
*   **High:** Medium balance + >15 days overdue.
*   **Watch:** New customers or slightly overdue accounts.

---

## 🛠 Tech Stack
| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Backend** | Django 5.0 / Python 3.12 | Core logic, auth, and ORM |
| **API** | REST Framework (DRF) | JSON endpoints for mobile/web |
| **Database** | PostgreSQL | High-integrity relational storage |
| **Static** | WhiteNoise | Production asset delivery |
| **Frontend** | Vanilla JS / Bootstrap 5 | Modern UI without heavy frameworks |
| **Style** | Custom Apple CSS | Premium design tokens and typography |

---

## 📂 Project Structure
```text
BakiFlow/
├── apps/
│   ├── accounts/          # Custom User, Forms, Registration
│   ├── businesses/        # Multi-tenancy & Isolation logic
│   ├── customers/         # CRM & Profile management
│   ├── credit/            # FIFO Ledger & Atomic Services
│   ├── payments/          # Payment allocation engine
│   ├── intelligence/      # AI Bot & Scoring services
│   └── audit/             # Immutable Credit Event logs
├── templates/             # Premium HTML5 Views
├── static/                # CSS/JS Assets (v1.0)
├── config/                # Django Project Settings
└── manage.py              # Management CLI
```

---

## 🚀 Getting Started

### 💻 Local Development
1. **Clone the repository**
   ```bash
   git clone https://github.com/utshob61/BakiFlow.git
   cd BakiFlow
   ```
2. **Setup Environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```
3. **Initialize Database**
   ```bash
   python manage.py migrate
   python manage.py seed_demo_data
   ```
4. **Launch**
   ```bash
   python manage.py runserver
   ```

### ☁️ Cloud Deployment (Vercel)
BakiFlow is optimized for Vercel Serverless.
1. Connect your GitHub fork to Vercel.
2. Add `DATABASE_URL` (Postgres), `SECRET_KEY`, and `DEBUG=False` to Environment Variables.
3. The `vercel.json` file will handle the rest.

---

## 🎨 Style Guide

### 🌓 Color Palette
| Swatch | Hex Code | Usage |
| :--- | :--- | :--- |
| **System Blue** | `#0071e3` | Primary buttons, links, active icons |
| **System Green** | `#34c759` | Success metrics, collections, cleared Baki |
| **System Red** | `#ff3b30` | Overdue alerts, high-risk priority |
| **Pure Dark** | `#0b1120` | Dark mode background (Fintech Night) |

### 🔤 Typography
| Element | Font Family | Weight | Letter Spacing |
| :--- | :--- | :--- | :--- |
| **H1 — Brand** | Inter | 800 (Extra Bold) | -0.05em |
| **Body Text** | Inter | 400 (Regular) | 0 |
| **Stat Labels** | Inter | 700 (Bold) | 0.05em |

---

## 🛡 Security & Integrity
*   **Atomic Transactions:** Prevents partial database updates during complex financial movements.
*   **Tenant Isolation:** Middleware automatically scopes every request to the user's specific business ID.
*   **Forensic Audit:** Every financial change creates an entry in the `CreditEvent` log.

---

## 📚 Extended Documentation
For a deeper dive into the system mechanics, please refer to the following documents:
*   🏗 **[System Architecture](docs/architecture.md)** — Design patterns and multi-tenancy.
*   🧠 **[Reliability Engine](docs/reliability-engine.md)** — Detailed behavioral scoring formula.
*   📊 **[Collection Priority](docs/collection-engine.md)** — Logic for the dynamic risk queue.
*   🔐 **[API Reference](docs/api.md)** — Endpoints for mobile/external integrations.

---

## 📈 Roadmap
*   [ ] **AlphaSMS integration:** Automated overdue SMS alerts.
*   [ ] **WhatsApp Ledger:** Export and send customer statements via WhatsApp API.
*   [ ] **Financial Health 2.0:** Business-wide cash flow forecasting using time-series analysis.

---

## 📖 API Documentation
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/customers/` | List customers with reliability metrics |
| `POST` | `/api/v1/chatbot/ask/` | Query the AI Financial Assistant |
| `POST` | `/api/v1/payments/` | Log payment & trigger FIFO allocation |

---

## 📸 Visuals

### Desktop Overview
<p align="center">
  <img src="docs/screenshots/dashboard_desktop.png" width="800" alt="Main Dashboard">
  <br>
  <img src="docs/screenshots/customer_list.png" width="400" alt="Customer Directory">
  <img src="docs/screenshots/ledger.png" width="400" alt="Informal Ledger">
</p>

### Mobile Experience
<p align="center">
  <img src="docs/screenshots/mobile_dashboard.png" width="250" alt="Mobile Dashboard">
  <img src="docs/screenshots/mobile_ai.png" width="250" alt="Mobile AI Chatbot">
</p>

---

## 🇧🇩 Proudly Built for Bangladesh
BakiFlow is localized for the unique SME ecosystem in Bangladesh, prioritizing simplicity, speed, and high-trust financial transparency.
