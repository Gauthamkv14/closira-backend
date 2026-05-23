from typing import List
from .enquiry import EnquiryResponse
from .followup import FollowupResponse
from .history import HistoryEventResponse


class EnquiryDetailResponse(EnquiryResponse):
    """Enquiry response with nested history and followups for the timeline view."""

    history_events: List[HistoryEventResponse] = []
    followups: List[FollowupResponse] = []
