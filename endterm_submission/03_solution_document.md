# End-Term Solution Document
**Project**: Agentic Customer 360 — Proactive Intervention Desk  
**Framework**: `ACT-TREE 360` (Actor-Critic Blackboard Swarm with Dynamic Life-Phase Hypothesis Trees)  
**Track**: Natural Language Processing (NLP) — Inter IIT Tech Meet 15.0 Prepathon  
**Author**: Om Mishra | Electronics Engineering (3rd Year), IIT (BHU) Varanasi | Roll No.: 24095073  

---

## 1. Problem Overview, Domain Insights & Core Paradigm

### 1.1 Enterprise Problem Context
"Customer 360" has long been the holy grail of enterprise banking architecture: aggregating a single, unified view of a customer's footprint across accounts, transactions, support tickets, and telemetry. Traditionally, large institutions attempted this by dumping data into massive lakes and building complex CRM dashboards. However, dashboards are passive. They rely on human account managers to continuously log in and spot subtle shifts—like a high-value customer quietly building up churn risk or entering financial hardship.

In real-world banking environments, customers generate an asynchronous, multi-modal stream of events: card swipes, wire transfers, app searches, support transcripts, and KYC updates. Human teams cannot continuously monitor millions of profiles to intervene before value loss occurs.

### 1.2 Ambient Agents vs. Prompt-Based Chatbots
Generative AI implementations frequently fall into the trap of building prompt-based chatbots that sit dormant until a human types a prompt. For Customer 360, enterprise deployment requires **Ambient Agents**: living background processes triggered asynchronously by environmental stream events or scheduled health rollups.

### 1.3 Core Innovation: The `ACT-TREE 360` Paradigm
To solve real-world stream noise and premature overreaction, we propose **`ACT-TREE 360`** (*Actor-Critic Blackboard Swarm with Dynamic Life-Phase Hypothesis Trees*):
1. **Dynamic Life-Phase Hypothesis Trees**: Maintains a probabilistic belief tree over candidate life phases ($P(\text{medical\_hardship})$, $P(\text{new\_child})$, $P(\text{churn\_risk})$), suppressing state jumps on red herrings until cross-domain signals validate the transition.
2. **Shared Per-Customer State Board**: Swarm agents write structured epistemic assertions with temporal decay half-lives ($\lambda$), eliminating memory leakage and context pollution across concurrent customer stores.
3. **Actor-Critic Multi-Agent Debate**: Resolves domain agent conflicts by pairing an *Actor Agent* (state/action proposer) with an adversarial *Critic Agent* (red-herring auditor).
4. **Deterministic Guardrails & Calibrated HITL**: Hardstop keyword bypasses, data-layer PII tokenization, and ambiguity/value-based routing with citation-backed "Ask Why" graphs.

---

## 2. System Architecture & Multi-Agent Topologies

### 2.1 Multi-Agent System (MAS) Coordination Topologies
Rather than defaulting to a uniform topology everywhere, `ACT-TREE 360` composes distinct coordination topologies mapped to specific pipeline stages:

- **Parallel Swarm Stage (Signal Ingestion)**: Independent domain agents (`UsageAgent`, `SupportAgent`, `TxnAgent`, `KYCAgent`) process incoming stream windows in parallel using real NLP (VADER sentiment analysis, TF-IDF semantic vector intent classification) and publish structured assertions to the customer's State Board.
- **Sequential Handoff Stage (Synthesis)**: The `SynthesisAgent` reads the State Board snapshot and evaluates likelihood updates across the Life-Phase Hypothesis Tree using a generalized Bayesian evidence accumulator.
- **Actor-Critic Debate Stage (Disagreement & Red Herring Audit)**: When swarm signals present ambiguity (e.g. tax refund deposit combined with standing instruction cancellation), the Actor and Critic agents debate counterfactual hypotheses to isolate red herrings.
- **Round-Robin & Refiner Stage (Drafting & Compliance)**: The `ActionAgent` drafts the bounded intervention, which is audited by the `CritiqueRefinerAgent` for tone, eligibility terms, budget limits, and guardrails.

### 2.2 Shared Per-Customer State Board & Memory Architecture
- **State Board**: Scoped strictly per `customer_id`. Agents publish key-value assertions with confidence scores and timestamped half-life decay ($\lambda_{usage} = 14\text{ days}$, $\lambda_{kyc} = 365\text{ days}$).
- **3-Tiered Memory Hierarchy**:
  - *Working Memory*: Active session state and open ticket text (Redis).
  - *Episodic Memory*: Chronological log of past interventions and customer outcomes (PostgreSQL).
  - *Semantic Memory*: Product eligibility matrices and policy guidelines (pgvector).

### 2.3 Event-Time Watermarking & Stream Normalization
Stream events are ingested and sorted strictly by `event_time` using an event-time watermark queue. This guarantees that late-arriving network packets (`ingestion_time` > `event_time`) do not corrupt 30-day windowed rolling rollups.

---

## 3. Benchmark Results, Non-Negotiables & Trade-Offs

### 3.1 Empirical Benchmark Evaluation Results
The system was evaluated using the automated scoring harness (`evaluate_scenarios.py`) across all official practice scenarios, achieving **High Benchmark Scores**:

| Practice Scenario | Scenario ID & Narrative | Checkpoints Passed | Red Herring Isolation | Score |
|---|---|---|---|---|
| **Scenario 01** | `scenario_05_major_medical_event` (Marcus Vance) | 3 / 3 | Tuition wire (`EVT_000382`) & Resort refund (`EVT_000402`) isolated | **90.0 / 110.0 (81.8%)** |
| **Scenario 02** | `scenario_06_new_child` (Priya Sharma) | 2 / 2 | Baby monitor electronics spend (`EVT_000328`) isolated | **60.0 / 70.0 (85.7%)** |
| **Scenario 03** | `scenario_07_churn_risk` (David Chen) | 3 / 3 | Tax refund deposit (`EVT_000447`) isolated | **100.0 / 100.0 (100.0%)** |

### 3.2 Non-Negotiables Verification (Safety, Traceability, Explainability)
1. **Explainability as a First-Class Output**: Every decision includes a citation-backed justification linking exact `cited_signal_events`, retrieved episodic history, and policy rules.
2. **Deterministic Hard-Stop Guardrails**: Keywords (`"lawsuit"`, `"attorney"`, `"legal action"`) trigger an instant pipeline halt and route to compliance (`compliance_fraud_hold`).
3. **Data-Layer PII Tokenization**: Customer account numbers, SSNs, and phone numbers are tokenized prior to LLM prompt generation.
4. **Calibrated HITL Routing**: Low-confidence or high-value decisions automatically route to human approvers (`escalated`) with an interactive "Ask Why" interface.

### 3.3 Known Limitations & Trade-Offs
- **Latency vs. Rigor**: Multi-agent debate adds ~1.2s latency per evaluation cycle. For real-time authorization (sub-second), fast-path guardrail engines bypass debate.
- **State Board Expiry**: Very long baseline shifts (>2 years) require explicit episodic summary compression to avoid state bloat.
