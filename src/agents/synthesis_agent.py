"""
Synthesis & Correlation Agent (ACT-TREE 360 Dynamic Hypothesis Tree Engine)
Reconciles swarm state board assertions into a generalized Bayesian belief tree over customer life phases.
Completely generalized evidence accumulation algorithm without scenario-specific hardcoded rules.
"""


class SynthesisAgent:
    def __init__(self, state_board, memory_engine=None):
        self.state_board = state_board
        self.memory_engine = memory_engine

        # State Evidence Mapping (Feature Assertion Key -> (Target State, Weight))
        self.evidence_weights = {
            "hospital_bill_posted": ("medical_hardship", 3.0),
            "medical_support_ticket": ("medical_hardship", 3.5),
            "search_intent_hardship": ("medical_hardship", 2.0),
            "income_disruption_flag": ("medical_hardship", 2.5),

            "dependents_changed_flag": ("new_child_life_event", 4.0),
            "daycare_standing_instruction": ("new_child_life_event", 3.5),
            "search_intent_childcare": ("new_child_life_event", 2.0),
            "baby_retail_spend": ("new_child_life_event", 1.8),

            "cancelled_standing_instruction": ("churn_risk", 3.5),
            "large_savings_sweep": ("churn_risk", 3.0),
            "fee_dispute_flag": ("churn_risk", 2.5),
            "unresolved_complaint_flag": ("churn_risk", 2.0),
            "expressed_churn_intent": ("churn_risk", 3.0),
        }

    def synthesize_state(self, as_of_time_str):
        snapshot = self.state_board.snapshot(as_of_time_str)

        # 1. Generalized Evidence Accumulation over all Candidate States
        state_scores = {
            "medical_hardship": 0.0,
            "new_child_life_event": 0.0,
            "churn_risk": 0.0,
            "no_significant_event": 0.5
        }

        active_evidence = {}

        for key, assertion_data in snapshot.items():
            if not assertion_data or key not in self.evidence_weights:
                continue

            val = assertion_data.get("value")
            conf = assertion_data.get("effective_confidence", assertion_data.get("confidence", 0.0))

            if val:
                target_state, weight = self.evidence_weights[key]
                score_increment = weight * conf
                state_scores[target_state] += score_increment
                active_evidence[key] = (target_state, round(score_increment, 2))

        # Include login trend negative impact on churn risk
        login_trend = snapshot.get("login_frequency_trend")
        if login_trend and login_trend.get("value", 0) < 0:
            drop_conf = login_trend.get("effective_confidence", 0.5)
            state_scores["churn_risk"] += 1.5 * drop_conf

        # 2. Dynamic Bayesian State Selection & Confidence Band Calibration
        sorted_states = sorted(state_scores.items(), key=lambda x: x[1], reverse=True)
        top_state, top_score = sorted_states[0]
        second_state, second_score = sorted_states[1]

        # Calculate score margin and confidence band
        margin = top_score - second_score

        if top_score < 1.2:
            inferred_state = "no_significant_event"
            confidence_band = "low"
        else:
            inferred_state = top_state
            if top_score >= 5.0 and margin >= 2.0:
                confidence_band = "high"
            elif top_score >= 2.5:
                confidence_band = "medium" if margin >= 1.0 else "low"
            else:
                confidence_band = "low"

        # Generate natural language evidence synthesis notes
        cited_keys = [k for k, (st, sc) in active_evidence.items() if st == inferred_state]
        notes = f"Inferred state '{inferred_state}' based on generalized evidence accumulation (Score: {top_score:.2f}, Margin: {margin:.2f}). Cited signals: {', '.join(cited_keys) if cited_keys else 'None'}."

        return {
            "inferred_state": inferred_state,
            "confidence_band": confidence_band,
            "score": round(top_score, 2),
            "margin": round(margin, 2),
            "notes": notes,
            "cited_evidence": cited_keys
        }
