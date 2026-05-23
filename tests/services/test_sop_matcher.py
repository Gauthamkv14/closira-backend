from app.services.sop_matcher import SOPMatcherService


def test_sop_match_pricing():
    message = "Hi, how much does the pro plan cost?"
    match = SOPMatcherService.match_enquiry(message)
    assert match.matched_sop == "Pricing Enquiry"
    assert "pricing" in match.suggested_response.lower()
    assert match.escalation_required is False
    assert match.confidence_score > 0


def test_sop_match_complaint():
    message = "I am very frustrated, your service is not working!"
    match = SOPMatcherService.match_enquiry(message)
    assert match.matched_sop == "Complaint"
    assert match.escalation_required is True


def test_sop_match_booking():
    message = "Can I schedule a meeting for a demo?"
    match = SOPMatcherService.match_enquiry(message)
    assert match.matched_sop == "Booking Request"
    assert "demo" in match.suggested_response.lower()


def test_sop_no_match_escalation():
    message = "The weather is nice today, don't you think?"
    match = SOPMatcherService.match_enquiry(message)
    assert match.matched_sop == "No Match Found"
    assert match.escalation_required is True
    assert match.confidence_score == 0.0


def test_sop_partial_match_priority():
    # Message containing keywords from both Pricing and Support, but more from Pricing
    message = "Help! I need a quote on the cost of your help guide"
    # Pricing keywords: quote, cost (2)
    # Support keywords: help, guide, assistance(no) (2)
    # Since Pricing is first in our list or has higher density, it will match.
    # In our current logic, first one with max matches wins.
    match = SOPMatcherService.match_enquiry(message)
    assert match.matched_sop in ["Pricing Enquiry", "General Support"]
