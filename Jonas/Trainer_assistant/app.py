import nest_asyncio
import streamlit as st
from phi.assistant import Assistant
from phi.utils.log import logger

from assistants import get_workout_planner_assistant  # type: ignore

nest_asyncio.apply()
st.set_page_config(
    page_title="Workout Planner",
    page_icon=":muscle:",
)
st.title("Workout Planner")
st.markdown("##### :muscle: Built using [phidata](https://github.com/phidatahq/phidata)")


def restart_assistant():
    logger.debug("---*--- Restarting Assistant ---*---")
    st.session_state["workout_assistant"] = None
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
    workout_assistant: Assistant
    if "workout_assistant" not in st.session_state or st.session_state["workout_assistant"] is None:
        workout_assistant = get_workout_planner_assistant(model=model)
        st.session_state["workout_assistant"] = workout_assistant
    else:
        workout_assistant = st.session_state["workout_assistant"]

    # Get user preferences
    st.sidebar.markdown("## Fitness Goals")
    fitness_goal = st.sidebar.selectbox(
        "What is your primary fitness goal?",
        options=["Build Muscle", "Lose Weight", "Improve Endurance", "Increase Flexibility"],
    )
    experience_level = st.sidebar.selectbox(
        "What is your experience level?",
        options=["Beginner", "Intermediate", "Advanced"],
    )
    available_equipment = st.sidebar.multiselect(
        "What equipment do you have access to?",
        options=["Bodyweight", "Dumbbells", "Barbell", "Resistance Bands", "Gym Machines"],
    )
    workout_duration = st.sidebar.number_input("How many minutes can you workout per day?", min_value=15, max_value=120, value=60)

    # Generate Workout Plan
    generate_plan = st.sidebar.button("Generate Workout Plan")
    if generate_plan:
        with st.spinner("Generating Workout Plan"):
            plan_input = f"Please generate a personalized workout plan for the following goals and preferences:\n\nFitness Goal: {fitness_goal}\nExperience Level: {experience_level}\nAvailable Equipment: {', '.join(available_equipment)}\nWorkout Duration: {workout_duration} minutes"
            final_plan = ""
            final_plan_container = st.empty()
            for delta in workout_assistant.run(plan_input):
                final_plan += delta  # type: ignore
                final_plan_container.markdown(final_plan)

    st.sidebar.markdown("---")
    if st.sidebar.button("New Plan"):
        restart_assistant()


main()