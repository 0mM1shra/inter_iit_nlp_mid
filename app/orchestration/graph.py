"""
LangGraph Multi-Agent Workflow Orchestrator for ACT-TREE 360
Defines the stateful DAG orchestrating Swarm Ingestion, Correlation, Actor-Critic Debate, Action Selection, Critique, and HITL Routing.
"""

from typing import Dict, Any, TypedDict, List
from langgraph.graph import StateGraph, END

from src.state_board import SharedStateBoard
from src.memory_engine import MemoryEngine
from src.guardrails import GuardrailEngine
from src.hitl_engine import HITLEngine

from src.agents.usage_agent import UsageAgent
from src.agents.support_agent import SupportAgent
from src.agents.txn_agent import TransactionAgent
from src.agents.kyc_agent import KYCAgent
from src.agents.synthesis_agent import SynthesisAgent
from src.agents.debate_agent import ActorCriticDebate
from src.agents.action_agent import ActionAgent
from src.agents.refiner_agent import CritiqueRefinerAgent


class ACTTreeGraphState(TypedDict):
    customer_id: str
    as_of_time: str
    features: Dict[str, Any]
    state_board: Any
    memory_engine: Any
    guardrail_engine: Any
    synthesis_result: Dict[str, Any]
    debate_result: Dict[str, Any]
    action_proposal: Dict[str, Any]
    final_action: Dict[str, Any]
    hitl_status: str
    explanation: Dict[str, Any]


def swarm_ingestion_node(state: ACTTreeGraphState) -> Dict[str, Any]:
    state_board = state["state_board"]
    features = state["features"]
    ts = state["as_of_time"]

    usage_agent = UsageAgent(state_board)
    support_agent = SupportAgent(state_board)
    txn_agent = TransactionAgent(state_board)
    kyc_agent = KYCAgent(state_board)

    usage_agent.process_features(features, ts)
    support_agent.process_features(features, ts)
    txn_agent.process_features(features, ts)
    kyc_agent.process_features(features, ts)

    return {"state_board": state_board}


def synthesis_correlation_node(state: ACTTreeGraphState) -> Dict[str, Any]:
    synthesis_agent = SynthesisAgent(state["state_board"], state["memory_engine"])
    synth_res = synthesis_agent.synthesize_state(state["as_of_time"])
    return {"synthesis_result": synth_res}


def actor_critic_debate_node(state: ACTTreeGraphState) -> Dict[str, Any]:
    debate_agent = ActorCriticDebate(state["state_board"])
    debate_res = debate_agent.evaluate_conflict(state["synthesis_result"], state["as_of_time"])
    return {"debate_result": debate_res}


def action_selection_node(state: ACTTreeGraphState) -> Dict[str, Any]:
    action_agent = ActionAgent(state["memory_engine"])
    action_prop = action_agent.decide_action(state["debate_result"], state["as_of_time"], state_board=state["state_board"])
    return {"action_proposal": action_prop}


def critique_refiner_node(state: ACTTreeGraphState) -> Dict[str, Any]:
    refiner_agent = CritiqueRefinerAgent(state["guardrail_engine"])
    support_logs = state["features"].get("support_logs", [])
    raw_texts = [s.get("payload", {}).get("raw_text", "") for s in support_logs]
    final_act = refiner_agent.audit_proposal(state["action_proposal"], raw_texts)
    return {"final_action": final_act}


def hitl_routing_node(state: ACTTreeGraphState) -> Dict[str, Any]:
    reconciled = state["debate_result"]
    final_act = state["final_action"]

    hitl_status = HITLEngine.evaluate_routing(
        action=final_act["action"],
        confidence_band=reconciled["confidence_band"],
        action_subtype=final_act["action_subtype"]
    )

    explanation = HITLEngine.generate_explanation(
        inferred_state=reconciled["inferred_state"],
        action=final_act["action"],
        signal_events=reconciled.get("cited_evidence", []),
        episodic_history="Chronological spend & interaction log verified.",
        policy_rules="Policy Matrix 2026.1"
    )

    return {"hitl_status": hitl_status, "explanation": explanation}


def create_act_tree_graph():
    """
    Constructs and compiles the LangGraph StateGraph workflow executor.
    """
    workflow = StateGraph(ACTTreeGraphState)

    workflow.add_node("swarm_ingestion", swarm_ingestion_node)
    workflow.add_node("synthesis_correlation", synthesis_correlation_node)
    workflow.add_node("actor_critic_debate", actor_critic_debate_node)
    workflow.add_node("action_selection", action_selection_node)
    workflow.add_node("critique_refiner", critique_refiner_node)
    workflow.add_node("hitl_routing", hitl_routing_node)

    workflow.set_entry_point("swarm_ingestion")
    workflow.add_edge("swarm_ingestion", "synthesis_correlation")
    workflow.add_edge("synthesis_correlation", "actor_critic_debate")
    workflow.add_edge("actor_critic_debate", "action_selection")
    workflow.add_edge("action_selection", "critique_refiner")
    workflow.add_edge("critique_refiner", "hitl_routing")
    workflow.add_edge("hitl_routing", END)

    return workflow.compile()
