"""
Pydantic Schemas for Multi-Modal Customer Stream Events
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class StreamEvent(BaseModel):
    event_id: str = Field(..., description="Unique event identifier")
    event_time: str = Field(..., description="ISO 8601 timestamp of event occurrence")
    ingestion_time: Optional[str] = Field(None, description="ISO 8601 timestamp of stream ingestion")
    customer_id: str = Field(..., description="Customer ID scope")
    account_id: Optional[str] = Field(None, description="Associated account ID")
    source_system: str = Field(..., description="Source system: card_payments, ach_wire, core_banking_ledger, web_app_events, support_logs, kyc")
    event_type: str = Field(..., description="Subtype of event")
    schema_version: str = Field("1.0", description="Schema version")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Event-specific attributes")
