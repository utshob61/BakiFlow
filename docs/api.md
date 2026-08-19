# BakiFlow REST API (v1.0)

BakiFlow provides a robust REST API for integration with mobile apps, POS systems, or external accounting software.

## 🔐 Authentication
All API requests require authentication.
- **Session Auth**: Used for the web frontend.
- **Token Auth**: Supported for mobile/external clients.

---

## 👥 Customer Endpoints

### List Customers
`GET /api/v1/customers/`
Returns a list of all customers for the authenticated business.
- **Includes**: Reliability scores, current balance, and contact info.

### Get Customer Detail
`GET /api/v1/customers/{id}/`
Returns detailed profile for a single customer.

---

## 💰 Transaction Endpoints

### Create Credit Sale (Baki)
`POST /api/v1/credit-sales/`
Records a new credit transaction.
- **Payload**:
  ```json
  {
    "customer": 12,
    "amount": "1500.00",
    "sale_date": "2026-08-19",
    "due_date": "2026-09-02",
    "description": "Textile raw materials"
  }
  ```

### Record Payment
`POST /api/v1/payments/`
Records cash collection and triggers FIFO allocation.
- **Payload**:
  ```json
  {
    "customer": 12,
    "amount": "1000.00",
    "method": "CASH",
    "payment_date": "2026-08-20"
  }
  ```

---

## 🤖 Intelligence Endpoints

### Query AI Assistant
`POST /api/v1/chatbot/ask/`
Returns contextual financial insights.
- **Payload**: `{"query": "total outstanding balance"}`

---

## 📥 Export Endpoints

### Export CSV Ledger
`GET /api/v1/customers/export_csv/`
Generates a high-integrity CSV file of the current receivables ledger.
