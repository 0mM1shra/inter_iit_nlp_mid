#!/usr/bin/env python3
"""
Evaluation & Scoring Harness for Agentic Customer 360
Evaluates predicted system checkpoints against scenario ground_truth.json
"""

import json
import sys
import os
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def parse_iso(ts_str):
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))

def evaluate_scenario(ground_truth_path, predictions_path):
    print(f"==================================================")
    print(f" Evaluating: {ground_truth_path}")
    print(f" Against:    {predictions_path}")
    print(f"==================================================")

    if not os.path.exists(ground_truth_path):
        print(f"Error: Ground truth file not found at {ground_truth_path}")
        return False
    if not os.path.exists(predictions_path):
        print(f"Error: Predictions file not found at {predictions_path}")
        return False

    with open(ground_truth_path, 'r') as f:
        gt = json.load(f)
    with open(predictions_path, 'r') as f:
        preds = json.load(f)

    scenario_id = gt.get("scenario_id", "unknown_scenario")
    print(f"Scenario ID: {scenario_id}")
    print(f"Narrative Summary: {gt.get('true_narrative', '')[:120]}...\n")

    score_total = 0.0
    max_score = 0.0

    # 1. Evaluate Checkpoints
    gt_checkpoints = gt.get("checkpoints", [])
    print(f"--- Checking Checkpoints ({len(gt_checkpoints)} expected) ---")
    for idx, expected_cp in enumerate(gt_checkpoints, 1):
        target_time = expected_cp["as_of_time"]
        exp_state = expected_cp["expected_inferred_state"]
        exp_action = expected_cp["expected_action"]
        exp_hitl = expected_cp.get("expected_hitl_status")

        # Find matching prediction by timestamp or nearest preceding timestamp
        matching_pred = None
        if isinstance(preds, list):
            for p in preds:
                if isinstance(p, dict) and p.get("as_of_time") == target_time:
                    matching_pred = p
                    break
        
        max_score += 30.0 # 10 pts state, 10 pts action, 10 pts hitl/confidence
        if matching_pred:
            pred_state = matching_pred.get("inferred_state") or matching_pred.get("expected_inferred_state")
            pred_action = matching_pred.get("action") or matching_pred.get("expected_action")
            pred_hitl = matching_pred.get("hitl_status") or matching_pred.get("expected_hitl_status")

            state_match = (pred_state == exp_state)
            action_match = (pred_action == exp_action)
            hitl_match = (pred_hitl == exp_hitl) if exp_hitl else True

            cp_score = (10.0 if state_match else 0.0) + (10.0 if action_match else 0.0) + (10.0 if hitl_match else 0.0)
            score_total += cp_score

            status_symbol = "[PASS]" if (state_match and action_match) else "[FAIL]"
            print(f"Checkpoint #{idx} [{target_time}]: {status_symbol}")
            print(f"  Expected: State={exp_state}, Action={exp_action}, HITL={exp_hitl}")
            print(f"  Got:      State={pred_state}, Action={pred_action}, HITL={pred_hitl}")
            print(f"  Score:    {cp_score}/30.0\n")
        else:
            print(f"Checkpoint #{idx} [{target_time}]: [FAIL] MISSING PREDICTION IN OUTPUT (-30.0 pts)\n")

    # 2. Evaluate False Positive / Red Herring Checks
    fp_checks = gt.get("false_positive_checks", [])
    if fp_checks:
        print(f"--- Checking Red Herring / False Positive Penalties ({len(fp_checks)} checks) ---")
        for fp in fp_checks:
            event_id = fp.get("event_id")
            forbidden_actions = fp.get("must_not_trigger_action", [])
            max_score += 10.0
            
            # Check if any prediction triggered forbidden actions
            violation = False
            if isinstance(preds, list):
                for p in preds:
                    if isinstance(p, dict) and p.get("action") in forbidden_actions:
                        violation = True
                        break
            
            if not violation:
                score_total += 10.0
                print(f"Red Herring {event_id}: [PASS] (Avoided prohibited actions {forbidden_actions})")
            else:
                print(f"Red Herring {event_id}: [FAIL] (Triggered prohibited action!)")

    pct = (score_total / max_score * 100.0) if max_score > 0 else 0.0
    print(f"\n==================================================")
    print(f" FINAL SCORE: {score_total:.1f} / {max_score:.1f} ({pct:.1f}%)")
    print(f"==================================================")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python evaluate_scenarios.py <path_to_ground_truth.json> <path_to_predictions.json>")
        sys.exit(1)
    gt_file = sys.argv[1]
    pred_file = sys.argv[2]
    evaluate_scenario(gt_file, pred_file)
