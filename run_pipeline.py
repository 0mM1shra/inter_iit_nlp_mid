#!/usr/bin/env python3
"""
ACT-TREE 360 End-to-End Pipeline Entrypoint & Terminal Visualizer
Author: Om Mishra (Electronics Engineering 3rd Year, IIT BHU)

Satisfies Section 7.2 Frontend Expectations:
Provides a real-time, terminal-based dashboard displaying data stream arrival,
swarm agent execution, shared state board updates, actor-critic debate, guardrail scans,
and final citation-backed HITL decisions.
"""

import os
import sys
import json
import time
from src.stream_processor import StreamProcessor
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

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Terminal Formatting
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def log_box(title, color=CYAN):
    border = "=" * 72
    print(f"\n{color}{BOLD}{border}{RESET}")
    print(f"{color}{BOLD} {title.center(70)} {RESET}")
    print(f"{color}{BOLD}{border}{RESET}")

def run_scenario_pipeline(scenario_dir, output_filename="inferred_events.json", verbose=True):
    log_box(f"ACT-TREE 360 STREAM PROCESSOR: {os.path.basename(scenario_dir)}", CYAN)

    stream_proc = StreamProcessor(scenario_dir)
    customer = stream_proc.entities.get("customer", {})
    customer_id = customer.get("customer_id", "CUST_UNKNOWN")
    customer_name = f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip() or "Customer"
    
    if verbose:
        print(f"👤 {BOLD}Customer Profile:{RESET} {customer_name} ({customer_id}) | Segment: {customer.get('segment', 'Standard')}")
        print(f"📦 {BOLD}Loaded Stream Events:{RESET} {len(stream_proc.history)} Seed Events | {len(stream_proc.live_stream)} Live Stream Events\n")

    # Initialize Core Engines
    state_board = SharedStateBoard(customer_id)
    memory_engine = MemoryEngine(customer_id)
    guardrail_engine = GuardrailEngine()

    # Initialize Swarm & Synthesis Agents
    usage_agent = UsageAgent(state_board)
    support_agent = SupportAgent(state_board)
    txn_agent = TransactionAgent(state_board)
    kyc_agent = KYCAgent(state_board)
    
    synthesis_agent = SynthesisAgent(state_board, memory_engine)
    debate_agent = ActorCriticDebate(state_board)
    action_agent = ActionAgent(memory_engine)
    refiner_agent = CritiqueRefinerAgent(guardrail_engine)

    # Determine Checkpoints to Evaluate
    gt_path = os.path.join(scenario_dir, "ground_truth.json")
    checkpoint_timestamps = []
    if os.path.exists(gt_path):
        with open(gt_path, 'r', encoding='utf-8') as f:
            gt_data = json.load(f)
            checkpoint_timestamps = [cp["as_of_time"] for cp in gt_data.get("checkpoints", [])]
    else:
        checkpoint_timestamps = ["2026-02-15T00:00:00Z", "2026-03-15T00:00:00Z", "2026-03-27T00:00:00Z"]

    output_checkpoints = []

    for idx, ts in enumerate(checkpoint_timestamps, 1):
        if verbose:
            print(f"{YELLOW}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
            print(f"{YELLOW}{BOLD} 🕒 CHECKPOINT #{idx} [AS-OF TIME: {ts}]{RESET}")
            print(f"{YELLOW}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

        # 1. Feature Aggregation up to checkpoint time
        features = stream_proc.compute_sliding_window_features(ts, window_days=45)

        if verbose:
            print(f"📥 {BOLD}Stream Influx (45-Day Window):{RESET} {features['transaction_count']} Txns | {features['support_count']} Support Logs | {features['login_count']} Logins | {len(features['kyc_updates'])} KYC Updates")

        # 2. Swarm Agents execution (Parallel structured writes to State Board)
        usage_agent.process_features(features, ts)
        support_agent.process_features(features, ts)
        txn_agent.process_features(features, ts)
        kyc_agent.process_features(features, ts)

        snap = state_board.snapshot(ts)
        if verbose:
            print(f"🐝 {BOLD}Swarm Assertions Published to State Board:{RESET}")
            for k, v in snap.items():
                print(f"   • {k.ljust(32)}: val={str(v['value']).ljust(10)} | conf={v['effective_confidence']}")

        # 3. Synthesis & Hypothesis Tree Reasoning
        synth_res = synthesis_agent.synthesize_state(ts)

        # 4. Multi-Agent Debate & Red-Herring Audit
        reconciled_synth = debate_agent.evaluate_conflict(synth_res, ts)
        if verbose:
            print(f"⚔️ {BOLD}Actor-Critic Debate Audit:{RESET} State -> {BOLD}{reconciled_synth['inferred_state']}{RESET} | Conf -> {BOLD}{reconciled_synth['confidence_band']}{RESET}")

        # 5. Action & Offer Selection
        action_proposal = action_agent.decide_action(reconciled_synth, ts, state_board=state_board)

        # 6. Critique-Refiner & Guardrail Pass
        raw_support_texts = [s.get("payload", {}).get("raw_text", "") for s in features.get("support_logs", [])]
        final_action = refiner_agent.audit_proposal(action_proposal, raw_support_texts)

        # 7. HITL Routing Calibration & Explanation Generation
        hitl_status = HITLEngine.evaluate_routing(
            action=final_action["action"],
            confidence_band=reconciled_synth["confidence_band"],
            action_subtype=final_action["action_subtype"]
        )

        explanation = HITLEngine.generate_explanation(
            inferred_state=reconciled_synth["inferred_state"],
            action=final_action["action"],
            signal_events=[e.get("event_id") for e in features.get("transactions", [])[:3]],
            episodic_history="Chronological spend & interaction log verified.",
            policy_rules="Policy Matrix 2026.1"
        )

        if verbose:
            status_color = GREEN if hitl_status == "auto_approved" else RED
            print(f"🎯 {BOLD}Final Decision:{RESET} Action -> {BOLD}{final_action['action']}{RESET} ({final_action.get('action_subtype') or 'None'})")
            print(f"🚦 {BOLD}HITL Checkpoint:{RESET} {status_color}{BOLD}{hitl_status.upper()}{RESET}")
            print(f"💡 {BOLD}Citation Explanation:{RESET} {final_action['notes']}\n")

        output_cp = {
            "as_of_time": ts,
            "inferred_state": reconciled_synth["inferred_state"],
            "confidence_band": reconciled_synth["confidence_band"],
            "action": final_action["action"],
            "action_subtype": final_action["action_subtype"],
            "hitl_status": hitl_status,
            "notes": final_action["notes"]
        }
        output_checkpoints.append(output_cp)

    # Save inferred events output
    out_path = os.path.join(scenario_dir, output_filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output_checkpoints, f, indent=2)

    if verbose:
        print(f"✅ {GREEN}{BOLD}Inferred events file written to:{RESET} {out_path}")
    return out_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        out_file = run_scenario_pipeline(target_dir, verbose=True)
        
        gt_file = os.path.join(target_dir, "ground_truth.json")
        if os.path.exists(gt_file):
            from evaluate_scenarios import evaluate_scenario
            evaluate_scenario(gt_file, out_file)
    else:
        base_dir = "customer_360_dataset"
        scenarios = ["scenario_01", "scenario_02", "scenario_03"]
        from evaluate_scenarios import evaluate_scenario
        for sc in scenarios:
            sc_dir = os.path.join(base_dir, sc)
            if os.path.exists(sc_dir):
                out_f = run_scenario_pipeline(sc_dir, verbose=True)
                gt_f = os.path.join(sc_dir, "ground_truth.json")
                if os.path.exists(gt_f):
                    evaluate_scenario(gt_f, out_f)
