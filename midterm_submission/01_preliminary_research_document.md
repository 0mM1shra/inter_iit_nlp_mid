# Preliminary Research Document & Reading Log
**Project**: Agentic Customer 360 — Proactive Intervention Desk  
**Event**: Inter IIT Tech Meet 15.0 Prepathon (NLP Track)  
**Submission Date**: September 15, 2026 (Mid-Term Deliverable)  

---

## 📌 Research Overview & Philosophy
As emphasized in the Problem Statement and organizer guidelines, this problem is **heavily research-oriented (weighed at 30% of final evaluation)**. Building an enterprise-grade, ambient agentic Customer 360 desk requires moving beyond static prompt-based chat frameworks. Traditional RAG wrappers fail under continuous multi-modal streaming due to context pollution, uncoordinated agent conflicts, out-of-order event corruption, and memory drift.

Below is our comprehensive reading log documenting research papers, engineering blogs, industry solutions, agent frameworks, and event stream analysis, along with the explicit architectural decisions each item informed in our system design.

---

## 1. Academic Research Papers

### 1.1 Memory & State Management Papers
1. **[MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)** (Packer et al., 2023)
   - *What was learned*: Introduces OS-style memory management for LLMs, dividing context into Main Context (working memory), Recall Memory (episodic event log), and Archival Memory (deep semantic storage), using explicit function calls for paging.
   - *System Decision Informed*: Inspired our **3-Tiered Memory Architecture** (Working Memory for active sessions, Episodic Memory per customer, Semantic Memory for policy rules) and automated memory paging to prevent context window overflow.

2. **[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)** (Park et al., 2023)
   - *What was learned*: Uses a memory stream scoring formula ($Score = \alpha \cdot \text{Recency} + \beta \cdot \text{Importance} + \gamma \cdot \text{Relevance}$) and periodic high-level reflection to form abstract state inferences.
   - *System Decision Informed*: Informed our **Continuous Life-Phase Reflection Engine** and decay-weighted episodic memory retrieval, preventing stale 2-year-old transactions from noise-polluting current hardship or churn risk evaluations.

3. **[Language Agent Tree Search (LATS)](https://arxiv.org/abs/2310.04406)** (Zhou et al., 2023)
   - *What was learned*: Combines LLM reasoning, action execution, and search tree planning with state evaluation and self-reflection.
   - *System Decision Informed*: Informed our Synthesis Agent's multi-hypothesis state evaluation, allowing the system to weigh alternative life event hypotheses (`new_child` vs `financial_distress`) before locking into a confidence band.

4. **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** (Yao et al., 2022)
   - *What was learned*: Interleaves reasoning traces ("Thought") with domain-specific execution ("Action") and observation ("Observation").
   - *System Decision Informed*: Used for domain specialist swarm agents (`UsageAgent`, `SupportAgent`, `TxnAgent`, `KYCAgent`) tool execution loops.

5. **[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)** (Shinn et al., 2023)
   - *What was learned*: Agents self-reflect on past execution failures and store verbal critiques to avoid repeating mistakes.
   - *System Decision Informed*: Populates episodic memory with intervention outcomes (e.g., "discount email sent on Jan 10 failed; phone call required").

---

### 1.2 Multi-Agent Coordination & Topology Papers
6. **[MetaGPT: Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352)** (Hong et al., 2023)
   - *What was learned*: Incorporates Standard Operating Procedures (SOPs) into multi-agent workflows with structured output schemas and role specialization.
   - *System Decision Informed*: Enforces strict agent role separation and structured Pydantic/JSON schema handoffs between agents rather than passing raw un-scoped prompt dumps.

7. **[Encouraging Divergent Thinking in LLMs via Multi-Agent Debate](https://arxiv.org/abs/2305.14325)** (Du et al., 2023)
   - *What was learned*: Multiple agent personas debating a shared problem uncover hidden contradictions and outperform single-agent consensus.
   - *System Decision Informed*: Establishes our **Multi-Agent Debate Protocol**, activated when Swarm agents yield conflicting signals (e.g., `TxnAgent` flags large deposit as growth while `SupportAgent` flags fee dispute as churn risk).

8. **[DyLAN: Dynamic Communication Structure in Multi-Agent Team](https://arxiv.org/abs/2310.02170)** (Liu et al., 2023)
   - *What was learned*: Dynamic selection of agent interaction topologies based on task complexity and agent contribution scores.
   - *System Decision Informed*: Guides our hybrid topology (Parallel Swarm for signal gathering $\rightarrow$ Sequential Handoff for synthesis $\rightarrow$ Debate on conflict $\rightarrow$ Round-Robin drafting).

9. **[ChatDev: Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924)** (Qian et al., 2023)
   - *What was learned*: Sequential pass-offs combined with dedicated reviewer/critic agents improve final artifact quality and compliance.
   - *System Decision Informed*: Informed our **Critique-Refiner Agent** which audits drafted proposals for tone, compliance rules, and budget limits before HITL checkpointing.

10. **[Self-RAG: Learning to Retrieve, Generate, and Critique](https://arxiv.org/abs/2310.11511)** (Asai et al., 2023)
    - *What was learned*: Adaptive retrieval on-demand using reflection tokens rather than constant vector DB searching on every token.
    - *System Decision Informed*: RAG retrieval against eligibility rules and policy documents is executed only when derived state board thresholds are crossed.

---

## 2. Engineering Blogs & Industry Architecture Case Studies

1. **[Stripe Engineering Blog — Real-time Financial Event Processing & Fraud Detection](https://stripe.com/blog)**
   - *Takeaway*: Real-time financial stream analysis requires immutable event logs, windowed aggregation, and separation of transaction authorization from post-transaction risk scoring.
   - *System Decision*: Implemented windowed spending anomaly scoring separate from real-time hard-stop guardrails.

2. **[Uber Engineering — Real-Time Event Processing at Scale with Apache Flink](https://www.uber.com/blog/engineering/)**
   - *Takeaway*: Key insights on event-time processing vs ingestion-time processing and watermarking for late-arriving events.
   - *System Decision*: Events in `live_stream.jsonl` are strictly sorted and ingested via `event_time` watermarking, preventing out-of-order network delays from corrupting rolling averages.

3. **[Netflix TechBlog — Real-Time Stateful Stream Processing](https://netflixtechblog.com/)**
   - *Takeaway*: Maintaining stateful customer boards across distributed workers using partitioned key-value stores.
   - *System Decision*: Informed our **Shared Per-Customer State Board**, ensuring all swarm agents read/write to a customer-scoped state object.

4. **[Databricks Blog — Real-Time Customer 360 Lakehouse Architecture](https://www.databricks.com/blog)**
   - *Takeaway*: Unifying multi-modal data streams (web telemetry + support tickets + transactions) into a single analytical feature store.
   - *System Decision*: Unified multi-source payload normalization (`card_payments`, `core_banking_ledger`, `web_app_events`, `support_logs`) into a common event envelope.

5. **[DoorDash Engineering — Real-Time Feature Engineering & Event Streaming](https://doordash.engineering/)**
   - *Takeaway*: Sliding time-window aggregations (e.g., rolling 30-day login frequency decay) calculated on live streams.
   - *System Decision*: Feature extraction algorithms for login frequency trends ($login\_freq\_trend = -40\%$) computed dynamically as app telemetry events arrive.

---

## 3. Existing Industry Solutions & Agent Frameworks Analyzed

1. **[LangChain & LangGraph (Stateful Multi-Agent Workflows)](https://python.langchain.com/docs/concepts/architecture/)**
   - *Analysis*: Evaluated for cyclic agent graphs and persistence.
   - *Key Takeaway*: Used to model our stateful graph execution (Swarm $\rightarrow$ State Board $\rightarrow$ Synthesis $\rightarrow$ Debate $\rightarrow$ Refiner $\rightarrow$ HITL).

2. **[Microsoft AutoGen (Conversational Multi-Agent Framework)](https://microsoft.github.io/autogen/)**
   - *Analysis*: Analyzed conversational multi-agent communication patterns.
   - *Key Takeaway*: Highlighted the risk of infinite agent conversational loops; confirmed the need for structured state boards over open-ended chatting.

3. **[CrewAI (Role-Based Agent Orchestration)](https://www.crewai.com/)**
   - *Analysis*: Looked at task delegation and role-based agent execution.
   - *Key Takeaway*: Reinforced strict tool boundaries per agent role.

4. **[NVIDIA NeMo Guardrails & Guardrails AI](https://github.com/NVIDIA/NeMo-Guardrails)**
   - *Analysis*: Evaluated programmable rails for LLM apps.
   - *Key Takeaway*: Implemented deterministic regex/keyword hard-stops (`"lawsuit"`, `"attorney"`, `"legal action"`) that bypass LLM logic entirely.

---

## 4. Event Stream Reading & Data Package Analysis

As highlighted by the problem statement and organizers, **reading the event stream is an essential input source**. 

### 4.1 Event Stream Datasets & Links Consulted
- **Official Problem Statement Event Stream Package**: [Mega Download Link](https://mega.nz/file/9rh1iLwS#ek99IhEEXnOq2NW-PDukwpUxZnyAhTpGEFLC6-DSLkA)
- **Local Practice Scenarios Inspected**: `customer_360_dataset/scenario_01`, `scenario_02`, `scenario_03`

### 4.2 Stream Envelope & Source Systems Analyzed
Every stream entry follows the common JSON envelope schema:
```json
{
  "event_id": "EVT_000173",
  "event_time": "2026-03-14T09:12:03Z",
  "ingestion_time": "2026-03-14T09:12:07Z",
  "customer_id": "CUST_00042",
  "account_id": "ACC_CHK_001",
  "source_system": "card_payments",
  "event_type": "card_transaction",
  "payload": {}
}
```

Multi-source event payloads parsed and mapped to domain agents:
1. `card_payments` (`purchase`, `decline`) $\rightarrow$ `TxnAgent` (MCC category spending, merchant analysis).
2. `instant_payments` / `ach_wire` (`inbound_transfer`, `outbound_transfer`) $\rightarrow$ `TxnAgent` (Large transfer detection, counterparty analysis).
3. `core_banking_ledger` (`deposit`, `withdrawal`, `standing_instruction`) $\rightarrow$ `TxnAgent` (Standing instruction cancellation tracking, salary deposits).
4. `loan_kyc` (`dependents_change`, `marital_status_change`, `address_change`) $\rightarrow$ `KYCAgent` (Demographic state changes).
5. `web_app_events` (`login`, `search_query`, `feature_used`) $\rightarrow$ `UsageAgent` (Login frequency decay, search query intent).
6. `support_logs` (`ticket_created`, `call_transcript`) $\rightarrow$ `SupportAgent` (Sentiment scoring, fee complaint detection).

### 4.3 Handling Event-Time vs. Ingestion-Time & Red Herrings
- **Out-of-Order Handling**: Stream replayer queues events into an event-time watermark window (`event_time` vs `ingestion_time`) to handle delayed transmissions without corrupting 30-day rolling rollups.
- **Red Herring Isolation**: Verified across dataset ground truth files (`EVT_000382` tuition wire, `EVT_000402` resort refund, `EVT_000328` baby monitor purchase, `EVT_000447` tax refund deposit). Red herrings are isolated by requiring **cross-domain signal correlation** on the Shared State Board before upgrading confidence from `low` to `high`.

---

## 5. Summary Mapping: Research to System Decisions

| Research Reference / Resource | Category | Specific System Architectural Decision |
|---|---|---|
| **[MemGPT](https://arxiv.org/abs/2310.08560)** | Paper | 3-Tiered Memory Hierarchy & Context Paging |
| **[Generative Agents](https://arxiv.org/abs/2304.03442)** | Paper | Decay-Weighted Episodic RAG & Life-Phase Reflection |
| **[MetaGPT](https://arxiv.org/abs/2308.00352)** | Paper | Structured Pydantic Schema Handoffs & Role SOPs |
| **[Agent Debate](https://arxiv.org/abs/2305.14325)** | Paper | Multi-Agent Debate for Contradiction Resolution |
| **[ChatDev](https://arxiv.org/abs/2307.07924)** | Paper | Critique-Refiner Agent & Round-Robin Drafting |
| **[Self-RAG](https://arxiv.org/abs/2310.11511)** | Paper | On-Demand Adaptive Policy RAG Retrieval |
| **[Uber Flink Stream Processing](https://www.uber.com/blog/engineering/)** | Blog | Event-Time Watermarking for Late/Out-of-Order Events |
| **[Netflix Stateful Streams](https://netflixtechblog.com/)** | Blog | Shared Per-Customer State Board Architecture |
| **[NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)** | Framework | Deterministic Keyword Bypasses & Data-Layer PII Masking |
| **[PS Event Stream Package](https://mega.nz/file/9rh1iLwS#ek99IhEEXnOq2NW-PDukwpUxZnyAhTpGEFLC6-DSLkA)** | Event Stream | Multi-Source Payload Normalization & Schema Contracts |
