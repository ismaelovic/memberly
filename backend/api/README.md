# API Endpoints

## Subscriptions

- **Purpose**: Manage subscription plans available to tenants.
- **Endpoints**:

  - `GET /subscriptions`: Fetch all active subscription plans.
  - `POST /subscriptions`: Create a new subscription plan.
  - `PUT /subscriptions/{subscription_id}`: Update an existing subscription plan.
  - `DELETE /subscriptions/{subscription_id}`: Delete a subscription plan.

- **Related Models**: `SubscriptionPlan` (defined in `models/subscriptions.py`).

## Memberships

- **Purpose**: Manage memberships linking users to subscription plans.
- **Endpoints**:

  - `GET /memberships`: Fetch all memberships.
  - `POST /memberships`: Create a new membership.
  - `PUT /memberships/{membership_id}`: Update an existing membership.
  - `DELETE /memberships/{membership_id}`: Delete a membership.

- **Related Models**: `Membership` (defined in `models/membership.py`).

## Payments

- **Purpose**: Handle payment processing and tracking.
- **Endpoints**:

  - `GET /payments`: Fetch all payments.
  - `POST /payments`: Process a new payment.
  - `GET /payments/{id}`: Retrieve a specific payment.
  - `GET /payments/membership/{id}`: Fetch payments for a specific membership.

- **Related Models**: `Payment` (defined in `models/payment.py`).
