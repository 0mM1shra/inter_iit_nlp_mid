"""
Tier 3: Semantic Memory (pgvector / Live Policy Vector Store)
Maintains a live vector index over product eligibility rules, hardship policies, retention terms, and legal compliance docs.
"""

from typing import List, Dict, Any
from src.nlp_engine import NLPEngine


class SemanticMemory:
    def __init__(self, nlp_engine: NLPEngine = None):
        self.nlp_engine = nlp_engine or NLPEngine()
        self.policies = [
            {
                "policy_id": "POL_001_MEDICAL_HARDSHIP",
                "title": "Medical Hardship Assistance & Fee Waiver Policy",
                "content": "For customers experiencing documented medical emergencies, hospital bills, or income disruption due to disability, the bank authorizes fee waivers, payment deferrals, and custom payment plans up to 12 months.",
                "category": "support_intervention"
            },
            {
                "policy_id": "POL_002_CHILDCARE_SAVINGS",
                "title": "New Parent Childcare Savings & 529 Insurance Policy",
                "content": "For customers adding dependents or enrolling in daycare standing instructions, offer personalized 529 college savings plans, child health insurance options, and high-yield nursery savings accounts.",
                "category": "personalized_offer"
            },
            {
                "policy_id": "POL_003_RETENTION_OUTREACH",
                "title": "High-Value Customer Retention & Fee Waiver Policy",
                "content": "When tenured customers cancel standing instructions or express fee dissatisfaction, initiate proactive retention outreach with annual fee waivers and priority phone routing.",
                "category": "proactive_retention_outreach"
            },
            {
                "policy_id": "POL_004_COMPLIANCE_LEGAL",
                "title": "Legal Threat & AML Mandatory Escalation Policy",
                "content": "Any explicit mention of lawsuit, attorney, legal counsel, bankruptcy, or fraud spike must immediately halt autonomous marketing or outreach and route to Legal Compliance.",
                "category": "compliance_fraud_hold"
            }
        ]

    def query_live_policies(self, query_text: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """
        Queries live policy vector index using TF-IDF / embedding similarity.
        """
        candidate_intents = {p["policy_id"]: [p["content"]] for p in self.policies}
        best_policy_id, conf = self.nlp_engine.classify_intent_tfidf(query_text, candidate_intents)

        matched = [p for p in self.policies if p["policy_id"] == best_policy_id]
        if matched:
            return matched
        return self.policies[:top_k]
