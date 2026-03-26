# Agentic Chaos: What Works and What Doesn't in Multi-Agent Chaos Engineering

## Presentation Title
Agentic Chaos: What Works and What Doesn't in Multi-Agent Chaos Engineering Systems

## Abstract
Chaos engineering has evolved from manual failure injection to automated resilience testing, but the next frontier is agentic chaos—intelligent, adaptive systems that can autonomously design, execute, and learn from chaos experiments. Based on our experience building a distributed multi-agent chaos engineering system at Huawei Cloud, this talk reveals the hard-won lessons about what actually works in production versus what looks good on paper.

Our system leverages multiple specialized agents working in concert: hypothesis generators that analyze source code, design documents, and deployment topology to identify potential failure modes; planning agents that coordinate safe experiment execution across distributed services; and analysis agents that correlate chaos results with service metrics to generate actionable improvement suggestions. We'll dive deep into the architectural decisions that made this possible—from agent communication patterns and consensus mechanisms to safety guardrails and rollback strategies.

However, the reality is messy. We'll share candid stories of agent conflicts, unexpected emergent behaviors, and reliability challenges that emerged when scaling from single-service to platform-wide chaos automation. Most importantly, we'll present a practical framework for evaluating when multi-agent chaos is worth the complexity overhead versus simpler approaches, along with concrete patterns for incremental adoption.

Attendees will leave with actionable insights for building their own agentic chaos systems, including agent role definitions, communication protocols, safety boundaries, and metrics for measuring chaos effectiveness—not just system resilience, but the reliability of the chaos system itself.

## Target Audience
- SREs and platform engineers implementing or considering chaos engineering automation
- Engineering leaders evaluating multi-agent architectures for operational tooling
- Researchers and practitioners interested in applied multi-agent systems in production environments
- Anyone who has struggled with scaling chaos engineering beyond basic failure injection

## Format
35-minute talk + 10 minutes Q&A

## Detailed Outline

### Introduction (3 minutes)
- The evolution of chaos engineering: from manual to automated to agentic
- Why traditional chaos tools hit limits at scale
- Overview of Huawei Cloud's distributed multi-agent chaos system

### Architecture Deep Dive (8 minutes)
- **Hypothesis Generation Agents**: 
  - Source code analysis for dependency mapping and failure point identification
  - Design document parsing for architectural constraint understanding
  - Deployment topology analysis for blast radius calculation
  - Multi-modal input fusion techniques
  
- **Planning and Coordination Agents**:
  - Distributed consensus for safe experiment scheduling
  - Resource-aware execution planning across microservices
  - Conflict resolution between concurrent chaos experiments
  - Integration with change management and incident response systems

- **Analysis and Learning Agents**:
  - Automated result correlation across metrics, logs, and traces
  - Service improvement suggestion generation
  - Feedback loops for continuous hypothesis refinement
  - Measuring chaos effectiveness beyond simple pass/fail

### What Actually Worked (7 minutes)
- **Successful Patterns**:
  - Specialized agent roles with clear boundaries of responsibility
  - Asynchronous communication with explicit contracts
  - Progressive rollout strategies for new agent capabilities
  - Human-in-the-loop approval gates for high-risk experiments
  
- **Key Technical Decisions**:
  - Event-driven vs. request-response communication patterns
  - State management approaches for distributed agent coordination
  - Observability instrumentation for agent behavior monitoring
  - Testing strategies for multi-agent system reliability

### What Didn't Work (and Why) (10 minutes)
- **Agent Conflicts and Emergent Behaviors**:
  - Cases where agents optimized for local objectives created global problems
  - Unexpected interaction patterns between hypothesis and planning agents
  - Race conditions in distributed experiment execution
  
- **Reliability Challenges**:
  - Agent availability requirements vs. chaos system availability
  - Cascading failures within the chaos system itself
  - Debugging complex multi-agent interactions in production
  
- **Operational Overhead**:
  - Monitoring and alerting complexity for agent health
  - Configuration management across heterogeneous agent types
  - Skill fragmentation and knowledge silos among agent maintainers

### Practical Framework for Adoption (5 minutes)
- **When to Use Multi-Agent Chaos**:
  - Decision matrix based on organization size, service complexity, and maturity
  - Cost-benefit analysis of agent complexity vs. chaos coverage
  - Incremental adoption pathways from single-agent to multi-agent systems
  
- **Getting Started Guidelines**:
  - Minimum viable agent set for different use cases
  - Essential safety patterns and guardrails
  - Metrics for measuring both chaos effectiveness and agent reliability

### Conclusion and Q&A Preparation (2 minutes)
- Key takeaways about the reality of agentic chaos engineering
- Future directions: self-healing agents, cross-organizational chaos, and AI-enhanced hypothesis generation
- Open questions and areas for community collaboration

## Alignment with SRECon26 Themes

This proposal directly addresses multiple SRECon26 focus areas:

**AI Everywhere**: Demonstrates practical application of AI/ML agents in critical SRE workflows, moving beyond hype to real-world implementation challenges and solutions.

**Dealing with Uncertainty**: Chaos engineering is fundamentally about managing uncertainty, and agentic systems introduce additional layers of unpredictability that must be carefully controlled.

**Human Factors**: Explores the human aspects of working with autonomous agents, including trust calibration, mental model alignment, and maintaining human expertise alongside automation.

**Traditional SRE Favorites**: Builds upon established chaos engineering principles while extending them to handle modern distributed system complexity.

**Different Perspectives**: Presents both the technical architecture perspective and the operational reality perspective, showing how theoretical designs meet practical constraints in production environments.

## Unique Value Proposition

Unlike generic talks about chaos engineering or AI agents, this presentation offers:

1. **Real Production Experience**: Concrete examples from Huawei Cloud's actual implementation, not theoretical concepts
2. **Failure Transparency**: Honest discussion of what didn't work and why, providing valuable lessons for others
3. **Practical Frameworks**: Actionable guidance for organizations considering similar approaches
4. **Multi-Dimensional Analysis**: Considers technical, operational, and human factors simultaneously
5. **Community Contribution**: Shares patterns and anti-patterns that can benefit the broader SRE community

## Speaker Qualifications

The speaker(s) have extensive experience building and operating large-scale distributed systems at Huawei Cloud, with specific expertise in:
- Chaos engineering implementation and scaling
- Multi-agent system design and operation
- SRE practices in cloud-native environments
- Reliability engineering for AI/ML systems
- Production incident response and postmortem analysis

This combination of theoretical knowledge and practical experience ensures that the presentation will be both technically rigorous and operationally relevant.