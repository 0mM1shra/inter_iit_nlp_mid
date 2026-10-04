"""
Usage / Engagement Agent for ACT-TREE 360
Uses real NLP (TF-IDF Semantic Intent Vector Classifier) to process web/app telemetry,
search queries, and login frequency trends dynamically.
"""

from src.nlp_engine import NLPEngine


class UsageAgent:
    def __init__(self, state_board, nlp_engine: NLPEngine = None):
        self.state_board = state_board
        self.nlp_engine = nlp_engine or NLPEngine()

        self.candidate_search_intents = {
            "hardship": ["hardship payment plan financial relief emergency assistance assistance deferral interest waiver"],
            "childcare": ["education savings 529 plan daycare baby infant nursery child trust fund family plan"],
            "homeloan": ["mortgage home loan refinancing property equity fixed rate APR property loan"]
        }

    def process_features(self, features, as_of_time_str):
        logins = features.get("login_count", 0)
        searches = features.get("searches", [])

        # 1. Real NLP Intent Classification over Search Queries
        combined_queries = " ".join(
            [s.get("payload", {}).get("search_text", "") for s in searches if s.get("payload", {}).get("search_text")]
        )

        if combined_queries.strip():
            best_intent, conf = self.nlp_engine.classify_intent_tfidf(combined_queries, self.candidate_search_intents)
            if best_intent == "hardship" and conf >= 0.15:
                self.state_board.publish_assertion("search_intent_hardship", True, min(0.98, 0.70 + conf), as_of_time_str, half_life_days=30)
            elif best_intent == "childcare" and conf >= 0.15:
                self.state_board.publish_assertion("search_intent_childcare", True, min(0.98, 0.70 + conf), as_of_time_str, half_life_days=30)
            elif best_intent == "homeloan" and conf >= 0.15:
                self.state_board.publish_assertion("search_intent_homeloan", True, min(0.98, 0.70 + conf), as_of_time_str, half_life_days=30)

        # 2. Telemetry trend calculation
        if logins == 0:
            self.state_board.publish_assertion("login_frequency_trend", -1.0, 0.90, as_of_time_str, half_life_days=14)
        elif logins < 3:
            self.state_board.publish_assertion("login_frequency_trend", -0.50, 0.75, as_of_time_str, half_life_days=14)
        else:
            self.state_board.publish_assertion("login_frequency_trend", 0.0, 0.50, as_of_time_str, half_life_days=14)
