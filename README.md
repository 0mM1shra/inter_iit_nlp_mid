# Agentic Customer 360 — Proactive Intervention Desk
### Inter IIT Tech Meet 15.0 Prepathon (Natural Language Processing Track)
**Author**: Om Mishra | Electronics Engineering (3rd Year), IIT (BHU) Varanasi | Roll No.: 24095073  
**Mid-Term Submission** | Deadline: September 15, 2026 (EoD)  
**GitHub Repository**: https://github.com/0mM1shra/inter_iit_nlp_mid  
**Submission Form**: [Google Form Submission](https://forms.gle/1MKiqta6dVjoY7D76)  

---

## 📌 Executive Summary
This repository contains the **Mid-Term Submission** for the *Agentic Customer 360 — Proactive Intervention Desk* problem statement. 

Traditional Customer 360 architectures rely on static CRM dashboards requiring manual observation. This project implements an **Ambient, Event-Driven Multi-Agent System (MAS)** that continuously parses multi-modal customer data streams (card transactions, banking ledgers, web/app telemetry, support logs, KYC updates), infers evolving customer states/life events (medical hardship, new child, churn risk, etc.), and executes costed interventions with strict explainability, traceability, and Human-in-the-Loop (HITL) checkpoints.

---

## 📂 Repository Structure & Mid-Term Deliverables

All required mid-term deliverables are structured under `midterm_submission/`:

```
NLP/
├── midterm_submission/
│   ├── MIDTERM_SUBMISSION.md                   # Central Submission Index
│   ├── 01_preliminary_research_document.md     # Research Document & Reading Log (30% Weight)
│   ├── 02_preliminary_system_architecture.md   # Preliminary System Architecture Specification
│   └── 03_one_page_report.pdf                  # One-Page Domain & Approach Report
├── customer_360_dataset/
│   ├── README_dataset_schema.md                # Dataset Schema & Output Enum Guidelines
│   ├── scenario_01/                            # Scenario 01: Medical Hardship (Marcus Vance)
│   ├── scenario_02/                            # Scenario 02: New Child Life Event (Priya Sharma)
│   └── scenario_03/                            # Scenario 03: Churn Risk (David Chen)
├── evaluate_scenarios.py                       # Automated Evaluation & Scoring Harness
├── .gitignore
└── README.md                                   # Repository Landing Page
```

---

## 📑 Deliverable Documents Overview

| Deliverable | File Link | Key Highlights |
|---|---|---|
| **Deliverable 1: Preliminary Research Document** | [`midterm_submission/01_preliminary_research_document.md`](midterm_submission/01_preliminary_research_document.md) | Grounded in 10 arXiv papers (MemGPT, MetaGPT, DyLAN, Self-RAG, Guardrails AI, Calibrated HITL), 5 engineering blogs (Stripe, Uber Flink, Netflix, Databricks, DoorDash), 4 agent frameworks (LangGraph, AutoGen, CrewAI, NeMo Guardrails), and explicit Event Stream Analysis. |
| **Deliverable 2: System Architecture Spec** | [`midterm_submission/02_preliminary_system_architecture.md`](midterm_submission/02_preliminary_system_architecture.md) | Visual Mermaid Flowchart, Event-Time Streaming Ingestion, Shared Per-Customer State Board, 3-Tiered Memory Architecture, Swarm + Debate + Refiner Topologies, and Non-Negotiable Safety Rails. |
| **Deliverable 3: One-Page Report (PDF)** | [`midterm_submission/03_one_page_report.pdf`](midterm_submission/03_one_page_report.pdf) | Executive 1-page PDF report detailing domain insights, dataset/event stream learnings, architectural progress achieved till now, and future execution plans. |
| **Submission Index** | [`midterm_submission/MIDTERM_SUBMISSION.md`](midterm_submission/MIDTERM_SUBMISSION.md) | Central submission summary file. |

---

## 🧪 Evaluation & Scoring Harness

We have included an automated evaluation script to test predicted checkpoints against scenario ground truths:

```bash
python evaluate_scenarios.py customer_360_dataset/scenario_01/ground_truth.json <path_to_predictions.json>
```

Calculates scores for:
- State Inference Accuracy & Precision
- Action Matching & Subtype Precision
- HITL Status Calibration
- Red Herring / False Positive Avoidance
