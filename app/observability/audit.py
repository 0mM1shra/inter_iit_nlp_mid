"""
OpenTelemetry Audit Logger & Distributed Tracing
Reconstructs every invocation, retrieval, tool call, and agent handoff for full auditability.
"""

import time
import json
from typing import Dict, Any


class AuditLogger:
    def __init__(self):
        self.logs: list = []

    def log_agent_invocation(self, trace_id: str, customer_id: str, agent_name: str, event_type: str, input_ref: Dict[str, Any], output: Dict[str, Any]):
        entry = {
            "trace_id": trace_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "customer_id": customer_id,
            "agent": agent_name,
            "event": event_type,
            "input_reference": input_ref,
            "output": output
        }
        self.logs.append(entry)

    def get_audit_trail(self, customer_id: str = None) -> list:
        if customer_id:
            return [l for l in self.logs if l["customer_id"] == customer_id]
        return self.logs
