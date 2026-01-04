import os


def export_mermaid_graph():
    """
    Generates a detailed Mermaid diagram showing:
    - High-level LangGraph orchestration
    - Internal agents used inside Rank Checker
    """

    mermaid_text = """flowchart LR

    %% High-level flow
    Start([Start])
    Reader[Keyword Reader Agent]
    RankChecker[Rank Checker]
    Report[Report Generator]
    End([End])

    Start --> Reader --> RankChecker --> Report --> End

    %% Rank Checker internals
    subgraph RankChecker["Rank Checker Internals"]
        RF[Rank Fetcher Agent]
        API[SerpAPI Tool]
        RA[Rank Analyzer Agent]
        ORG[Organic Rank Analyzer]
        PLC[Places Rank Analyzer]

        RF --> API
        API --> RA
        RA --> ORG
        RA --> PLC
    end

    %% Logical connections
    Reader --> RF
    ORG --> Report
    PLC --> Report
    """

    os.makedirs("docs", exist_ok=True)
    output_path = "docs/langgraph_orchestration.md"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 🧠 LangGraph Orchestration Diagram\n\n")
        f.write("```mermaid\n")
        f.write(mermaid_text)
        f.write("\n```")

    print(f"✅ Mermaid orchestration diagram generated at: {output_path}")


if __name__ == "__main__":
    export_mermaid_graph()
