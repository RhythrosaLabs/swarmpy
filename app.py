import streamlit as st
from swarm import Swarm, Agent
import os

# Title for the app
st.title("Enhanced Swarm Multi-Agent Chat Interface")

# Step 1: API Key Input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# Proceed only if an API key is entered
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key

    # Step 2: Define agent handoff function
    def handoff_to_agent_b():
        return agent_b

    # Step 3: Initialize agents
    agent_a = Agent(
        name="Agent A",
        instructions="You are a helpful agent.",
        functions=[handoff_to_agent_b],
    )

    agent_b = Agent(
        name="Agent B",
        instructions="Only speak in Haikus.",
    )

    client = Swarm()

    # Step 4: Additional User Controls
    with st.sidebar:
        st.header("Agent Configuration")
        selected_agent = st.selectbox("Choose an agent to start the conversation:", ["Agent A", "Agent B"])
        agent_instructions = st.text_area("Customize agent instructions:", "You are a helpful agent.")

        # Apply new instructions based on user input
        if selected_agent == "Agent A":
            agent_a.instructions = agent_instructions
        else:
            agent_b.instructions = agent_instructions

    # Step 5: Initialize conversation history
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Step 6: Input area for user's message
    user_input = st.text_input("Enter your message:")

    # Step 7: Button to submit the message
    if st.button("Send"):
        if user_input:
            # Choose the selected agent to start
            starting_agent = agent_a if selected_agent == "Agent A" else agent_b

            # Run the conversation
            response = client.run(
                agent=starting_agent,
                messages=[{"role": "user", "content": user_input}],
            )

            # Update and display conversation history
            st.session_state["history"].append({"user": user_input, "agent": response.messages[-1]["content"]})
            user_input = ""  # Clear the input field

    # Step 8: Display conversation history
    st.subheader("Conversation History")
    for exchange in st.session_state["history"]:
        st.write(f"**You**: {exchange['user']}")
        st.write(f"**{selected_agent}**: {exchange['agent']}")

    # Step 9: Conversation Reset Button
    if st.button("Reset Conversation"):
        st.session_state["history"] = []
        st.write("Conversation history cleared.")
else:
    st.warning("Please enter your OpenAI API key to proceed.")
