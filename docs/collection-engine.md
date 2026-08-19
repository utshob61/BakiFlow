# Collection Priority Engine

The Collection Priority Engine is a deterministic scoring system that identifies which customers require immediate follow-up. It helps SME owners focus their collection efforts where they are most needed.

## 🧠 Scoring logic

The engine assigns a score from **0 to 100** based on three primary vectors:

### 1. Overdue Magnitude (40%)
- **Base Score**: Any amount past due triggers an immediate base score.
- **Thresholds**: 
    - > ৳10,000: +10 pts
    - > ৳50,000: +20 pts
    - > ৳100,000: +30 pts

### 2. Time-Based Risk (40%)
- **Oldest Invoice**: The age of the oldest unpaid credit sale.
- **Tiers**:
    - 1–7 days: Low priority.
    - 8–30 days: Medium priority (+15 pts).
    - 31–90 days: High priority (+30 pts).
    - 90+ days: Critical priority (+40 pts).

### 3. Behavioral Factor (20%)
- **Reliability Inverse**: Customers with a low **Reliability Score** receive an additional priority bump.
- If Reliability < 40%, Priority increases by +20 pts.

## 📊 Priority Levels

| Score | Level | Action Required |
| :--- | :--- | :--- |
| **80+** | 🔴 **CRITICAL** | Call immediately / Suspend credit |
| **60-79** | 🟠 **HIGH** | Send reminder / Schedule visit |
| **40-59** | 🟡 **MEDIUM** | Standard SMS reminder |
| **<40** | 🟢 **LOW** | Routine monitoring |

## 🛠 Implementation
The engine is implemented in `apps/intelligence/services/collection_priority.py`. It is triggered automatically after every new payment or credit sale to ensure the dashboard reflects real-time risk.
