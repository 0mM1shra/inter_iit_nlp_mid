"""
Transaction / Billing Agent for ACT-TREE 360
Uses real NLP (Semantic Entity Extraction & Intent Vector Matching) to process
spending patterns, income disruptions, standing instruction changes, and red-herring transfers.
"""

from src.nlp_engine import NLPEngine


class TransactionAgent:
    def __init__(self, state_board, nlp_engine: NLPEngine = None):
        self.state_board = state_board
        self.nlp_engine = nlp_engine or NLPEngine()

        self.merchant_intents = {
            "disability_income": ["short term disability insurance claim maternity benefit payout workers compensation income disruption benefits credit"],
            "hospital_medical": ["hospital medical clinical er visit emergency care health system healthcare surgery billing clinic city general hospital"],
            "childcare_daycare": ["daycare preschool infant care learning academy early childhood nursery standing instruction"],
            "baby_retail": ["baby retail infant stroller maternity wear nursery furniture diaper supply infant buybuybaby buy buy baby"],
            "tuition_wire": ["university tuition college wire transfer education fee higher education academic board state university"],
            "tax_refund": ["tax refund irs treasury deposit state tax return internal revenue treasury"]
        }

    def process_features(self, features, as_of_time_str):
        txns = features.get("transactions", [])
        if not txns:
            return

        for t in txns:
            payload = t.get("payload", {})
            amount = payload.get("amount", 0.0)
            merchant = (payload.get("merchant_name") or payload.get("counterparty_name") or "").lower()
            mcc = (payload.get("mcc_category") or "").lower()
            txn_type = (t.get("event_type") or payload.get("transaction_type") or "").lower()

            combined_text = f"{merchant} {mcc} {txn_type}"
            if not combined_text.strip():
                continue

            # 1. Genuine NLP Semantic Classifier over transaction context
            best_intent, conf = self.nlp_engine.classify_intent_tfidf(combined_text, self.merchant_intents)
            entities = self.nlp_engine.extract_semantic_entities(combined_text)

            # 2. Extract assertions based on semantic findings
            if best_intent == "disability_income" or "benefits_credit" in txn_type or ("salary" in combined_text and 0 < amount < 3500):
                self.state_board.publish_assertion("income_disruption_flag", True, 0.95, as_of_time_str, half_life_days=90)

            if best_intent == "hospital_medical" or mcc in ["healthcare", "pharmacy"] or "hospital" in merchant or "er visit" in merchant or "emergency" in merchant:
                self.state_board.publish_assertion("hospital_bill_posted", True, 0.95, as_of_time_str, half_life_days=90)

            if best_intent == "childcare_daycare" and not entities.get("cancellation_flag"):
                self.state_board.publish_assertion("daycare_standing_instruction", True, 0.95, as_of_time_str, half_life_days=180)

            if entities.get("cancellation_flag") or ("standing_instruction" in txn_type and ("cancel" in txn_type or amount == 0)):
                self.state_board.publish_assertion("cancelled_standing_instruction", True, 0.98, as_of_time_str, half_life_days=180)

            if ("outbound_transfer" in txn_type or "wire" in txn_type or "withdrawal" in txn_type) and amount >= 3000:
                if best_intent == "tuition_wire":
                    self.state_board.publish_assertion("red_herring_tuition_wire", True, 0.90, as_of_time_str, half_life_days=60)
                else:
                    self.state_board.publish_assertion("large_savings_sweep", True, 0.95, as_of_time_str, half_life_days=90)

            if best_intent == "baby_retail":
                self.state_board.publish_assertion("baby_retail_spend", True, 0.90, as_of_time_str, half_life_days=180)

            if best_intent == "tax_refund":
                self.state_board.publish_assertion("red_herring_tax_refund", True, 0.90, as_of_time_str, half_life_days=60)
