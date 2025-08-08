# System Architecture: Geotab Add-In Generator

This document outlines the multi-agent system architecture for the automated generation of Geotab Add-Ins.

## Flow Diagram

The system follows a sequential workflow managed by an Orchestrator Agent, with feedback loops for quality assurance. The communication protocol between agents is MCP (Multi-Agent Communication Protocol).

```mermaid
graph TD
    subgraph "User Interaction"
        User[("👤 User")]
    end

    subgraph "Core System"
        Orchestrator(Orchestrator Agent)
        LLM[("✨ Gemini LLM")]
    end

    subgraph "Specialist Agents (Worker Guild)"
        Analyst(Analyst Agent)
        Designer(Designer Agent)
        Coder(Coder Agent)
        Tester(Tester Agent)
        Deployer(Deployer Agent)
    end

    subgraph "Final Product"
        AddIn{{"</> Deployed Add-In"}}
    end

    User -- "Natural Language Request (e.g., 'Create a map Add-In')" --> Orchestrator
    Orchestrator -- "1. Analyze Prompt & Create Plan" --> LLM
    LLM -- "2. Structured Plan & Task Breakdown" --> Orchestrator
    Orchestrator -- "3. Delegate: Analyze Requirements" --> Analyst
    Analyst -- "4. Refined Specifications" --> Orchestrator
    Orchestrator -- "5. Delegate: Design Solution" --> Designer
    Designer -- "6. Technical Design / Blueprints" --> Orchestrator
    Orchestrator -- "7. Delegate: Write Code" --> Coder
    Coder -- "8. Generated Code" --> Orchestrator
    Orchestrator -- "9. Delegate: Test Code" --> Tester
    Tester -- "10a. Bugs / Issues Found" --> Orchestrator
    Orchestrator -- "Delegate: Fix Bugs" --> Coder
    Tester -- "10b. Code Approved" --> Orchestrator
    Orchestrator -- "11. Delegate: Deploy Add-In" --> Deployer
    Deployer -- "12. Packaged Add-In" --> AddIn
    Orchestrator -- "13. Notify: Add-In Ready" --> User
```

## Agent Responsibilities

*   **Orchestrator Agent**: Manages the overall workflow, communicates with the LLM, and delegates tasks to specialist agents.
*   **Analyst Agent**: Transforms the user's request into detailed functional specifications.
*   **Designer Agent**: Creates the technical architecture and UI/UX design based on the specifications.
*   **Coder Agent**: Writes the source code based on the technical design.
*   **Tester Agent**: Validates the generated code against specifications and reports bugs.
*   **Deployer Agent**: Packages the final code for deployment.