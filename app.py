import streamlit as st
from swarm import Swarm, Agent
import os

# Initialize session state
if "agents" not in st.session_state:
    st.session_state["agents"] = {}
if "history" not in st.session_state:
    st.session_state["history"] = []

# Application title
st.title("Swarm Multi-Agent Interface")

# API Key Input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key

    # Agent Management
    with st.sidebar:
        st.header("Manage Agents")
        
        # Add a new agent
        agent_name = st.text_input("New Agent Name")
        agent_instructions = st.text_area("New Agent Instructions", "Provide specific instructions for the agent.")
        if st.button("Add Agent"):
            if agent_name and agent_name not in st.session_state["agents"]:
                st.session_state["agents"][agent_name] = Agent(name=agent_name, instructions=agent_instructions)
                st.success(f"Agent '{agent_name}' added.")
            else:
                st.warning("Agent name must be unique and not empty.")

        # Select an agent to edit or delete
        if st.session_state["agents"]:
            selected_agent = st.selectbox("Select Agent to Edit", list(st.session_state["agents"].keys()))
            if selected_agent:
                agent = st.session_state["agents"][selected_agent]
                new_instructions = st.text_area("Update Instructions", agent.instructions)
                if st.button("Update Instructions"):
                    agent.instructions = new_instructions
                    st.success(f"Instructions for '{selected_agent}' updated.")
                if st.button("Delete Agent"):
                    del st.session_state["agents"][selected_agent]
                    st.success(f"Agent '{selected_agent}' deleted.")
        else:
            st.info("No agents available. Please add a new agent.")

    # Conversation Interaction
    st.subheader("Interact with Agents")
    if st.session_state["agents"]:
        selected_agent = st.selectbox("Select Agent to Interact With", list(st.session_state["agents"].keys()))
        user_input = st.text_input("Enter your message:")
        if st.button("Send Message"):
            if user_input and selected_agent:
                agent = st.session_state["agents"][selected_agent]
                client = Swarm()
                try:
                    response = client.run(agent=agent, messages=[{"role": "user", "content": user_input}])
                    st.session_state["history"].append({"role": "user", "content": user_input})
                    st.session_state["history"].append({"role": agent.name, "content": response.messages[-1]["content"]})
                    st.write(f"{agent.name}: {response.messages[-1]['content']}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.info("No agents available. Please add a new agent.")

    # Display conversation history
    st.subheader("Conversation History")
    for entry in st.session_state["history"]:
        st.write(f"{entry['role']}: {entry['content']}")

    # Clear conversation history
    if st.button("Clear History"):
        st.session_state["history"] = []
        st.success("Conversation history cleared.")
