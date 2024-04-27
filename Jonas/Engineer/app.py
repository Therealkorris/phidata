import nest_asyncio
import streamlit as st
from phi.assistant import Assistant
from phi.utils.log import logger

from assistants import get_technical_writer_assistant  # type: ignore

nest_asyncio.apply()
st.set_page_config(
    page_title="Technical Documentation Generator",
    page_icon=":computer:",
)
st.title("Technical Documentation Generator")
st.markdown("##### :computer: Built using [phidata](https://github.com/phidatahq/phidata)")


def restart_assistant():
    logger.debug("---*--- Restarting Assistant ---*---")
    st.session_state["technical_writer_assistant"] = None
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
    technical_writer_assistant: Assistant
    if "technical_writer_assistant" not in st.session_state or st.session_state["technical_writer_assistant"] is None:
        technical_writer_assistant = get_technical_writer_assistant(model=model)
        st.session_state["technical_writer_assistant"] = technical_writer_assistant
    else:
        technical_writer_assistant = st.session_state["technical_writer_assistant"]

    # Get user input
    st.sidebar.markdown("## Documentation Requirements")
    topic = st.sidebar.text_input("Topic or Feature to Document", value="REST API")
    programming_language = st.sidebar.selectbox(
        "Programming Language",
        options=["Python", "JavaScript", "Java", "C++", "C#", "Go", "Ruby", "Other"],
    )
    documentation_type = st.sidebar.selectbox(
        "Documentation Type",
        options=["Overview", "Tutorial", "API Reference", "Code Examples"],
    )
    code_examples = st.sidebar.checkbox("Include Code Examples", value=True)

    # Generate Documentation
    generate_documentation = st.sidebar.button("Generate Documentation")
    if generate_documentation:
        with st.spinner("Generating Documentation"):
            doc_input = f"Please generate a {documentation_type} for {topic} in {programming_language}."
            if code_examples:
                doc_input += " Include relevant code examples."
            final_documentation = ""
            final_documentation_container = st.empty()
            for delta in technical_writer_assistant.run(doc_input):
                final_documentation += delta  # type: ignore
                final_documentation_container.markdown(final_documentation)

    st.sidebar.markdown("---")
    if st.sidebar.button("New Documentation"):
        restart_assistant()


main()