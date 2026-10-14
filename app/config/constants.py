from enum import StrEnum


class UserRole(StrEnum):
    BUYER = "buyer"
    SELLER = "seller"
    ADMIN = "admin"


class BuyerTier(StrEnum):
    BASIC = "basic"
    ULTRA = "ultra"
    PRO = "pro"


class ProductStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class OrderStatus(StrEnum):
    PENDING_PAYMENT = "pending_payment"
    PAID = "paid"
    PARTIALLY_REFUNDED = "partially_refunded"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class SellerOrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    FULFILLED = "fulfilled"
    REFUNDED = "refunded"


class PaymentStatus(StrEnum):
    REQUIRES_PAYMENT_METHOD = "requires_payment_method"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"


class SubscriptionStatus(StrEnum):
    INCOMPLETE = "incomplete"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"


class LedgerAccountType(StrEnum):
    ASSET = "asset"
    LIABILITY = "liability"
    REVENUE = "revenue"
    EXPENSE = "expense"


class LedgerAccountCode(StrEnum):
    STRIPE_CLEARING = "STRIPE_CLEARING"
    SELLER_PAYABLE = "SELLER_PAYABLE"
    PLATFORM_REVENUE = "PLATFORM_REVENUE"
    DISCOUNT_EXPENSE = "DISCOUNT_EXPENSE"
    STRIPE_FEE_EXPENSE = "STRIPE_FEE_EXPENSE"
    REFUND_LIABILITY = "REFUND_LIABILITY"
    SUBSCRIPTION_REVENUE = "SUBSCRIPTION_REVENUE"


class LedgerDirection(StrEnum):
    DEBIT = "debit"
    CREDIT = "credit"


class ReconciliationIssueType(StrEnum):
    MISSING_LOCAL = "missing_local"
    MISSING_STRIPE = "missing_stripe"
    AMOUNT_MISMATCH = "amount_mismatch"
    STATUS_MISMATCH = "status_mismatch"
