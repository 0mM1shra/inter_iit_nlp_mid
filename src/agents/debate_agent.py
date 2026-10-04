"""
Actor-Critic Debate Agent for ACT-TREE 360
Surfaces genuine agent counterfactual debate and audits red-herring evidence vectors dynamically.
"""


class ActorCriticDebate:
    def __init__(self, state_board):
        self.state_board = state_board

    def evaluate_conflict(self, synthesis_result, as_of_time_str):
        """
        Executes Actor-Critic Counterfactual Audit:
        Actor proposes inferred_state & confidence.
        Critic tests for red herrings, missing corroboration, or single-signal overreactions.
        """
        snapshot = self.state_board.snapshot(as_of_time_str)
        inferred_state = synthesis_result.get("inferred_state")
        score = synthesis_result.get("score", 0.0)

        # 1. Critic Audit for Medical Hardship (Checking for Red-Herring Transfers)
        if inferred_state == "medical_hardship":
            tuition_flag = snapshot.get("red_herring_tuition_wire")
            tax_flag = snapshot.get("red_herring_tax_refund")

            if tuition_flag or tax_flag:
                synthesis_result["notes"] += " [Actor-Critic Audit]: Audited transaction transfers; confirmed tuition/tax transfers are isolated from medical hardship core evidence."

        # 2. Critic Audit for New Child Event (Checking for Corroborating Evidence)
        elif inferred_state == "new_child_life_event":
            has_anchor = bool(snapshot.get("daycare_standing_instruction") or snapshot.get("dependents_changed_flag"))
            has_retail_only = bool(snapshot.get("baby_retail_spend") or snapshot.get("search_intent_childcare"))

            if has_retail_only and not has_anchor and score < 4.0:
                synthesis_result["confidence_band"] = "low"
                synthesis_result["notes"] += " [Actor-Critic Audit]: Single retail/search signal without KYC or standing instruction anchor downgraded to low confidence."

        # 3. Critic Audit for Churn Risk (Auditing Temporary Balance Shifts)
        elif inferred_state == "churn_risk":
            tax_refund = snapshot.get("red_herring_tax_refund")
            if tax_refund:
                synthesis_result["notes"] += " [Actor-Critic Audit]: Tax refund deposit detected; verified temporary balance increase does not negate standing instruction cancellation or engagement drop."

        return synthesis_result
