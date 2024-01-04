import os
import streamlit as st
from crewai import Agent, Task, Crew, Process


# Set up CrewAI
my_secret = "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"
os.environ["OPENAI_API_KEY"] = my_secret

# Define your agent with a role and goal
productivity_expert = Agent(
    role="Productivity Expert",
    goal="Help individuals improve time management and daily effectiveness",
    backstory="As a renowned productivity expert, you are tasked with designing an end-of-day review for individuals seeking to improve their time management and daily effectiveness. Create a set of five insightful questions that encourage reflection on daily activities, time management, goal progress, and personal well-being: Reflection on Accomplishments: What are the top three tasks I completed today that brought me closer to my long-term goals? Time Management Assessment: Which part of the day was I most productive, and what strategies helped me stay focused? Challenges and Learning: What challenges did I encounter today, and what did I learn from them? Personal Well-being Check: How did my work today contribute to my overall well-being and work-life balance? Goal Alignment: How do today's activities align with my broader personal and professional goals? Summary Action: After answering these questions, identify one specific action or change you can implement tomorrow to enhance your productivity and personal satisfaction based on today's reflections.",
    verbose=True,
    allow_delegation=False,
)

# Instantiate the crew with a sequential process
crew = Crew(
    agents=[productivity_expert],
    tasks=[],
    verbose=False,
    process=Process.sequential,
)

# Streamlit UI
st.title("Productivity Expert Interaction")

# Display chat history
chat_history_container = st.container()

# Use a dictionary for session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "my_text" not in st.session_state:
    st.session_state.my_text = ""
# Apply custom CSS to move the text input to the bottom and add a black border


def submit():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""


st.text_input("", key="widget", on_change=submit, placeholder="Ask your Question")

st.markdown(
    """
    <style>
        .stTextInput {
            position: fixed;
            bottom: 0;
            margin-bottom: 10px;
            width: 50%;
            padding: 5px;
        }
        .response-text {
            white-space: pre-wrap;
            padding: 5px;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Display entire chat history in the container
def display_chat_history():
    with chat_history_container:
        for chat_line in st.session_state.chat_history:
            role = chat_line.get("role")
            if role == "agent":
                with st.chat_message(role, avatar="👤"):
                    st.write(chat_line.get("message"))
            else:
                with st.chat_message(role, avatar="👨‍🦰"):
                    st.write(chat_line.get("message"))


user_input = st.session_state.my_text


# Function to get the agent's response
def get_agent_response(question, crew):
    if question:
        display_chat_history()

        user_message = {"role": "user", "message": question}
        st.session_state.chat_history.append(user_message)

        new_task = Task(
            description=question,
            agent=productivity_expert,
        )

        crew.tasks.append(new_task)

        result = crew.kickoff()
        agent_response = result

        agent_message = {"role": "agent", "message": agent_response}
        st.session_state.chat_history.append(agent_message)
        with st.chat_message("agent", avatar="👤"):
            st.write(agent_response)


if user_input:
    with st.chat_message("user", avatar="👨‍🦰"):
        st.write(user_input)
    get_agent_response(user_input, crew)
