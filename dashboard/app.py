import streamlit as st
import pandas as pd
import subprocess


# Configure Streamlit page settings
st.set_page_config(page_title="Keyword Ranking Analyzer", layout="wide")

st.title("Keyword Ranking Analysis Dashboard")

# Upload input Excel file
uploaded_file = st.file_uploader("Upload Keyword Excel File", type=["xlsx"])

if uploaded_file:
    # Save uploaded file to input directory
    with open("data/input/keywords_input.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Run Keyword Ranking Analysis"):
        # Execute the main analysis pipeline
        with st.spinner("Running analysis..."):
            subprocess.run(["python", "main.py"])

        st.success("Analysis completed successfully.")

        # Load generated output report
        df = pd.read_excel("data/output/keyword_ranking_report.xlsx")

        # Display summary metrics
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Keywords", len(df))

        col2.metric(
            "Page-1 Organic Keywords",
            len(df[df["google links"].apply(lambda x: isinstance(x, int) and x <= 10)])
        )

        col3.metric(
            "Not Ranking (Organic & Places)",
            len(
                df[
                    (df["google places"] == "Not Found")
                    & (df["google links"] == "Not Found")
                ]
            )
        )

        # Display detailed ranking table
        st.dataframe(
            df[["keyword", "google places", "google links", "page number"]],
            use_container_width=True
        )

        # Provide option to download the Excel report
        st.download_button(
            "Download Excel Report",
            data=open("data/output/keyword_ranking_report.xlsx", "rb"),
            file_name="keyword_ranking_report.xlsx"
        )
