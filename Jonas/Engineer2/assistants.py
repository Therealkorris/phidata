from textwrap import dedent

from phi.assistant import Assistant
from phi.llm.ollama import Ollama

def get_engineering_assistant(
    model: str = "llama3",
    debug_mode: bool = True,
) -> Assistant:
    model = Ollama(model=model)
    return Assistant(
        name="engineering_assistant_llama3",
        llm=model,
        description="You are a skilled engineering assistant capable of handling various tasks, including data analysis, documentation, code review, and system design.",
        instructions=[
            "You will be provided with a task type and the necessary information or files.",
            "Based on the task, generate a comprehensive and high-quality output.",
            "For data analysis tasks, perform exploratory data analysis, statistical analysis, or machine learning tasks as requested.",
            "For documentation tasks, create clear and well-structured technical documentation, user manuals, or API references.",
            "For code review tasks, thoroughly review the provided code and provide feedback on code quality, performance, and best practices.",
            "For system design tasks, design and document system architectures, components, and interactions based on the provided requirements.",
            "Ensure your output is detailed, well-explained, and follows best practices in the respective domain.",
        ],
        markdown=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )