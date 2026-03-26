# SRECon26 Presentation Proposal

## Title
**Agentic SRE: Navigating the Messy Reality of SRE Agents**

---

## Abstract (150-200 words)

The promise of AI-powered SRE agents is compelling: autonomous incident response, self-healing systems, and round-the-clock reliability without human intervention. But the reality is far messier. After 18 months of deploying SRE agents across production environments at Huawei Cloud, we've learned that the gap between demo and production is enormous.

This presentation shares hard-won insights from the trenches of agentic SRE. We'll explore the fundamental architectural decisions that determine success or failure: local vs. remote agents, distributed vs. single-instance deployments, and multi-agent orchestration vs. monolithic designs. Each choice introduces trade-offs in latency, reliability, and operational complexity that aren't obvious from vendor demos.

We'll dive deep into the challenges that don't make it into marketing materials: Model Context Protocol (MCP) fragmentation across tools, the reliability crisis of agent skills, and the uncomfortable truth that agents themselves become critical infrastructure requiring SRE discipline. The talk concludes with practical frameworks for evaluating when agents help vs. hinder, and how to build SRE practices that account for unreliable AI components.

Attendees will leave with realistic expectations, architectural patterns, and a roadmap for responsibly integrating agents into SRE workflows.

---

## Audience Level
**Intermediate to Advanced**

Prerequisites: Basic understanding of SRE principles, distributed systems, and LLM fundamentals. Familiarity with agents/AI concepts helpful but not required.

---

## Topics Covered

### 1. The SRE Agent Landscape
- Current state of AI agents in production environments
- Vendor promises vs. operational reality
- The "demo effect": why agents look better than they perform

### 2. Architectural Decisions and Trade-offs

#### Local vs. Remote Agents
| Aspect | Local Agents | Remote Agents |
|--------|--------------|---------------|
| Latency | Sub-10ms response | 100-500ms network overhead |
| Data Privacy | Full control | Requires data egress |
| Scalability | Hardware-limited | Cloud-elastic |
| Reliability | Single point of failure | Distributed risk |
| Model Access | Limited to local models | Full cloud model access |

#### Single-Instance vs. Distributed Agents
- Single-instance: Simpler state management, easier debugging
- Distributed: Better fault isolation, parallel execution, complex coordination

#### Monolithic vs. Multi-Agent Systems
- Monolithic: Easier to reason about, single failure domain
- Multi-Agent: Specialized capabilities, complex orchestration, emergent behaviors

### 3. The MCP Challenge

**What is MCP?**
Model Context Protocol provides standardized interfaces for agents to interact with tools, databases, and APIs. In theory, this enables interoperability. In practice:

- **Fragmentation**: Every vendor implements MCP differently
- **Version Hell**: Incompatible protocol versions across tools
- **Skill Reliability**: Tools that work 95% of the time break agents 50% of the time
- **Discovery Gaps**: No universal skill registry or capability negotiation

**Real-World Impact:**
- 30% of agent failures traced to tool/skill issues
- Average of 3-4 retry attempts per complex operation
- Significant engineering overhead maintaining custom MCP adapters

### 4. The Reliability Crisis

**Agent Skills Are Fragile:**
- Skills assume clean, well-formatted inputs
- Real-world data is messy, incomplete, inconsistent
- Error handling is often superficial
- Cascading failures when one skill fails

**Measuring Agent Reliability:**
```
Agent Success Rate = Skill_Reliability ^ Number_of_Skills

Example:
- 5 skills in pipeline
- Each skill 95% reliable
- Overall: 0.95^5 = 77.6% success rate
```

**Strategies for Improvement:**
- Redundant skill implementations
- Graceful degradation paths
- Human-in-the-loop for critical decisions
- Extensive monitoring and alerting on agent behavior

### 5. SRE for Agents (Meta-Reliability)

**The Uncomfortable Truth:**
Agents are now critical infrastructure. They need their own SRE practices:

| Traditional SRE | Agent SRE |
|-----------------|-----------|
| Monitor services | Monitor agent decisions |
| Set SLOs for uptime | Set SLOs for accuracy |
| Handle incidents | Handle hallucinations |
| Capacity planning | Token budget planning |
| Deploy canaries | Prompt version control |

**Agent Reliability Stack:**
1. **Observability**: Log every decision, tool call, and output
2. **Guardrails**: Define boundaries for autonomous action
3. **Fallbacks**: When agents fail, who/what takes over?
4. **Human Escalation**: Clear criteria for human intervention
5. **Cost Control**: Prevent runaway token consumption

### 6. Lessons from Huawei Cloud Deployment

**What Worked:**
- Starting with narrow, well-defined use cases
- Building extensive evaluation frameworks
- Maintaining human oversight for critical decisions
- Investing in robust error handling

**What Didn't Work:**
- Expecting agents to handle novel situations
- Underestimating skill maintenance burden
- Ignoring the "last 10%" edge cases
- Assuming cloud model availability

**Key Metrics from Production:**
- 78% reduction in routine incident triage time
- 15% false positive rate requiring human correction
- 40% of agent actions need human review
- 2-3 skill fixes per week on average

---

## Key Takeaways

1. **Start Small**: Begin with narrow, high-value use cases. Expand gradually.
2. **Expect Failure**: Build systems that assume agents will fail, not succeed.
3. **Measure Everything**: You can't improve what you don't measure.
4. **Humans Remain Critical**: The best agent systems augment humans, not replace them.
5. **Treat Agents as Infrastructure**: They need SRE discipline too.

---

## Proposed Duration
**45 minutes** (35-minute presentation + 10-minute Q&A)

---

## Speaker Bio
*[To be filled with speaker details]*

**Company:** Huawei Cloud
**Experience:** 18+ months deploying SRE agents in production at scale

---

## Related Work and References

1. "Site Reliability Engineering" - Google SRE Book
2. "Building Secure and Reliable Systems" - Google
3. Model Context Protocol Specification - Anthropic
4. "AI Agents in Production: Lessons Learned" - Various industry reports
5. Internal Huawei Cloud agent deployment documentation

---

## Why This Talk?

The SRE community is flooded with AI agent hype but starved for honest, experience-based guidance. This presentation fills that gap by sharing real-world lessons from large-scale production deployments. Attendees will leave with practical knowledge they can immediately apply, avoiding costly mistakes and setting realistic expectations for their own agent initiatives.

The talk is particularly timely as organizations move from "should we use agents?" to "how do we make agents actually work in production?" This is the critical operational knowledge gap that this presentation addresses.