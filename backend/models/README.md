# Models Summary

## Users

- **Purpose**: Represents all users in the system, including members, staff, and admins.
- **Fields**:
  - `id`: Primary key.
  - `tenant_id`: Foreign key linking to the tenant.
  - `email`: Contact email (unique per tenant).
  - `first_name`, `last_name`: User's name.
  - `role`: Role of the user (e.g., `system_admin`, `tenant_admin`, `staff`, `member`).
  - `is_active`: Indicates if the account is active.
  - `hashed_password`: Encrypted password (nullable for members without system access).

## SubscriptionPlan

- **Purpose**: Defines subscription plans available to tenants. This model is now located in `models/subscriptions.py`.
- **Fields**:
  - `id`: Primary key.
  - `tenant_id`: Foreign key linking to the tenant.
  - `name`: Plan name (e.g., Basic, Premium).
  - `description`: Optional description of the plan.
  - `price`: Cost of the plan.
  - `duration_months`: Duration of the plan in months.
  - `is_active`: Indicates if the plan is active.
  - `is_popular`: Indicates if the plan is marked as popular.
  - `features`: JSON field for subscription features as a list.
  - `created_at`: Timestamp of creation.
  - `updated_at`: Timestamp of last update.

## Membership

- **Purpose**: Links accounts to subscription plans.
- **Fields**:
  - `id`: Primary key.
  - `member_id`: Foreign key linking to the account.
  - `plan_id`: Foreign key linking to the subscription plan.
  - `adjusted_price`: Manually adjusted price for the subscription (nullable).
  - `start_date`, `end_date`: Subscription period.
  - `is_active`: Indicates if the membership is active.

## Payment

- **Purpose**: Tracks payments made by accounts.
- **Fields**:
  - `id`: Primary key.
  - `member_id`: Foreign key linking to the account.
  - `membership_id`: Foreign key linking to the membership.
  - `tenant_id`: Foreign key linking to the tenant.
  - `amount`: Payment amount.
  - `payment_date`: Date of payment.
  - `payment_method`: Method of payment (e.g., Credit Card).
  - `status`: Payment status (e.g., Pending, Completed, Failed).
  - `coverage_start_date`, `coverage_end_date`: Period the payment covers.

## Tenant

- **Purpose**: Represents a tenant in the multi-tenant system.
- **Fields**:
  - `id`: Primary key.
  - `name`: Tenant's name.

## Communication

- **Purpose**: Tracks communication sent to accounts.
- **Fields**:
  - `id`: Primary key.
  - `member_id`: Foreign key linking to the account.
  - `tenant_id`: Foreign key linking to the tenant.
  - `type`: Type of communication (e.g., Email, SMS).
  - `content`: Message content.
  - `status`: Delivery status (e.g., Sent, Failed).
  - `sent_at`: Timestamp of when the communication was sent.
