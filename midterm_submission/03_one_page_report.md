# One-Page Domain & Approach Report
**Project**: Agentic Customer 360 — Proactive Intervention Desk  
**Event**: Inter IIT Tech Meet 15.0 Prepathon (NLP Track)  
**Author**: Om Mishra | Electronics Engineering (3rd Year), IIT (BHU) Varanasi | Roll No.: 24095073  
**Submission Date**: September 15, 2026 (Mid-Term Deliverable)  

---

## 1. Problem Domain Insights & Key Challenges

The traditional "Customer 360" paradigm relies on static CRM dashboards that require human account managers to manually discover customer risks or opportunities. Transitioning to **Agentic Customer 360** introduces fundamental architectural challenges:

1. **Ambient Execution vs. Prompt-Based Chatbots**: Traditional generative AI sits dormant until a human types a prompt. Ambient agents must live asynchronously in the background, triggered by continuous multi-modal event streams (card swipes, ledger entries, web searches, support tickets) or scheduled health checks.
2. **Early Lead Time vs. Premature Overreaction**: An optimal system must detect subtle behavioral shifts early (e.g., catching a tenured customer withdrawing savings before complete churn) without firing premature, low-confidence interventions on weak signals (e.g., offering a baby savings loan after just one grocery purchase).
3. **Red Herring Isolation**: Real-world financial streams contain noisy events (e.g., a tuition transfer mistaken for wealth drain, a resort refund mistaken for a windfall, a high-value electronics purchase mistaken for fraud). The system must correlate cross-domain signals over time to filter out red herrings.

---

## 2. Dataset & Event Stream Learnings

Analysis of the official event stream package ([Mega Event Stream Package](https://mega.nz/file/9rh1iLwS#ek99IhEEXnOq2NW-PDukwpUxZnyAhTpGEFLC6-DSLkA)) and the three practice scenarios (`scenario_01`, `scenario_02`, `scenario_03`) reveals critical stream processing and domain requirements:

- **Multi-Source Event Payload Normalization**: Ingests multi-modal payloads across `card_payments`, `instant_payments`/`ach_wire`, `core_banking_ledger`, `trading_brokerage`, `loan_kyc`, `web_app_events`, `support_logs`, and `social_signal_consented` into a unified `event_time` watermark queue.
- **Scenario 01 (Marcus Vance - Medical Hardship)**: ER visit + disability income reduction building over weeks before hospital bills and hardship ticket. *Key takeaway*: Weak early signals raise state board confidence without triggering high-stakes actions until explicit thresholds are met. Red herrings (tuition wire, resort refund) are isolated.
- **Scenario 02 (Priya Sharma - New Child Life Event)**: Maternity leave income dip + baby retail spend + search queries + daycare standing instruction + KYC dependents change $1 \to 2$. *Key takeaway*: Multi-signal correlation across KYC, ledger, and search telemetry transitions confidence from `low` to `high`.
- **Scenario 03 (David Chen - Churn Risk)**: Unresolved international fee dispute + dropping app logins + standing instruction cancellation + savings transfer. *Key takeaway*: Early lead-time is critical. Triggering retention outreach after standing instruction cancellation saves the account; waiting until zero card activity fails evaluation. Tax refund deposits are recognized as temporary red herrings.

---

## 3. Proposed Solution Approach & Architecture

Our approach combines state-of-the-art research in multi-agent systems and memory architectures to meet every production bar requirement:

1. **Shared Per-Customer State Board**: Swarm agents (`UsageAgent`, `SupportAgent`, `TxnAgent`, `KYCAgent`) run in parallel, writing structured conclusions to a shared blackboard scoped strictly per customer ID. This prevents context pollution and eliminates memory leakage between accounts.
2. **Multi-Agent Debate & Reconciler**: When swarm agents disagree (e.g., large tax deposit vs. zero app logins), a structured debate protocol surfaces the contradiction and adjudicates the true customer state.
3. **3-Tiered Memory Hierarchy**: Incorporates **Working Memory** (session context), **Episodic Memory** (decay-weighted historical events and past intervention outcomes), and **Semantic Memory** (product/policy RAG).
4. **Non-Negotiable Safety & Calibrated HITL**: Deterministic keyword guardrails bypass autonomous logic for legal/fraud threats. Low-confidence or high-value decisions are routed to human approvers with citation-backed explanations ("Ask Why").

---

## 4. Roadmap to Final Submission (Sept 19, 2026)

| Date | Key Milestone | Deliverable |
|---|---|---|
| **Sept 15 (EoD)** | **Mid-Term Submission** | Research Reading Log, Architecture Specification, 1-Page Report |
| **Sept 16** | **Streaming Pipeline & Swarm Engine** | Event-time stream replayer, state board, swarm agents |
| **Sept 17** | **Synthesis, Debate & HITL Layer** | Synthesis engine, debate protocol, refiner, HITL checkpoint |
| **Sept 18** | **Evaluation & Scoring Harness** | Automated evaluation script against practice scenario ground truths |
| **Sept 19 (EoD)** | **Final Submission** | GitHub Repo, Codebase, Architecture Diagram, 3-Page Solution Doc |
