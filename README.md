# Agentic Customer 360 — Proactive Intervention Desk
### Inter IIT Tech Meet 15.0 Prepathon (Natural Language Processing Track)

**Author**: Om Mishra | Electronics Engineering (3rd Year), IIT (BHU) Varanasi | Roll No.: 24095073  
**GitHub Repository**: [https://github.com/0mM1shra/inter_iit_nlp_mid](https://github.com/0mM1shra/inter_iit_nlp_mid)  

---

## 🛠️ Architecture & System Overview: `ACT-TREE 360`

Enterprise banking architectures have historically attempted "Customer 360" by aggregating customer records into passive CRM dashboards. However, dashboards fail because they rely on human account managers to continuously monitor thousands of customer accounts to catch subtle shifts—such as a tenured client quietly building up churn risk or entering medical hardship.

This repository implements **`ACT-TREE 360`** (*Actor-Critic Blackboard Swarm with Dynamic Life-Phase Hypothesis Trees*), an **Ambient, Event-Driven Multi-Agent System (MAS)** designed to continuously parse multi-modal streaming event logs (`card_payments`, `ach_wire`, `core_banking_ledger`, `trading_brokerage`, `loan_kyc`, `web_app_events`, `support_logs`), infer evolving customer life states, and execute costed, safe interventions under strict safety and explainability boundaries.

### Core Architectural Pillars
1. **Dynamic Bayesian Life-Phase Hypothesis Trees**: Maintains a probabilistic belief tree over candidate customer states ($P(\text{medical\_hardship})$, $P(\text{new\_child})$, $P(\text{churn\_risk})$) across event timelines, suppressing state jumps on red herrings (e.g. tuition wires or tax refunds) until multi-domain cross-validation occurs.
2. **Per-Customer Epistemic Blackboard (`SharedStateBoard`)**: Swarm agents do not dump raw chain-of-thought text into context windows. Instead, they write customer-scoped key-value assertions with exponential decay half-lives ($\lambda_{usage}=14\text{d}$, $\lambda_{kyc}=365\text{d}$), eliminating context pollution and multi-tenant memory leakage.
3. **Actor-Critic Adversarial Debate Engine**: Resolves swarm agent disagreements by pairing an *Actor Agent* (state/action proposer) with an adversarial *Critic Agent* (red-herring auditor) to explicitly test and filter out noisy events.
4. **Deterministic Hard-Stop Guardrails & Data-Layer PII Tokenization**: Non-bypassable regex scanners for legal/AML threats (`"lawsuit"`, `"attorney"`) that halt autonomous logic instantly, paired with automated PII tokenization prior to prompt generation.
5. **Calibrated HITL Routing & "Ask Why" Graph Generation**: Automated routing (`auto_approved` vs `escalated`) based on confidence bands and action value thresholds, accompanied by citation-backed justification graphs linking exact signal events and policy nodes.

---

## 🖥️ Terminal Dashboard & Execution Visualization (PS Section 7.2 Frontend Expectations)

In accordance with Section 7.2 of the Problem Statement (*"No flashy frontend is expected or rewarded. What is expected is a bare-minimum, working way to actually see the system doing its job—the influx of data arriving, agents acting on it, and the system arriving at (and explaining) its final decisions"*), running `python run_pipeline.py` launches an interactive, real-time terminal visualizer dashboard:

```text
========================================================================
               ACT-TREE 360 STREAM PROCESSOR: scenario_01               
========================================================================
👤 Customer Profile: Marcus Vance (CUST_00042) | Segment: Standard
📦 Loaded Stream Events: 375 Seed Events | 116 Live Stream Events

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 🕒 CHECKPOINT #3 [AS-OF TIME: 2026-03-26T00:00:00Z]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📥 Stream Influx (45-Day Window): 43 Txns | 1 Support Logs | 31 Logins | 0 KYC Updates
🐝 Swarm Assertions Published to State Board:
   • login_frequency_trend           : val=0.0        | conf=0.5
   • support_sentiment_score         : val=-0.5       | conf=0.8
   • hospital_bill_posted            : val=True       | conf=0.95
   • red_herring_tuition_wire        : val=True       | conf=0.76
   • search_intent_hardship          : val=True       | conf=0.95
   • medical_support_ticket          : val=True       | conf=0.98
⚔️ Actor-Critic Debate Audit: State -> medical_hardship | Conf -> high
🎯 Final Decision: Action -> support_intervention (medical_hardship_payment_plan)
🚦 HITL Checkpoint: ESCALATED
💡 Citation Explanation: Medical hardship confirmed. Recommending medical hardship payment plan support intervention.

✅ Inferred events file written to: customer_360_dataset/scenario_01/inferred_events.json
==================================================
 FINAL SCORE: 110.0 / 110.0 (100.0%)
==================================================
```

### What Reviewers Observe During Execution:
1. **Data Stream Influx**: Live multi-source telemetry arriving in event-time order.
2. **Swarm Agent Activity**: `UsageAgent`, `SupportAgent`, `TransactionAgent`, and `KYCAgent` executing tools and publishing structured epistemic assertions to the customer's `SharedStateBoard`.
3. **Actor-Critic Debate Audit**: Contradictions and red-herring transfers (tuition wires, vacation refunds, tax deposits) explicitly audited.
4. **Final Decision & HITL Status**: Bounded intervention decision, confidence band, and HITL status (`AUTO_APPROVED` / `ESCALATED`).
5. **Citation-Backed Explanation**: Instant justification linking exact signal events and policy nodes.

---

## 🎯 Deliverables Satisfaction & PS Requirement Mapping

Every deliverable required in Sections 7 and 8 of the Problem Statement PDF is explicitly satisfied by dedicated components in this repository:

| PS Deliverable Section | PS Description & Weight | Repository Component & File Location | Implementation Proof & Compliance Details |
|---|---|---|---|
| **7.1 Research Log** | Documented running list of papers, blogs, frameworks, and event stream analysis (**30% Weight**) | [`endterm_submission/01_research_log.md`](endterm_submission/01_research_log.md) & [`midterm_submission/01_preliminary_research_document.md`](midterm_submission/01_preliminary_research_document.md) | **10 arXiv Papers** (MemGPT, MetaGPT, DyLAN, Self-RAG, Guardrails AI, Calibrated HITL, LATS, ReAct, Reflexion, Generative Agents), **5 Engineering Blogs** (Stripe, Uber Flink, Netflix, Databricks, DoorDash), **4 Agent Frameworks**, and explicit **Event Stream Analysis**. Features a Research-to-Decision Mapping Matrix. |
| **7.2 Codebase & Execution** | End-to-end working system, clean modular components, output visibility (**25% Weight**) | [`run_pipeline.py`](run_pipeline.py) & [`src/`](src/) | Full Python engine. Reviewers run `python run_pipeline.py` to watch live event streams ingest, agents write to `StateBoard`, hypothesis trees synthesize, debate execute, refiners audit, and `inferred_events.json` emit. |
| **7.3 Architecture Spec & Diagram** | System architecture diagram with data flows, agent tools, sync vs async flows (**10% Docs Weight**) | [`endterm_submission/02_system_architecture.md`](endterm_submission/02_system_architecture.md) | Complete visual Mermaid flowcharts color-coding Async Stream Ingestion, State Board, Swarm Agents, Sync Fast-Path Guardrails, Synthesis/Debate Layer, Action Pipeline, and Sync HITL Checkpoint. Includes comprehensive agent tool/data source tables. |
| **7.4 Solution Document** | Concise solution document explaining architecture, decisions, & trade-offs | [`endterm_submission/03_solution_document.md`](endterm_submission/03_solution_document.md) | Comprehensive Solution Document covering Problem Overview, Architecture & Topologies, and Benchmark Evaluation Results & Trade-Offs. |
| **7.5 Testing & Evaluation** | Testing results across scenario timelines, red herring isolation, & failure mode analysis | [`endterm_submission/04_testing_and_evaluation.md`](endterm_submission/04_testing_and_evaluation.md) | In-depth evaluation report detailing testing methodology, red-herring isolation mechanisms (tuition wire `EVT_000382`, resort refund `EVT_000402`, tax deposit `EVT_000447`), and lead-time calibration. |
| **8.1 Inferred-Events Schema** | Logging system outputs in required JSON schema (`inferred_state`, `confidence_band`, `action`, `hitl_status`) | `customer_360_dataset/*/inferred_events.json` generated by [`run_pipeline.py`](run_pipeline.py) | `run_pipeline.py` automatically writes `inferred_events.json` using strictly the allowed fixed enums specified in `README_dataset_schema.md`. |
| **8.1 Brownie Points Scoring Harness** | Custom scoring harness measuring predictions against ground truth answer keys (**Brownie Points**) | [`evaluate_scenarios.py`](evaluate_scenarios.py) | Standalone automated Python scoring script that parses `ground_truth.json`, scores checkpoints, enforces false-positive red-herring penalties, and reports percentage scores (**100% Benchmark Score**). |

---

## 🔍 Detailed Component-by-Component Codebase Guide

The `src/` directory and root scripts are modularized with strict single-responsibility boundaries:

```
src/
├── stream_processor.py       # Event-Time Watermarking & Sliding Window Feature Extraction
├── state_board.py            # Per-Customer Epistemic Blackboard with Half-Life Decay (λ)
├── memory_engine.py          # 3-Tiered Memory (Working, Episodic Decay RAG, Semantic Policy Base)
├── guardrails.py             # Hard-Stop Keyword Scanner & Data-Layer PII Tokenization
├── hitl_engine.py            # Calibrated HITL Routing & Citation-Backed "Ask Why" Generator
└── agents/
    ├── usage_agent.py        # App/Web Telemetry, Login Frequency Trends, Search Query Intent
    ├── support_agent.py      # Support Ticket NLP, Sentiment Scoring, Fee Dispute Classifier
    ├── txn_agent.py          # Ledger Anomaly Scorer, Standing Instruction Tracker, Red-Herring Filter
    ├── kyc_agent.py          # Demographic Updates, Dependents Changes (1->2), Relocation Processor
    ├── synthesis_agent.py    # Bayesian Life-Phase Hypothesis Tree Engine
    ├── debate_agent.py       # Actor-Critic Adversarial Debate & Counterfactual Audit Engine
    ├── action_agent.py       # Bounded Action Selection & Product Eligibility Matrix
    └── refiner_agent.py      # Critique-Refiner Compliance, Tone, & Budget Auditor
```

### Module Responsibilities:

1. **`src/stream_processor.py`**:
   - Ingests `entities.json`, `history_seed.jsonl`, and `live_stream.jsonl`.
   - Sorts events strictly by `event_time` using an event-time watermark queue to gracefully handle out-of-order data (`event_time` vs `ingestion_time`).
   - Computes sliding 30-day window aggregations (login frequency trends, spend baseline deviations).

2. **`src/state_board.py` (`SharedStateBoard`)**:
   - Manages a structured key-value blackboard scoped per `customer_id`.
   - Swarm agents publish structured assertions (`login_frequency_trend: -0.50`, `confidence: 0.75`).
   - Computes exponential decay half-lives ($\text{Effective Conf} = \text{Raw Conf} \cdot e^{-0.693 \cdot \Delta t / \lambda}$) so stale flags decay over time.

3. **`src/memory_engine.py` (`MemoryEngine`)**:
   - *Working Memory*: Active session state and ticket context.
   - *Episodic Memory*: Chronological history of past interventions and customer outcomes queried via decay-weighted RAG ($Score = \alpha \cdot \text{Recency} + \beta \cdot \text{Importance} + \gamma \cdot \text{Relevance}$).
   - *Semantic Memory*: Product eligibility matrices and compliance guidelines.

4. **`src/guardrails.py` (`GuardrailEngine`)**:
   - Fast-path deterministic regex scanner for legal threats (`"lawsuit"`, `"attorney"`, `"legal action"`, `"bankrupt"`) that immediately halts autonomous logic and routes to legal (`compliance_fraud_hold`).
   - Data-layer PII tokenization stripping SSNs and full account numbers before LLM prompt construction.

5. **`src/hitl_engine.py` (`HITLEngine`)**:
   - Evaluates routing status (`auto_approved` vs `escalated`).
   - Automatically escalates low-confidence decisions or high-value interventions (> $500 or loan pre-approvals).
   - Generates citation-backed "Ask Why" justification graphs linking `cited_signal_events`, retrieved episodic context, and policy rules.

6. **`src/agents/` (Swarm & Coordination Agents)**:
   - **`usage_agent.py`**: Analyzes telemetry logins and search intent (`hardship`, `education savings`, `mortgage`).
   - **`support_agent.py`**: Scans ticket sentiment (-0.82) and unresolved fee disputes.
   - **`txn_agent.py`**: Tracks standing instruction cancellations, income dips (disability vs salary), and detects red-herring transfers (tuition wire, tax refund).
   - **`kyc_agent.py`**: Monitors dependents changes (1 $\to$ 2) and address relocations.
   - **`synthesis_agent.py`**: Synthesizes State Board assertions into likelihood updates over the Life-Phase Hypothesis Tree.
   - **`debate_agent.py`**: Actor-Critic debate layer that audits counterfactual red-herring rules.
   - **`action_agent.py`**: Selects bounded actions (`no_action`, `proactive_retention_outreach`, `relationship_manager_escalation`, `personalized_offer`, `support_intervention`, `compliance_fraud_hold`).
   - **`refiner_agent.py`**: Audits drafted proposals against compliance, tone, and budget limits.

7. **`run_pipeline.py`**:
   - Entrypoint script that ties all components into an end-to-end executable pipeline. Writes `inferred_events.json` for any scenario directory.

8. **`evaluate_scenarios.py`**:
   - Standalone Brownie Points evaluation harness measuring predictions against ground truth answer keys.

---

## 📈 Benchmark Evaluation Scorecard

Our pipeline was benchmarked using `evaluate_scenarios.py` across all official practice scenarios, achieving **100% Perfect Accuracy**:

```
==================================================
 Running ACT-TREE 360 Pipeline on: customer_360_dataset\scenario_01
==================================================
Scenario ID: scenario_05_major_medical_event (Marcus Vance)
Checkpoint #1 [2026-02-15T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Checkpoint #2 [2026-03-12T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Checkpoint #3 [2026-03-26T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Red Herring EVT_000382 (Tuition Wire): [PASS]
Red Herring EVT_000402 (Resort Refund): [PASS]
FINAL SCORE: 110.0 / 110.0 (100.0%)

==================================================
 Running ACT-TREE 360 Pipeline on: customer_360_dataset\scenario_02
==================================================
Scenario ID: scenario_06_new_child (Priya Sharma)
Checkpoint #1 [2026-02-20T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Checkpoint #2 [2026-03-27T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Red Herring EVT_000328 (Baby Monitor Spend): [PASS]
FINAL SCORE: 70.0 / 70.0 (100.0%)

==================================================
 Running ACT-TREE 360 Pipeline on: customer_360_dataset\scenario_03
==================================================
Scenario ID: scenario_07_churn_risk (David Chen)
Checkpoint #1 [2026-02-15T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Checkpoint #2 [2026-03-08T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Checkpoint #3 [2026-04-10T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Red Herring EVT_000447 (Tax Refund Deposit): [PASS]
FINAL SCORE: 100.0 / 100.0 (100.0%)
```

---

## 📁 Repository Directory Breakdown

```
inter_iit_nlp_mid/
├── README.md                                   # Root Landing Page & Comprehensive Overview
├── docker-compose.yml                          # Production Compose (PostgreSQL+pgvector, Redis, Kafka, FastAPI)
├── requirements.txt                            # Pinned Dependencies (LangGraph, OpenAI, FastAPI, pgvector)
├── app/                                        # ENTERPRISE LANGGRAPH & FASTAPI APPLICATION
│   ├── main.py                                 # FastAPI Entrypoint & Interactive HITL Web Dashboard
│   ├── schemas/                                # Pydantic Event, Finding, CustomerState & Action Schemas
│   ├── database/                               # SQLAlchemy Database Models & Repositories
│   ├── memory/                                 # 3-Tier Memory (Redis Working, Postgres Episodic, pgvector Semantic)
│   ├── streaming/                              # Kafka Producer, Consumer & Event Topics
│   ├── agents/                                 # Swarm, Correlation, Offer, Retention & Critique Agents
│   ├── guardrails/                             # Deterministic Rules & Emergency Scanner
│   ├── hitl/                                   # HITL Routing & Interactive Web Interface Service
│   └── observability/                          # OpenTelemetry Tracing & Audit Logger
├── endterm_submission/                         # END-TERM SUBMISSION DELIVERABLES
│   ├── ENDTERM_SUBMISSION.md                 # Central End-Term Index & Execution Guide
│   ├── 01_research_log.md                    # Research Log & Theoretical Grounding (30% Weight)
│   ├── 02_system_architecture.md             # Architecture Spec & Visual Mermaid Flowcharts (20% Weight)
│   ├── 03_solution_document.md               # Solution Document (Problem Overview, Architecture & Evaluation)
│   ├── 04_testing_and_evaluation.md          # Benchmark Evaluation Report & Failure Mode Analysis
│   └── Endterm_final_report.pdf              # Compiled Comprehensive Master Report (PDF)
├── midterm_submission/                         # MID-TERM SUBMISSION ARCHIVE
├── src/                                      # CORE PYTHON ENGINE & NLP MODULES (25% Weight)
│   ├── nlp_engine.py                         # Genuine NLP Engine (VADER Sentiment & TF-IDF Vector Intent)
│   ├── stream_processor.py                   # Event-time watermarking & sliding window aggregations
│   ├── state_board.py                        # Shared Per-Customer State Board with decay
│   ├── memory_engine.py                      # 3-Tiered Memory Architecture (Working, Episodic, Semantic)
│   ├── guardrails.py                         # Hard-stop keyword guardrails & data-layer PII redaction
│   ├── hitl_engine.py                        # Calibrated HITL routing & citation graph generator
│   └── agents/                               # Specialist Agents (Usage, Support, Txn, KYC, Synthesis, Debate)
├── customer_360_dataset/                      # DATASET SCENARIOS & SCHEMAS
├── run_pipeline.py                           # Command-Line End-to-End Pipeline Entrypoint
├── evaluate_scenarios.py                     # Benchmark Evaluation Harness
└── .gitignore
```

---

## 💻 Quickstart Guide: Running the Codebase

### 1. Launch Production Services (Docker Compose)
Start PostgreSQL with pgvector, Redis, Kafka, and FastAPI web dashboard:

```bash
docker-compose up -d
```

Access the interactive HITL Web Dashboard at: `http://localhost:8000`

### 2. Process Live Streams & Generate `inferred_events.json`
Run the end-to-end pipeline across all practice scenarios using the virtual environment:

```bash
.\venv\Scripts\python run_pipeline.py
```

Run on a single scenario:

```bash
.\venv\Scripts\python run_pipeline.py customer_360_dataset/scenario_01
```

### 3. Run Automated Scoring Harness
Evaluate generated predictions against practice scenario ground truths:

```bash
.\venv\Scripts\python evaluate_scenarios.py customer_360_dataset/scenario_01/ground_truth.json customer_360_dataset/scenario_01/inferred_events.json
```

