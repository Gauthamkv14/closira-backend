from enum import Enum


class ChannelType(str, Enum):
    EMAIL = "email"
    CHAT = "chat"
    SOCIAL = "social"


class EnquiryStatus(str, Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    PROCESSED = "processed"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EventType(str, Enum):
    CREATED = "enquiry_created"
    STATUS_CHANGED = "status_changed"
    SOP_MATCHED = "sop_matched"
    ESCALATED = "escalation_triggered"
    FOLLOWUP_SCHEDULED = "followup_scheduled"
    FOLLOWUP_COMPLETED = "followup_completed"
    ERROR = "error"
