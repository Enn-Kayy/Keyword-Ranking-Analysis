from graphs.ranking_workflow import build_graph


if __name__ == "__main__":
    """
    Entry point for the keyword ranking analysis pipeline.
    Builds the LangGraph workflow and triggers execution.
    """

    app = build_graph()

    app.invoke({
        "input_file": "data/input/keywords_input.xlsx"
    })
