# SRECon26 Presentation Proposal

## Title
**Agentic Chaos: What Works and What Doesn't**

---

## Abstract (150-200 words)

Traditional chaos engineering relies on human intuition to hypothesize failure modes, design experiments, and interpret results. This approach is fundamentally limited by human cognitive bandwidth—we can only imagine so many ways systems can break. At Huawei Cloud, we built a distributed multi-agent chaos engineering system that automates the entire chaos lifecycle: from hypothesis generation through source code analysis, to automated experiment planning and execution, to result analysis and service improvement recommendations.

This presentation shares our 12-month journey building and operating this system at hyperscale. We'll cover what actually works: using LLMs to analyze code for latent failure modes, automated topology-aware experiment design, and multi-agent coordination for complex scenarios. More importantly, we'll share what doesn't work: the hypothesis explosion problem, verification challenges, and the difficulty of proving resilience rather than just failing.

Attendees will learn architectural patterns for agent-based chaos systems, practical approaches to hypothesis generation from code and design docs, and realistic expectations for what these systems can achieve. We'll share production metrics, failure stories, and a framework for evaluating whether agentic chaos is right for your organization.

---

## Audience Level
**Intermediate to Advanced**

Prerequisites: Understanding of chaos engineering principles, distributed systems fundamentals, and basic LLM capabilities. Experience with chaos tools (Chaos Mesh, Gremlin, Litmus) helpful but not required.

---

## Topics Covered

### 1. The Problem with Human-Driven Chaos

**Cognitive Limitations:**
- Humans can only hypothesize ~5-10 failure modes per session
- Confirmation bias leads to testing expected failures
- Complexity explosion in microservice environments
- Knowledge silos: what one team knows, another doesn't

**Operational Constraints:**
- Game days require coordination, scheduling, and dedicated time
- Experiments are sporadic, not continuous
- Analysis depth varies by engineer expertise
- Improvement recommendations often lack specificity

**The Coverage Gap:**
```
Traditional Coverage = Human_Hypotheses × Execution_Time

Where:
- Human_Hypotheses ~ 10-50 per game day
- Execution_Time ~ 4-8 hours per session
- Coverage gaps: ~90% of failure modes never tested
```

### 2. The Agentic Chaos Architecture

**System Overview:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE INGESTION LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Code Analyzer│  │ Docs Indexer │  │ Topology Mapper      │  │
│  │ (AST/Call    │  │ (RAG over    │  │ (Service Mesh +      │  │
│  │  Graphs)     │  │  ADRs/Runbooks)│  │  Deployment Data)   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                  │                      │              │
│         └──────────────────┼──────────────────────┘              │
│                            ▼                                     │
├─────────────────────────────────────────────────────────────────┤
│                      AGENT CORE LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ┌────────────┐    ┌─────────────┐    ┌──────────────┐  │  │
│  │  │Investigator│───▶│Risk Assessor│───▶│  Architect   │  │  │
│  │  │  Agent     │    │   Agent     │    │   Agent      │  │  │
│  │  │(Hypothesis)│    │(Prioritization)│ │(Exp. Design) │  │  │
│  │  └────────────┘    └─────────────┘    └──────┬───────┘  │  │
│  │                                              │           │  │
│  │  ┌────────────┐                              ▼           │  │
│  │  │  Forensic  │◀─────────────────────────────────────────│  │
│  │  │  Agent     │    ┌─────────────┐                        │  │
│  │  │ (Analysis) │◀───│Safety Officer│◀──────────────────────┤  │
│  │  └─────┬──────┘    │   Agent     │                        │  │
│  │        │           │(Governance) │                        │  │
│  │        ▼           └─────────────┘                        │  │
│  │  ┌────────────┐                                           │  │
│  │  │ Engineer   │                                           │  │
│  │  │  Agent     │                                           │  │
│  │  │(Improvements)                                         │  │
│  │  └────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                   EXECUTION & SAFETY LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ CEP Adapter  │  │ Stop-Button  │  │ Steady State Monitor │  │
│  │(Chaos Mesh,  │  │   Monitor    │  │   (SLO Watcher)      │  │
│  │ Litmus, etc) │  │(Auto-abort)  │  │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Hypothesis Generation from Code

**What Actually Works:**

**Static Analysis + LLM Reasoning:**
- AST parsing to identify external calls, retry logic, circuit breakers
- Call graph analysis for dependency chains
- Exception handler analysis for missing error handling
- Timeout configuration mining

**Example Hypothesis Generation:**
```python
# Agent detects from code:
external_api_call(url, timeout=None)  # No timeout!

# Generated Hypothesis:
"""
Service A calls External API without timeout configuration.
If External API hangs (network partition, overload), Service A
threads will exhaust, causing cascade failure.

Confidence: 85%
Blast Radius: High (critical path)
Recommended Test: Inject 10s latency, measure thread pool exhaustion
"""
```

**Design Doc Analysis (RAG):**
- Extract stated assumptions about failure modes
- Identify gaps between documented architecture and actual implementation
- Find implicit dependencies not explicit in code

**Topology-Aware Hypothesis:**
- Cross-reference code hypotheses with actual deployment topology
- Identify single points of failure in cluster configuration
- Detect cross-zone/cross-region dependencies

### 4. What Works: Planning and Execution

**Effective Patterns:**

**1. Prioritized Experiment Queue**
- Risk-scored hypothesis queue
- Automatic scheduling based on:
  - Blast radius estimation
  - Current system health
  - Business criticality
  - Recent changes (drift detection)

**2. Progressive Fault Injection**
```
Stage 1: Latency (10ms → 50ms → 200ms → 1s)
Stage 2: Packet loss (1% → 5% → 10%)
Stage 3: Resource exhaustion (CPU, memory)
Stage 4: Complete service failure
```

**3. Automated Guardrails**
- Pre-execution health checks
- Real-time SLO monitoring
- Automatic experiment abortion on threshold breach
- Blackout window enforcement (deployments, peak traffic)

**4. Multi-Agent Coordination**
- Lead agent: Orchestrates experiment flow
- Observer agent: Monitors steady-state metrics
- Analyst agent: Processes results in real-time
- Reporter agent: Generates human-readable findings

**Production Metrics:**
| Metric | Traditional | Agentic | Improvement |
|--------|-------------|---------|-------------|
| Hypotheses/month | 50 | 2,400 | 48x |
| Experiments/month | 20 | 800 | 40x |
| Time to hypothesis | 4 hours | 15 minutes | 16x faster |
| Coverage (% critical paths) | 35% | 89% | 2.5x |

### 5. What Doesn't Work

**1. The Hypothesis Explosion Problem**

**Issue:**
- Agents generate too many hypotheses
- 80% are low-value or duplicate
- Human review bottleneck

**Failed Approaches:**
- Naive scoring: Agents self-rate, still too many
- Hard limits: Cuts off potentially valuable hypotheses
- Automated filtering: Too aggressive, loses signal

**Partial Solution:**
- Tiered confidence thresholds
- Deduplication via semantic similarity
- Service owner review sessions (weekly, not real-time)

**2. Verification Challenges**

**The Fundamental Problem:**
- Chaos proves systems fail, not that they're resilient
- "It didn't break" ≠ "It's reliable"
- Silent failures are hardest to detect

**What Didn't Work:**
- Assuming green metrics = success
- Trusting agent interpretation of results
- Not accounting for experiment interference

**Better Approach:**
- Explicit success criteria before each experiment
- Multi-signal verification (logs + metrics + traces)
- Known-failure injection (test the test)

**3. The Context Window Limit**

**Challenge:**
- Complex systems exceed model context
- Agents lose the "big picture" in long experiments
- Cross-service dependencies get missed

**Workarounds:**
- Hierarchical agent delegation
- Summarization checkpoints
- Focused scope per agent (service-specific)

**4. Improvement Recommendation Quality**

**Mixed Results:**
```
Good Recommendations (60%):
- "Add timeout to UserServiceClient (line 47)"
- "Implement circuit breaker for PaymentService"
- "Configure retry with exponential backoff"

Vague/Unhelpful (30%):
- "Improve error handling"
- "Add more monitoring"
- "Consider adding resilience"

Dangerous/Wrong (10%):
- Incorrect root cause analysis
- Recommendations that would introduce bugs
- Breaking existing resilience patterns
```

**Key Insight:** Agents are better at finding problems than proposing solutions. Shift focus to detection, use humans for remediation.

### 6. Result Analysis and Improvement Suggestions

**Effective Analysis Pipeline:**

```
┌────────────────────────────────────────────────────────────────┐
│                    RESULT ANALYSIS FLOW                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. COLLECT                                                    │
│     ├── Metrics (Prometheus, Datadog)                         │
│     ├── Logs (ELK, Loki)                                      │
│     ├── Traces (Jaeger, Zipkin)                               │
│     └── Events (Kubernetes events, alerts)                    │
│                                                                │
│  2. CORRELATE                                                  │
│     ├── Time-align all signals                                │
│     ├── Cross-reference with fault injection timeline         │
│     └── Identify cascade patterns                             │
│                                                                │
│  3. ANALYZE                                                    │
│     ├── Did fallback mechanisms trigger?                      │
│     ├── Were SLOs maintained?                                 │
│     ├── What user impact occurred?                            │
│     └── How long to recovery?                                  │
│                                                                │
│  4. RECOMMEND                                                  │
│     ├── Specific code changes (with line numbers)             │
│     ├── Configuration adjustments                             │
│     ├── Architecture improvements                             │
│     └── Runbook updates                                        │
│                                                                │
│  5. VALIDATE                                                   │
│     ├── Human review of recommendations                        │
│     ├── Test suggestion in staging                            │
│     └── Re-run chaos to verify improvement                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Recommendation Quality Framework:**

| Dimension | Score | Description |
|-----------|-------|-------------|
| Specificity | 1-5 | How precise is the recommendation? |
| Actionability | 1-5 | Can it be implemented directly? |
| Correctness | 1-5 | Is it technically accurate? |
| Priority | 1-5 | How important is it? |
| **Overall** | **1-25** | Weighted average |

**Production Stats:**
- Average recommendation score: 16/25
- High-quality (20+): 35%
- Medium quality (12-19): 50%
- Low quality (<12): 15%

### 7. Lessons Learned

**What We'd Do Differently:**

1. **Start smaller**: We began with 50 services, should have started with 5
2. **Human review is essential**: Early assumption that agents could auto-improve was wrong
3. **Invest in guardrails**: Safety infrastructure took 3x longer than expected
4. **Metrics observability is prerequisite**: You can't test what you can't measure
5. **Chaos is not resilience**: Proving failure modes exist doesn't prove reliability

**What Surprised Us:**

1. **Hypothesis quality > quantity**: Fewer, better hypotheses are more valuable
2. **Silent failures are common**: 40% of discovered issues had no visible symptoms
3. **Agents hallucinate experiments**: Must validate generated test plans
4. **Cross-service issues dominate**: 70% of critical issues involved service interactions
5. **Improvement is harder than detection**: Finding bugs is easier than fixing them

### 8. When to Use Agentic Chaos

**Good Fit:**
- Large microservice environments (50+ services)
- Frequent changes (continuous deployment)
- Strong observability foundation
- Team capacity to review recommendations
- High-availability requirements

**Not Yet Ready:**
- Monolithic applications
- Sparse observability
- No chaos engineering experience
- Limited engineering bandwidth
- Low tolerance for experimentation

**ROI Threshold:**
```
Agentic Chaos ROI = (Issues_Found × MTTR_Saved) - System_Cost

Where System_Cost = Infrastructure + Agent_Tokens + Human_Review_Time

Breakeven: ~50 services with 2+ incidents/month preventable
```

---

## Key Takeaways

1. **Agents excel at hypothesis generation** but struggle with verification
2. **Start with detection, not remediation** - humans should fix, agents should find
3. **Quality over quantity** - fewer, better hypotheses beat volume
4. **Guardrails are infrastructure** - invest heavily in safety
5. **This is not fully autonomous** - human oversight remains critical

---

## Proposed Duration
**45 minutes** (35-minute presentation + 10-minute Q&A)

---

## Speaker Bio
*[To be filled with speaker details]*

**Company:** Huawei Cloud
**Experience:** 12+ months building and operating distributed multi-agent chaos engineering system at hyperscale

---

## Related Work and References

1. "Chaos Engineering" - Nora Jones & Casey Rosenthal
2. "Building Secure and Reliable Systems" - Google
3. "Learning from Failures" - L. Peter Deutsch
4. Chaos Mesh Documentation - https://chaos-mesh.org
5. Litmus Chaos Documentation - https://litmuschaos.io
6. Internal Huawei Cloud MACES architecture documentation

---

## Why This Talk?

Chaos engineering is evolving from human-driven game days to automated continuous verification. This presentation provides the first comprehensive look at what happens when you add AI agents to the chaos engineering loop. Unlike vendor talks that promise autonomous resilience, this presentation delivers honest, experience-based insights into what works and what doesn't.

The content fills a critical gap: there's enormous interest in AI-powered operations, but almost no published experience from large-scale production deployments. Attendees will leave with realistic expectations, practical architectural patterns, and a clear framework for evaluating whether agentic chaos is appropriate for their organization.