import streamlit as st
from swarm import Swarm, Agent
import os

# Set up session state for agents, conversation history, and back-and-forth control
if "agents" not in st.session_state:
    st.session_state["agents"] = {}
if "history" not in st.session_state:
    st.session_state["history"] = []
if "custom_functions" not in st.session_state:
    st.session_state["custom_functions"] = {}

# Title for the app
st.title("Automated Swarm Multi-Agent Interaction Interface")

# Step 1: API Key Input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key

    # Step 2: Define Agent Handoff
    def automated_handoff(agent_a, agent_b, user_input, max_cycles=5):
        """
        Automates conversation back-and-forth between two agents.
        
        Parameters:
        - agent_a: First agent to start the conversation.
        - agent_b: Second agent to receive handoff.
        - user_input: Initial input from the user.
        - max_cycles: Maximum number of back-and-forth exchanges.
        """
        client = Swarm()
        current_agent = agent_a
        conversation = [{"role": "user", "content": user_input}]
        
        for i in range(max_cycles):
            # Run the conversation with the current agent
            response = client.run(agent=current_agent, messages=conversation)
            response_content = response.messages[-1]["content"]
            
            # Log response in session history
            st.session_state["history"].append({"role": current_agent.name, "content": response_content})
            
            # Display the response in Streamlit
            st.write(f"**{current_agent.name} says:** {response_content}")
            
            # Prepare next agent and update conversation
            conversation.append({"role": current_agent.name, "content": response_content})
            current_agent = agent_b if current_agent == agent_a else agent_a
            
            # Optionally break out if a condition is met (e.g., keyword or end token)
            if "goodbye" in response_content.lower():
                st.write("Ending conversation based on 'goodbye' keyword.")
                break

    # Step 3: Agent Management in Sidebar
    with st.sidebar:
        st.header("Manage Agents")
        
        # Add new agents or update instructions
        agent_name = st.text_input("New Agent Name")
        agent_instructions = st.text_area("New Agent Instructions", "Provide specific instructions for the agent.")
        if st.button("Add Agent"):
            if agent_name and agent_name not in st.session_state["agents"]:
                st.session_state["agents"][agent_name] = Agent(name=agent_name, instructions=agent_instructions)
                st.write(f"Agent '{agent_name}' added.")
            else:
                st.warning("Agent name must be unique and not empty.")

        # Select two agents for back-and-forth interaction
        agent_a_name = st.selectbox("Select Agent A", list(st.session_state["agents"].keys()))
        agent_b_name = st.selectbox("Select Agent B", list(st.session_state["agents"].keys()))

    # Step 4: Conversation Control
    st.subheader("Automated Conversation Control")
    user_input = st.text_input("Enter your initial message to start the conversation:")
    max_cycles = st.slider("Set Maximum Cycles", min_value=1, max_value=20, value=5)

    if st.button("Start Automated Interaction") and agent_a_name and agent_b_name:
        agent_a = st.session_state["agents"][agent_a_name]
        agent_b = st.session_state["agents"][agent_b_name]
        
        # Start automated conversation between the selected agents
        st.write("**Starting automated interaction...**")
        st.session_state["history"].append({"role": "user", "content": user_input})
        automated_handoff(agent_a, agent_b, user_input, max_cycles=max_cycles)

    # Step 5: Display conversation history
    st.subheader("Conversation History")
    for entry in st.session_state["history"]:
        st.write(f"{entry['role']}: {entry['content']}")

    # Clear conversation history button
    if st.button("Clear History"):
        st.session_state["history"] = []
        st.write("Conversation history cleared.")
else:
    st.warning("Please enter your OpenAI API key to proceed.")
