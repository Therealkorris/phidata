import nest_asyncio
import streamlit as st
from scrapy import Spider
from twisted.internet import reactor
from phi.assistant import Assistant
from phi.utils.log import logger

from assistants import get_web_scraper_assistant  # type: ignore
from spiders.website_spider import WebsiteSpider

nest_asyncio.apply()
st.set_page_config(
    page_title="Web Scraper",
    page_icon=":spider_web:",
)
st.title("Web Scraper")
st.markdown("##### :spider_web: Built using [phidata](https://github.com/phidatahq/phidata)")


def restart_assistant():
    logger.debug("---*--- Restarting Assistant ---*---")
    st.session_state["web_scraper_assistant"] = None
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
    web_scraper_assistant: Assistant
    if "web_scraper_assistant" not in st.session_state or st.session_state["web_scraper_assistant"] is None:
        web_scraper_assistant = get_web_scraper_assistant(model=model)
        st.session_state["web_scraper_assistant"] = web_scraper_assistant
    else:
        web_scraper_assistant = st.session_state["web_scraper_assistant"]

    # Get user input
    st.sidebar.markdown("## Scraping Parameters")
    target_website = st.sidebar.text_input("Target Website (e.g., https://www.example.com)")
    scrape_subdomains = st.sidebar.checkbox("Scrape Subdomains", value=True)
    data_to_scrape = st.sidebar.multiselect(
        "Data to Scrape",
        options=[
            "Product Names",
            "Product Descriptions",
            "Product Prices",
            "Product Images",
            "Product Categories",
            "Product SKUs",
            "Product Reviews",
        ],
        default=["Product Names", "Product Prices", "Product SKUs"],
    )

    # Scrape Website
    scrape_website = st.sidebar.button("Scrape Website")
    if scrape_website:
        with st.spinner("Scraping Website"):
            scraped_data = []
            spider = WebsiteSpider(
                start_urls=[target_website],
                scrape_subdomains=scrape_subdomains,
                data_to_scrape=data_to_scrape,
            )
            runner = Spider.from_crawler(spider, stats=None)
            deferred = runner.crawl()
            reactor.run()
            scraped_data = spider.scraped_data

            scraped_data_container = st.empty()
            if scraped_data:
                scraped_data_container.write(scraped_data)
            else:
                scraped_data_container.warning("No data scraped from the website.")

    st.sidebar.markdown("---")
    if st.sidebar.button("New Scrape"):
        restart_assistant()


main()