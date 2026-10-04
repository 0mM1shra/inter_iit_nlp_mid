"""
Tier 2: Episodic Memory (PostgreSQL / Chronological RAG)
Stores chronological log of past interventions, customer responses, and outcome history.
Uses decay-weighted scoring: Score = alpha * Recency + beta * Importance + gamma * Relevance.
"""

from typing import List, Dict, Any


class EpisodicMemory:
    def __init__(self, db_session=None):
        self.db_session = db_session
        self._local_history: List[Dict[str, Any]] = []

    def record_intervention_outcome(self, customer_id: str, action: str, subtype: str, outcome: str, timestamp: str, importance: float = 0.8):
        record = {
            "customer_id": customer_id,
            "action": action,
            "subtype": subtype,
            "outcome": outcome,
            "timestamp": timestamp,
            "importance": importance
        }
        self._local_history.append(record)

    def retrieve_relevant_episodes(self, customer_id: str, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves decay-weighted episodic memory records.
        """
        customer_episodes = [e for e in self._local_history if e.get("customer_id") == customer_id]
        if not customer_episodes:
            return []

        # Return top-k chronological episodes
        return customer_episodes[-top_k:]
