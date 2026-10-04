#!/usr/bin/env python3
"""
ACT-TREE 360 End-to-End Pipeline Entrypoint & Terminal Visualizer
Author: Om Mishra (Electronics Engineering 3rd Year, IIT BHU)

Satisfies Section 7.2 Frontend Expectations:
Provides a real-time, terminal-based dashboard displaying data stream arrival,
swarm agent execution, shared state board updates, actor-critic debate, guardrail scans,
and final citation-backed HITL decisions via LangGraph orchestration.
"""

import os
import sys
import json
import time
from src.stream_processor import StreamProcessor
from src.state_board import SharedStateBoard
from src.memory_engine import MemoryEngine
from src.guardrails import GuardrailEngine
from app.orchestration.graph import create_act_tree_graph

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

    # Initialize Core Engines & LangGraph Orchestrator
    state_board = SharedStateBoard(customer_id)
    memory_engine = MemoryEngine(customer_id)
    guardrail_engine = GuardrailEngine()
    langgraph_app = create_act_tree_graph()

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

        # 2. Execute LangGraph Stateful Multi-Agent DAG
        graph_input = {
            "customer_id": customer_id,
            "as_of_time": ts,
            "features": features,
            "state_board": state_board,
            "memory_engine": memory_engine,
            "guardrail_engine": guardrail_engine,
            "synthesis_result": {},
            "debate_result": {},
            "action_proposal": {},
            "final_action": {},
            "hitl_status": "auto_approved",
            "explanation": {}
        }

        graph_output = langgraph_app.invoke(graph_input)

        # 3. Extract LangGraph Workflow Results
        reconciled_synth = graph_output["debate_result"]
        final_action = graph_output["final_action"]
        hitl_status = graph_output["hitl_status"]
        explanation = graph_output["explanation"]

        snap = state_board.snapshot(ts)
        if verbose:
            print(f"🐝 {BOLD}Swarm Assertions Published to State Board:{RESET}")
            for k, v in snap.items():
                print(f"   • {k.ljust(32)}: val={str(v['value']).ljust(10)} | conf={v['effective_confidence']}")

            print(f"⚔️ {BOLD}Actor-Critic Debate Audit:{RESET} State -> {BOLD}{reconciled_synth['inferred_state']}{RESET} | Conf -> {BOLD}{reconciled_synth['confidence_band']}{RESET}")
            print(f"🎯 {BOLD}Final Decision:{RESET} Action -> {GREEN}{BOLD}{final_action['action']}{RESET} ({final_action.get('action_subtype')})")
            print(f"🚦 {BOLD}HITL Checkpoint:{RESET} {RED if hitl_status == 'escalated' else GREEN}{hitl_status.upper()}{RESET}")
            print(f"💡 {BOLD}Citation Explanation:{RESET} {explanation.get('summary', final_action.get('notes'))}\n")

        # Format strictly per evaluation harness schema
        checkpoint_entry = {
            "as_of_time": ts,
            "inferred_state": reconciled_synth["inferred_state"],
            "confidence_band": reconciled_synth["confidence_band"],
            "action": final_action["action"],
            "action_subtype": final_action["action_subtype"],
            "hitl_status": hitl_status
        }
        output_checkpoints.append(checkpoint_entry)

    # Write output to scenario directory
    out_path = os.path.join(scenario_dir, output_filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output_checkpoints, f, indent=2)

    if verbose:
        print(f"✅ {GREEN}{BOLD}Inferred events file written to: {out_path}{RESET}")

    return out_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sc_dir = sys.argv[1]
        out_f = run_scenario_pipeline(sc_dir, verbose=True)

        gt_f = os.path.join(sc_dir, "ground_truth.json")
        if os.path.exists(gt_f):
            from evaluate_scenarios import evaluate_scenario
            evaluate_scenario(gt_f, out_f)
    else:
        # Run across all scenarios
        dataset_dir = "customer_360_dataset"
        scenarios = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d)) and d.startswith("scenario_")]
        for sc in sorted(scenarios):
            sc_path = os.path.join(dataset_dir, sc)
            out_f = run_scenario_pipeline(sc_path, verbose=True)

            gt_f = os.path.join(sc_path, "ground_truth.json")
            if os.path.exists(gt_f):
                from evaluate_scenarios import evaluate_scenario
                evaluate_scenario(gt_f, out_f)
