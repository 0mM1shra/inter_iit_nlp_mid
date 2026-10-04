"""
Shared CustomerState Schema matching production State Board specification
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CustomerState(BaseModel):
    customer_id: str = Field(..., description="Customer ID scope")
    timestamp: str = Field(..., description="ISO 8601 evaluation timestamp")
    current_life_phase: str = Field("no_significant_event", description="Inferred life phase")
    life_phase_confidence: float = Field(0.0, ge=0.0, le=1.0, description="Life phase confidence score")
    churn_risk: float = Field(0.0, ge=0.0, le=1.0, description="Inferred churn risk probability")
    churn_confidence: float = Field(0.0, ge=0.0, le=1.0, description="Churn risk confidence band")
    usage_summary: Dict[str, Any] = Field(default_factory=dict, description="Usage & telemetry summary")
    support_summary: Dict[str, Any] = Field(default_factory=dict, description="Support ticket & sentiment summary")
    transaction_summary: Dict[str, Any] = Field(default_factory=dict, description="Transaction & ledger summary")
    compliance_status: str = Field("CLEARED", description="Compliance / guardrail status")
    active_signals: List[str] = Field(default_factory=list, description="List of active signal keys")
    agent_findings: List[Dict[str, Any]] = Field(default_factory=list, description="Structured agent findings")
    previous_interventions: List[Dict[str, Any]] = Field(default_factory=list, description="Episodic intervention history")
    recommended_action: Optional[Dict[str, Any]] = Field(None, description="Recommended intervention action")
