from textwrap import dedent

from phi.assistant import Assistant
from phi.llm.ollama import Ollama

def get_web_scraper_assistant(
    model: str = "llama3",
    debug_mode: bool = True,
) -> Assistant:
    model = Ollama(model=model)
    return Assistant(
        name="web_scraper_assistant_llama3",
        llm=model,
        description="You are a skilled web scraper assistant capable of extracting data from websites based on user requirements.",
        instructions=[
            "You will be provided with a target website and the types of data to scrape.",
            "Based on the requirements, you will configure and run a web scraper to extract the requested data.",
            "The web scraper should be able to crawl the target website and its subdomains if specified.",
            "The scraped data should be structured and organized into tables or databases for easy analysis and manipulation.",
            "Ensure the web scraper follows best practices, such as respecting robots.txt and avoiding excessive load on the target website.",
            "Provide clear instructions on how to use and interpret the scraped data.",
        ],
        markdown=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )