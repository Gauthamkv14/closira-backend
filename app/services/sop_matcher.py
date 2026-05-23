from typing import Dict


class SOPMatch:
    def __init__(
        self,
        name: str,
        suggested_response: str,
        escalate: bool = False,
        confidence: float = 0.0,
    ):
        self.matched_sop = name
        self.suggested_response = suggested_response
        self.escalation_required = escalate
        self.confidence_score = confidence

    def to_dict(self) -> Dict:
        return {
            "matched_sop": self.matched_sop,
            "suggested_response": self.suggested_response,
            "escalation_required": self.escalation_required,
            "confidence_score": self.confidence_score,
        }


class SOPMatcherService:
    """
    Keyword-based SOP matcher for customer enquiries.

    This service simulates AI analysis by matching message content against
    predefined keywords for specific Standard Operating Procedures (SOPs).
    """

    SOPS = [
        {
            "name": "Pricing Enquiry",
            "keywords": ["price", "cost", "quote", "pricing", "how much", "rate"],
            "response": "Our pricing plans start at $29/mo for the starter tier. You can view full details at closira.com/pricing.",
            "escalate": False,
        },
        {
            "name": "Booking Request",
            "keywords": [
                "book",
                "demo",
                "schedule",
                "meeting",
                "appointment",
                "reserve",
            ],
            "response": "I'd be happy to help you schedule a demo. Please use our calendar link here: closira.com/demo-booking",
            "escalate": False,
        },
        {
            "name": "Complaint",
            "keywords": [
                "bad",
                "issue",
                "fault",
                "disappointed",
                "complaint",
                "not working",
                "refund",
                "frustrated",
            ],
            "response": "We're sincerely sorry to hear about your experience. Our management team has been alerted and will prioritize your request.",
            "escalate": True,  # Complaints are automatically escalated for human review
        },
        {
            "name": "After-Hours Support",
            "keywords": ["tonight", "weekend", "after hours", "holiday", "closed"],
            "response": "Our official support hours are 9 AM - 6 PM EST. We've received your message and will get back to you during our next shift.",
            "escalate": False,
        },
        {
            "name": "General Support",
            "keywords": [
                "help",
                "question",
                "support",
                "how to",
                "assistance",
                "guide",
            ],
            "response": "Thanks for your enquiry! A support specialist has been assigned to your case and will respond shortly.",
            "escalate": False,
        },
    ]

    @classmethod
    def match_enquiry(cls, message: str) -> SOPMatch:
        """
        Matches a message against defined SOPs using simple keyword lookup.
        Returns the best matching SOP or a default escalation if no match is found.
        """
        message_lower = message.lower()
        best_match = None
        max_keywords_found = 0

        for sop in cls.SOPS:
            # Count how many keywords from this SOP appear in the message
            matches = sum(1 for keyword in sop["keywords"] if keyword in message_lower)

            if matches > max_keywords_found:
                max_keywords_found = matches
                best_match = sop

        if best_match and max_keywords_found > 0:
            # Confidence is a simple ratio of matching keywords (max capped at 1.0)
            confidence = min(max_keywords_found / 3.0, 1.0)
            return SOPMatch(
                name=best_match["name"],
                suggested_response=best_match["response"],
                escalate=best_match["escalate"],
                confidence=confidence,
            )

        # Fallback: If no match found, we MUST escalate for human review
        return SOPMatch(
            name="No Match Found",
            suggested_response="I'm unable to automatically categorize your request. A team member will review this manually.",
            escalate=True,
            confidence=0.0,
        )
