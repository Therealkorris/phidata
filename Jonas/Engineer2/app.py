import nest_asyncio
import streamlit as st
import pandas as pd
from phi.assistant import Assistant
from phi.utils.log import logger

from assistants import get_engineering_assistant  # type: ignore

nest_asyncio.apply()
st.set_page_config(
    page_title="Engineering Assistant",
    page_icon=":wrench:",
)
st.title("Engineering Assistant")
st.markdown("##### :wrench: Built using [phidata](https://github.com/phidatahq/phidata)")


def restart_assistant():
    logger.debug("---*--- Restarting Assistant ---*---")
    st.session_state["engineering_assistant"] = None
    st.rerun()


def main() -> None:
    # Get LLM Model
    model = (
        st.sidebar.selectbox("Select LLM", options=["llama3", "llama3:instruct", "mixtral"])
        or "llama3"
    )
    # Set llm in session state
    if "model" not in st.session_state:
        st.session_state["model"] = model
    # Restart the assistant if model changes
    elif st.session_state["model"] != model:
        st.session_state["model"] = model
        restart_assistant()

    # Get the assistant
    engineering_assistant: Assistant
    if "engineering_assistant" not in st.session_state or st.session_state["engineering_assistant"] is None:
        engineering_assistant = get_engineering_assistant(model=model)
        st.session_state["engineering_assistant"] = engineering_assistant
    else:
        engineering_assistant = st.session_state["engineering_assistant"]

    # Get user input
    st.sidebar.markdown("## Task Requirements")
    task_type = st.sidebar.selectbox(
        "Task Type",
        options=["Data Analysis", "Documentation", "Code Review", "System Design"],
    )

    if task_type == "Data Analysis":
        data_file = st.sidebar.file_uploader("Upload Data File", type=["csv", "xlsx"])
        if data_file is not None:
            data = pd.read_csv(data_file) if data_file.name.endswith(".csv") else pd.read_excel(data_file)
            st.dataframe(data)
            analysis_type = st.sidebar.selectbox(
                "Analysis Type",
                options=["Exploratory Data Analysis", "Statistical Analysis", "Machine Learning"],
            )

    elif task_type == "Documentation":
        documentation_type = st.sidebar.selectbox(
            "Documentation Type",
            options=["Technical Documentation", "User Manual", "API Reference"],
        )
        topic = st.sidebar.text_input("Topic or Feature to Document")

    elif task_type == "Code Review":
        code_file = st.sidebar.file_uploader("Upload Code File", type=["py", "js", "java", "cpp", "cs", "go", "rb"])
        if code_file is not None:
            code_content = code_file.read().decode("utf-8")
            st.code(code_content, language=code_file.name.split(".")[-1])

    elif task_type == "System Design":
        system_type = st.sidebar.selectbox(
            "System Type",
            options=["Web Application", "Mobile Application", "Distributed System", "Microservices Architecture"],
        )
        design_requirements = st.sidebar.text_area("Design Requirements")

    # Generate Output
    generate_output = st.sidebar.button("Generate Output")
    if generate_output:
        with st.spinner("Processing Task"):
            task_input = f"Task Type: {task_type}\n\n"
            if task_type == "Data Analysis":
                task_input += f"Data:\n{data}\n\nAnalysis Type: {analysis_type}"
            elif task_type == "Documentation":
                task_input += f"Documentation Type: {documentation_type}\nTopic: {topic}"
            elif task_type == "Code Review":
                task_input += f"Code:\n{code_content}"
            elif task_type == "System Design":
                task_input += f"System Type: {system_type}\nDesign Requirements:\n{design_requirements}"

            final_output = ""
            final_output_container = st.empty()
            for delta in engineering_assistant.run(task_input):
                final_output += delta  # type: ignore
                final_output_container.markdown(final_output)

    st.sidebar.markdown("---")
    if st.sidebar.button("New Task"):
        restart_assistant()


main()