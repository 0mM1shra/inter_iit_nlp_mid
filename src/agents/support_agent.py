"""
Support / Sentiment Agent for ACT-TREE 360
Uses real NLP (VADER Sentiment Analysis & TF-IDF Semantic Intent Classification)
to process support transcripts, call logs, and customer tickets dynamically.
"""

from src.nlp_engine import NLPEngine


class SupportAgent:
    def __init__(self, state_board, nlp_engine: NLPEngine = None):
        self.state_board = state_board
        self.nlp_engine = nlp_engine or NLPEngine()

        self.candidate_intents = {
            "medical_hardship": [
                "hospital emergency medical bill er visit injury illness treatment surgery clinical hardship financial distress payment plan credit card"
            ],
            "fee_dispute": [
                "fee dispute charge refund denied complaint unauthorized penalty overdraft waiver service fee dispute"
            ],
            "churn_complaint": [
                "closing account switching bank terrible service moving funds transfer out unhelpful dissatisfied competitor"
            ]
        }

    def process_features(self, features, as_of_time_str):
        support_logs = features.get("support_logs", [])
        if not support_logs:
            return

        total_compound_sentiment = 0.0
        log_count = 0

        for log in support_logs:
            payload = log.get("payload", {})
            raw_text = payload.get("raw_text") or payload.get("summary") or ""
            if not raw_text.strip():
                continue

            status = (payload.get("resolution_status") or "").lower()

            # 1. Genuine NLP Sentiment Analysis
            sentiment_dict = self.nlp_engine.analyze_sentiment(raw_text)
            compound = sentiment_dict.get("compound", 0.0)
            total_compound_sentiment += compound
            log_count += 1

            # 2. Genuine NLP TF-IDF Semantic Intent Classification
            best_intent, confidence = self.nlp_engine.classify_intent_tfidf(raw_text, self.candidate_intents)
            entities = self.nlp_engine.extract_semantic_entities(raw_text)

            # Publish NLP-derived assertions
            if best_intent == "medical_hardship" and confidence >= 0.08:
                self.state_board.publish_assertion(
                    "medical_support_ticket", True, min(0.98, 0.70 + confidence), as_of_time_str, half_life_days=45
                )

            if best_intent == "fee_dispute" or entities.get("dispute_flag"):
                self.state_board.publish_assertion(
                    "fee_dispute_flag", True, min(0.95, 0.65 + confidence), as_of_time_str, half_life_days=30
                )
                if "resolved" not in status:
                    self.state_board.publish_assertion(
                        "unresolved_complaint_flag", True, 0.95, as_of_time_str, half_life_days=30
                    )

            if best_intent == "churn_complaint":
                self.state_board.publish_assertion(
                    "expressed_churn_intent", True, min(0.95, 0.70 + confidence), as_of_time_str, half_life_days=30
                )

        if log_count > 0:
            avg_sentiment = total_compound_sentiment / log_count
            self.state_board.publish_assertion(
                "support_sentiment_score", round(avg_sentiment, 2), 0.85, as_of_time_str, half_life_days=14
            )
