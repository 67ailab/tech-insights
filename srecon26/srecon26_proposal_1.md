# Agentic SRE: Navigating the Messy Reality of SRE Agents

## Abstract
The promise of AI-powered SRE agents has captivated the industry, but the reality is far messier than vendor demos suggest. Drawing from our extensive experience implementing agentic SRE systems at Huawei Cloud, this talk cuts through the hype to reveal what actually works—and what doesn't—in production environments.

We'll explore the critical architectural decisions that determine success or failure: local agents embedded in service processes versus remote orchestration agents, distributed multi-agent systems versus monolithic single-instance approaches, and the trade-offs between coordination complexity and fault isolation. The session will dive deep into the practical challenges of Multi-Component Platforms (MCPs), including version skew, dependency conflicts, and the operational overhead of maintaining agent fleets.

Most importantly, we'll address the elephant in the room: how do you ensure reliability for the very agents tasked with ensuring system reliability? We'll share our framework for "SRE for Agents," covering observability patterns, circuit breakers for agent actions, graceful degradation strategies, and validation methodologies that prevent agents from becoming the weakest link in your reliability chain.

Attendees will leave with a realistic assessment of agentic SRE maturity, concrete architectural patterns validated in large-scale production, and practical guidance for avoiding the common pitfalls that turn promising agent initiatives into operational nightmares.

## Target Audience
- SREs and platform engineers evaluating or implementing AI/agent-based automation
- Engineering managers and architects designing next-generation reliability platforms
- Technical leaders responsible for AI strategy in infrastructure and operations

## Format
35-minute talk + 10 minutes Q&A

## Key Topics Covered
- **Architectural Patterns**: Local vs. remote agents, distributed vs. monolithic designs, coordination mechanisms
- **MCP Challenges**: Dependency management, version compatibility, deployment complexity, and testing strategies
- **Agent Reliability**: Observability for agent behavior, action validation, circuit breaking, and fallback mechanisms
- **Skill Fragmentation**: Managing inconsistent agent capabilities across services and environments
- **Production Lessons**: Real-world case studies from Huawei Cloud's agentic SRE implementation
- **Future Outlook**: Where agentic SRE is heading and what prerequisites organizations need to succeed

## Alignment with SRECon26 Themes
This proposal directly addresses the conference's focus on "different perspectives on SRE" by providing an honest, practitioner-focused view of agentic SRE that contrasts sharply with vendor marketing narratives. It tackles the "AI everywhere" theme while grounding discussions in real operational constraints and human factors. The talk provides both technical depth (architectural patterns, reliability engineering) and organizational insights (team structures, skill development, change management).