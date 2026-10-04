"""
Pydantic Schemas for Agent Findings & Epistemic Assertions
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class AgentFinding(BaseModel):
    finding_id: str = Field(..., description="Unique finding ID")
    customer_id: str = Field(..., description="Customer ID scope")
    agent_name: str = Field(..., description="Name of agent publishing assertion")
    finding_type: str = Field(..., description="Type of assertion / feature key")
    finding_value: Any = Field(..., description="Assertion value")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    timestamp: str = Field(..., description="ISO 8601 timestamp of assertion")
    expires_at: Optional[str] = Field(None, description="Expiration timestamp based on half-life decay")
