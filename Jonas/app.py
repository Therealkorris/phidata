# app.py
import nest_asyncio
import streamlit as st
from scraper import ProductScraper
from phi.assistant import Assistant
from phi.utils.log import logger

from assistants import get_product_research_assistant  # type: ignore

nest_asyncio.apply()
st.set_page_config(
    page_title="Product Researcher",
    page_icon="🛒",
)
st.title("Product Researcher")
st.markdown("##### 🛒 Built using [phidata](https://github.com/phidatahq/phidata)")


def restart_assistant():
    logger.debug("---*--- Restarting Assistant ---*---")
    st.session_state["research_assistant"] = None
    st.rerun()


def main() -> None:
    # Get LLM Model
    model = st.sidebar.selectbox("Select LLM", options=["llama3", "llama3:instruct", "mixtral"], key="model_selection") or "llama3"

    # Set llm in session state
    if "model" not in st.session_state:
        st.session_state["model"] = model
    # Restart the assistant if model changes
    elif st.session_state["model"] != model:
        st.session_state["model"] = model
        restart_assistant()

    # Get the assistant
    research_assistant: Assistant
    if "research_assistant" not in st.session_state or st.session_state["research_assistant"] is None:
        research_assistant = get_product_research_assistant(model=model)
        st.session_state["research_assistant"] = research_assistant
    else:
        research_assistant = st.session_state["research_assistant"]

    # Get website URL for research
    website_url = st.sidebar.text_input(
        "🔍 Enter a website URL to research",
        value="https://www.ikea.com/",
        key="website_url_input",
    )

    # Generate Report
    generate_report = st.sidebar.button("Generate Report", key="generate_report_button")
    if generate_report:
        with st.spinner("Scraping website data..."):
            scraper = ProductScraper(website_url)
            product_data = scraper.scrape_products()

        if not product_data.empty:
            with st.container():
                draft_report_container = st.empty()
                draft_report_container.write(product_data)

            with st.spinner("Generating Report"):
                final_report = ""
                final_report_container = st.empty()
                report_message = f"Please generate a report about products from: {website_url}\n\n\n"
                report_message += str(product_data)
                for delta in research_assistant.run(report_message):
                    final_report += delta  # type: ignore
                    final_report_container.markdown(final_report)
        else:
            st.warning("No product data found on the website.")

    st.sidebar.markdown("---")
    if st.sidebar.button("New Run", key="new_run_button"):
        restart_assistant()


main()