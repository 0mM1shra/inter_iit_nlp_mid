# Inter IIT Tech Meet 15.0 Prepathon — Mid-Term Submission
**Problem Statement**: Agentic Customer 360 — Proactive Intervention Desk  
**Track**: Natural Language Processing (NLP)  
**Submission Deadline**: September 15, 2026 (EoD)  
**Submission Form Link**: [Google Form Submission Link](https://forms.gle/1MKiqta6dVjoY7D76)  

---

## Mid-Term Submission Deliverables Overview

This directory contains the complete set of required deliverables for the **Mid-Term Submission** as requested by the organizers:

| Deliverable # | Document Name | Description & Key Focus | Link to File |
|---|---|---|---|
| **01** | **Preliminary Research Document & Reading Log** | Hyperlinked reading log of academic research papers (MemGPT, MetaGPT, DyLAN, Self-RAG, Guardrails AI, Calibrated HITL), engineering blogs (Stripe, Uber Flink, Netflix, Databricks, DoorDash), industry frameworks (LangGraph, AutoGen, CrewAI), and Event Stream Analysis. Weighs 30% of total score. | [01_preliminary_research_document.md](file:///c:/Users/DELL/Documents/Inter%20IIT/NLP/midterm_submission/01_preliminary_research_document.md) |
| **02** | **Preliminary System Architecture** | Detailed visual Mermaid flowchart & text specification covering Event-Time Streaming Ingestion, Shared Per-Customer State Board, Tiered Memory, Hybrid MAS Topology (Swarm + Debate + Refiner), Non-Negotiable Guardrails, and HITL Checkpoints. | [02_preliminary_system_architecture.md](file:///c:/Users/DELL/Documents/Inter%20IIT/NLP/midterm_submission/02_preliminary_system_architecture.md) |
| **03** | **One-Page Report** | Executive summary of domain findings (ambient vs prompt-based agents, early lead time vs overreaction), dataset & event stream learnings (`scenario_01`, `scenario_02`, `scenario_03`), red herring isolation, and execution roadmap. | [03_one_page_report.md](file:///c:/Users/DELL/Documents/Inter%20IIT/NLP/midterm_submission/03_one_page_report.md) |

---

## Key Highlights of the Architecture

1. **Event Stream Ingestion**: Event-time watermarking to handle out-of-order logs across multi-source streams (`card_payments`, `ach_wire`, `core_banking_ledger`, `web_app_events`, `support_logs`, `loan_kyc`). Analyzed using [Official Mega Package](https://mega.nz/file/9rh1iLwS#ek99IhEEXnOq2NW-PDukwpUxZnyAhTpGEFLC6-DSLkA).
2. **Shared Per-Customer State Board**: Eliminates memory leakage and context pollution by restricting swarm agents (`UsageAgent`, `SupportAgent`, `TxnAgent`, `KYCAgent`) to publishing structured observations.
3. **Multi-Agent Debate & Synthesis**: Explicit reconciliation layer when domain agents yield contradictory reads, surfacing ambiguity for calibrated Human-in-the-Loop (HITL) review.
4. **Deterministic Hard-Stop Guardrails**: Instant bypass for legal threats, self-harm, or AML spikes, with data-layer PII redaction.
5. **Evaluation Contract Compliance**: Outputs conform strictly to the required `inferred-events` JSON schema (`inferred_state`, `confidence_band`, `action`, `hitl_status`).
