"""
Human-In-The-Loop (HITL) Service & Citation Explanation Generator
"""

import uuid
import time
from typing import Dict, Any, List


class HITLService:
    def __init__(self):
        self.pending_interventions: Dict[str, Dict[str, Any]] = {}
        self.decisions_log: List[Dict[str, Any]] = []

    def create_proposal(
        self,
        customer_id: str,
        inferred_state: str,
        confidence_band: str,
        action: str,
        action_subtype: str,
        cited_signals: List[str],
        policy_citations: List[str],
        estimated_cost: float = 0.0
    ) -> Dict[str, Any]:

        proposal_id = f"PROP_{uuid.uuid4().hex[:8].upper()}"

        # Deterministic HITL Routing Evaluation
        if confidence_band == "low" or estimated_cost > 500.0 or action in ["compliance_fraud_hold", "relationship_manager_escalation"]:
            hitl_status = "escalated"
        elif action == "no_action":
            hitl_status = "auto_approved"
        else:
            hitl_status = "escalated" if confidence_band != "high" else "auto_approved"

        proposal = {
            "proposal_id": proposal_id,
            "customer_id": customer_id,
            "inferred_state": inferred_state,
            "confidence_band": confidence_band,
            "action": action,
            "action_subtype": action_subtype,
            "estimated_cost": estimated_cost,
            "hitl_status": hitl_status,
            "cited_signals": cited_signals,
            "policy_citations": policy_citations,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        if hitl_status == "escalated":
            self.pending_interventions[proposal_id] = proposal

        return proposal

    def record_decision(self, proposal_id: str, reviewer_id: str, decision: str, modified_action: Dict[str, Any] = None, comments: str = None) -> Dict[str, Any]:
        proposal = self.pending_interventions.pop(proposal_id, None)
        record = {
            "decision_id": f"DEC_{uuid.uuid4().hex[:8].upper()}",
            "proposal_id": proposal_id,
            "reviewer_id": reviewer_id,
            "decision": decision, # APPROVE, REJECT, MODIFY
            "original_proposal": proposal,
            "modified_action": modified_action,
            "comments": comments,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self.decisions_log.append(record)
        return record
