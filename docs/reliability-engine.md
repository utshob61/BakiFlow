# Payment Reliability Engine

The Payment Reliability Score is a 0-100 metric that reflects a customer's payment behavior.

## Scoring Formula

- **On-time Payments (30 points)**: Percentage of credit sales paid in full by the due date.
- **Payment Consistency (20 points)**: Regularity of payments over time.
- **Average Delay (20 points)**: Average number of days past the due date for late payments.
- **Recent Behavior (15 points)**: Weighted score for behavior in the last 90 days.
- **Outstanding Trend (15 points)**: Analysis of whether the customer's balance is increasing or decreasing.

## Implementation
The logic is implemented in `apps/intelligence/services/reliability.py`.
It is calculated deterministically and stored in the `ReliabilityScore` model.
