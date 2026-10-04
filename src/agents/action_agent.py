"""
Action & Offer Agent for ACT-TREE 360
Decides specific bounded interventions from product eligibility policies and state board evidence.
Generates dynamic action recommendations without hardcoded scenario timestamps.
"""


class ActionAgent:
    def __init__(self, memory_engine=None):
        self.memory_engine = memory_engine

        # Policy Action Mapping (Inferred State -> Confidence -> Action Payload)
        self.policy_matrix = {
            "medical_hardship": {
                "high": {
                    "action": "support_intervention",
                    "action_subtype": "medical_hardship_payment_plan",
                    "notes": "High confidence medical hardship confirmed. Recommending medical hardship payment plan support intervention."
                },
                "medium": {
                    "action": "no_action",
                    "action_subtype": None,
                    "notes": "Medical hardship signal accumulating; withholding intervention until high confidence."
                }
            },
            "new_child_life_event": {
                "high": {
                    "action": "personalized_offer",
                    "action_subtype": "childcare_savings_or_insurance_plan",
                    "notes": "New child life event confirmed via anchor signals. Surfacing personalized childcare savings/insurance offer."
                }
            },
            "churn_risk": {
                "high": {
                    "action": "relationship_manager_escalation",
                    "action_subtype": "premium_retention_offer_and_fee_waiver",
                    "notes": "High confidence churn risk detected via standing instruction cancellation and engagement drop. Escalate to relationship manager."
                }
            }
        }

    def decide_action(self, synthesis_result, as_of_time_str, state_board=None):
        inferred_state = synthesis_result.get("inferred_state")
        confidence = synthesis_result.get("confidence_band")

        if inferred_state == "no_significant_event" or confidence == "low":
            return {
                "action": "no_action",
                "action_subtype": None,
                "notes": synthesis_result.get("notes", "Signal confidence insufficient to trigger action.")
            }

        # Handle specific churn stage policy check (proactive retention vs relationship manager escalation)
        if inferred_state == "churn_risk" and confidence == "high" and state_board:
            snapshot = state_board.snapshot(as_of_time_str)
            login_trend = snapshot.get("login_frequency_trend")
            login_val = login_trend.get("value", 0) if login_trend else 0

            # If engagement has severely dropped (login_val <= -0.5), route to proactive retention outreach
            if login_val <= -0.5:
                return {
                    "action": "proactive_retention_outreach",
                    "action_subtype": None,
                    "notes": "Severe engagement drop and churn signals detected; initiating proactive retention outreach."
                }

        state_policies = self.policy_matrix.get(inferred_state, {})
        action_payload = state_policies.get(confidence)

        if action_payload:
            return dict(action_payload)

        return {
            "action": "no_action",
            "action_subtype": None,
            "notes": f"State '{inferred_state}' with confidence '{confidence}' does not satisfy policy action threshold."
        }
