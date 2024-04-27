import nest_asyncio
import streamlit as st
from duckduckgo_search import DDGS
from phi.assistant import Assistant
from phi.utils.log import logger

from assistants import get_travel_planner_assistant  # type: ignore

nest_asyncio.apply()
st.set_page_config(
    page_title="Travel Planner",
    page_icon=":earth_americas:",
)
st.title("Travel Planner")
st.markdown("##### :earth_americas: Built using [phidata](https://github.com/phidatahq/phidata)")


def restart_assistant():
    logger.debug("---*--- Restarting Assistant ---*---")
    st.session_state["travel_assistant"] = None
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
    travel_assistant: Assistant
    if "travel_assistant" not in st.session_state or st.session_state["travel_assistant"] is None:
        travel_assistant = get_travel_planner_assistant(model=model)
        st.session_state["travel_assistant"] = travel_assistant
    else:
        travel_assistant = st.session_state["travel_assistant"]

    # Get user preferences
    st.sidebar.markdown("## Travel Preferences")
    destination = st.sidebar.text_input("Destination (city or country)", value="Paris")
    travel_duration = st.sidebar.number_input("Duration (in days)", min_value=1, value=7)
    travel_budget = st.sidebar.number_input("Budget (in USD)", min_value=100, value=2000)
    interests = st.sidebar.multiselect(
        "Interests",
        options=[
            "Culture", "History", "Food", "Nature", "Outdoor Activities",
            "Nightlife", "Shopping", "Architecture", "Museums"
        ],
        default=["Culture", "History", "Food"],
    )

    # Generate Travel Itinerary
    generate_itinerary = st.sidebar.button("Generate Itinerary")
    if generate_itinerary:
        with st.spinner("Generating Itinerary"):
            itinerary_input = f"Please generate a {travel_duration}-day travel itinerary for {destination} with a budget of ${travel_budget} and focusing on the following interests: {', '.join(interests)}."
            final_itinerary = ""
            final_itinerary_container = st.empty()
            for delta in travel_assistant.run(itinerary_input):
                final_itinerary += delta  # type: ignore
                final_itinerary_container.markdown(final_itinerary)

    st.sidebar.markdown("---")
    if st.sidebar.button("New Search"):
        restart_assistant()


main()