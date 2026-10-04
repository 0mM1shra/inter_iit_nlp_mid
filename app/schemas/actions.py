"""
Pydantic Schemas for Interventions, HITL Decisions, and Audit Logs
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class InterventionProposal(BaseModel):
    intervention_id: str = Field(..., description="Unique intervention ID")
    customer_id: str = Field(..., description="Customer ID")
    action_type: str = Field(..., description="Allowed action enum")
    action_subtype: Optional[str] = Field(None, description="Allowed action subtype enum")
    reason: str = Field(..., description="Natural language justification")
    estimated_cost: float = Field(0.0, description="Estimated execution cost")
    confidence_band: str = Field(..., description="high, medium, low")
    hitl_status: str = Field(..., description="auto_approved, escalated, rejected")
    cited_signals: List[str] = Field(default_factory=list, description="Cited signal keys")
    policy_citations: List[str] = Field(default_factory=list, description="Cited policy references")
    created_at: str = Field(..., description="ISO 8601 creation timestamp")


class HITLDecision(BaseModel):
    decision_id: str = Field(..., description="Decision ID")
    intervention_id: str = Field(..., description="Intervention ID")
    reviewer_id: str = Field(..., description="Human reviewer ID")
    decision: str = Field(..., description="APPROVE, REJECT, MODIFY")
    modified_action: Optional[Dict[str, Any]] = Field(None, description="Modified action if decision is MODIFY")
    comments: Optional[str] = Field(None, description="Reviewer feedback")
    timestamp: str = Field(..., description="ISO 8601 decision timestamp")
