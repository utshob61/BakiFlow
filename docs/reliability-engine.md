# Payment Reliability Engine

The Payment Reliability Score is a 0-100 metric that reflects a customer's payment behavior based on historical performance. It provides SME owners with a "Trust Score" for each client.

## 📐 Scoring Formula

The final score is a weighted average of the following components:

### 1. On-time Payments (30 points)
Calculates the percentage of credit sales that were fully cleared by their due date.
- `(On-time Sales / Total Sales) * 30`

### 2. Payment Consistency (20 points)
Measures the regularity of payments. Frequent, small payments are often more reliable than irregular large ones.
- Analyzes the standard deviation of payment intervals.

### 3. Average Delay (20 points)
Calculates the mean number of days past the due date for all late payments.
- 0 days: 20 pts
- 1–15 days: 10 pts
- 15+ days: 0 pts

### 4. Recent Behavior (15 points)
A weighted score focusing on the last 90 days of activity. This detects if a previously reliable customer is starting to "slip."

### 5. Outstanding Trend (15 points)
Analyzes the direction of the customer's total balance.
- **Improving**: Balance decreasing month-over-month.
- **Degrading**: Balance increasing without corresponding payments.

## 📊 Visual Representation
In the customer directory, this score is shown as a high-integrity progress bar:
- **70%+**: 🟢 Excellent
- **40-69%**: 🟡 Fair
- **<40%**: 🔴 Risky

## 🛠 Implementation
The logic is implemented in `apps/intelligence/services/reliability.py`. It uses `django.db.models` aggregates to process historical data efficiently.
