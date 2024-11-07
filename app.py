import streamlit as st
from swarm import Swarm, Agent
import os

# Set up session state for agents and conversation history
if "agents" not in st.session_state:
    st.session_state["agents"] = {}
if "history" not in st.session_state:
    st.session_state["history"] = []

# Title for the app
st.title("Collaborative Swarm Multi-Agent Interface")

# Step 1: API Key Input
api_key = st.text_input("🔑 Enter your OpenAI API Key:", type="password")
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key

    # Step 2: Agent Management
    with st.sidebar:
        st.header("Agent Management")

        # Add a new agent
        agent_name = st.text_input("New Agent Name")
        agent_instructions = st.text_area("New Agent Instructions", "Provide specific instructions for this agent.")
        if st.button("Add Agent"):
            if agent_name and agent_name not in st.session_state["agents"]:
                # Store agent as an Agent instance in session state
                st.session_state["agents"][agent_name] = Agent(name=agent_name, instructions=agent_instructions)
                st.success(f"Agent '{agent_name}' added.")
            else:
                st.warning("Agent name must be unique and not empty.")

        # Edit existing agent
        if st.session_state["agents"]:
            selected_agent = st.selectbox("Select Agent to Edit", list(st.session_state["agents"].keys()))
            if selected_agent:
                agent = st.session_state["agents"][selected_agent]
                new_instructions = st.text_area("Update Instructions", agent.instructions)
                if st.button("Update Instructions"):
                    # Update the agent in session state with new instructions
                    st.session_state["agents"][selected_agent] = Agent(name=selected_agent, instructions=new_instructions)
                    st.success(f"Instructions for '{selected_agent}' updated.")
                if st.button("Delete Agent"):
                    del st.session_state["agents"][selected_agent]
                    st.success(f"Agent '{selected_agent}' deleted.")
        else:
            st.info("No agents available. Please add a new agent.")

    # Step 3: Collaborative Interaction Setup
    st.subheader("Collaborative Interaction")
    if len(st.session_state["agents"]) >= 2:
        # Select two agents for interaction
        agent_a_name = st.selectbox("Select Agent A", list(st.session_state["agents"].keys()))
        agent_b_name = st.selectbox("Select Agent B", [name for name in st.session_state["agents"].keys() if name != agent_a_name])
        
        # Settings for back-and-forth interaction
        user_input = st.text_input("💬 Initial User Message:")
        max_turns = st.slider("🔄 Number of Turns", min_value=1, max_value=10, value=5)
        
        # Start interaction
        if st.button("Start Collaborative Interaction"):
            agent_a = st.session_state["agents"][agent_a_name]
            agent_b = st.session_state["agents"][agent_b_name]
            client = Swarm()
            st.session_state["history"] = []  # Reset history for new conversation
            
            # Initialize conversation with user input
            conversation = [{"role": "user", "content": user_input}]
            current_agent = agent_a

            # Function to convert Agent instance to dictionary
            def agent_to_dict(agent_instance):
                return {"name": agent_instance.name, "instructions": agent_instance.instructions}

            # Perform turn-based interaction between the two agents
            for turn in range(max_turns):
                try:
                    # Convert the Agent instance to a dictionary only for this API call
                    agent_data = agent_to_dict(current_agent)
                    response = client.run(agent=agent_data, messages=conversation)
                    response_content = response.messages[-1]["content"]
                    
                    # Update and display conversation history
                    st.session_state["history"].append({"role": current_agent.name, "content": response_content})
                    conversation.append({"role": current_agent.name, "content": response_content})
                    
                    # Toggle between agents
                    current_agent = agent_b if current_agent == agent_a else agent_a
                    
                except Exception as e:
                    st.error(f"Error during API call: {e}")
                    break

    # Step 4: Display conversation history in chat format
    st.subheader("Conversation History")
    for entry in st.session_state["history"]:
        if entry["role"] == "user":
            st.markdown(f"<div style='text-align: right; background-color: #d1e7dd; padding: 10px; border-radius: 10px; margin: 5px;'>"
                        f"<strong>You:</strong> {entry['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; background-color: #f8d7da; padding: 10px; border-radius: 10px; margin: 5px;'>"
                        f"<strong>{entry['role']}:</strong> {entry['content']}</div>", unsafe_allow_html=True)

    # Clear conversation history
    if st.button("Clear History"):
        st.session_state["history"] = []
        st.success("Conversation history cleared.")
