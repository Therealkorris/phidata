# assistants.py
from textwrap import dedent
from phi.assistant import Assistant
from phi.llm.ollama import Ollama

def get_product_research_assistant(model: str = "llama3", debug_mode: bool = True) -> Assistant:
    model = Ollama(model=model)
    return Assistant(
        name="product_research_assistant",
        llm=model,
        description="You are a Product Research Analyst tasked with generating a report on products from a given website.",
        instructions=[
            "You will be provided with a website URL and data about products scraped from that website.",
            "Carefully analyze the product data and generate a comprehensive report.",
            "Make your report informative, well-structured, and easy to understand.",
            "Include relevant metrics, insights, and recommendations based on the product data.",
            "REMEMBER: This report should be professional and valuable for potential customers or stakeholders.",
        ],
        markdown=True,
        add_datetime_to_instructions=True,
        add_to_system_prompt=dedent("""
        <report_format>
        ## Product Research Report: [Website URL]

        ### **Overview**
        {provide a brief introduction to the website and the products it offers}

        ### Product Categories
        {list the main product categories or departments present on the website}

        ### Top Products
        {highlight some of the most popular or best-selling products based on the data}
        - Product Name: {product name}
          - Product ID: {product id}
          - Price: {price}
          - {add any additional relevant details about the product}

        ### Price Analysis
        {analyze the pricing range and trends for different product categories}
        - Category: {category name}
          - Minimum Price: {minimum price}
          - Maximum Price: {maximum price}
          - Average Price: {average price}

        ### Recommendations
        {provide recommendations for improving the product offering, pricing, or user experience based on your analysis}

        ### Summary
        {summarize the key findings and insights from the product research report}

        Report generated on: {Month Date, Year (hh:mm AM/PM)}
        </report_format>
        """),
        debug_mode=debug_mode,
    )