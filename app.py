import streamlit as st
from swarm import Swarm, Agent
import os
import openai

# Preset agents with instructions
preset_agents = {
    "Friendly Assistant": "You are a friendly assistant, always eager to help with a positive tone.",
    "Knowledgeable Expert": "You are a knowledgeable expert on various subjects and answer in a concise, informative manner.",
    "Casual Conversationalist": "Engage in casual, friendly conversation, responding as though chatting with a friend.",
    "Haiku Poet": "Only respond in haikus, following a 5-7-5 syllable structure."
}

# Initialize session states for agents and conversation history
if "agents" not in st.session_state:
    st.session_state["agents"] = {}
if "history" not in st.session_state:
    st.session_state["history"] = []

# Title for the app
st.title("Sleek Swarm Multi-Agent Interaction Interface")

# Step 1: API Key Input
api_key = st.text_input("🔑 Enter your OpenAI API Key:", type="password")
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key

    # Step 2: Define Agent Handoff Function
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
            try:
                # Display conversation being sent for debugging
                st.write(f"Sending to API: {conversation}")

                # Run the conversation with the current agent
                response = client.run(agent=current_agent, messages=conversation)
                response_content = response.messages[-1]["content"]

                # Log response in session history
                st.session_state["history"].append({"role": current_agent.name, "content": response_content})
                st.write(f"**{current_agent.name} says:** {response_content}")

                # Prepare next agent and update conversation
                conversation.append({"role": current_agent.name, "content": response_content})
                current_agent = agent_b if current_agent == agent_a else agent_a

                # Check for a termination condition
                if "goodbye" in response_content.lower():
                    st.write("Ending conversation based on 'goodbye' keyword.")
                    break

            except openai.error.InvalidRequestError as e:
                st.error(f"Error with the OpenAI API request: {e}")
                break
            except openai.error.OpenAIError as e:
                st.error(f"An error occurred with the OpenAI API: {e}")
                break

    # Step 3: Agent Management in Sidebar
    with st.sidebar:
        st.header("🤖 Agent Management")

        # Preset selection dropdown for Agent A and Agent B
        agent_a_preset = st.selectbox("Select Preset for Agent A", list(preset_agents.keys()))
        agent_b_preset = st.selectbox("Select Preset for Agent B", list(preset_agents.keys()))

        # Button to add agents based on presets
        if st.button("Add Preset Agents"):
            agent_a_name = "Agent A"
            agent_b_name = "Agent B"

            # Add preset agents if not already added
            if agent_a_name not in st.session_state["agents"]:
                st.session_state["agents"][agent_a_name] = Agent(name=agent_a_name, instructions=preset_agents[agent_a_preset])
            if agent_b_name not in st.session_state["agents"]:
                st.session_state["agents"][agent_b_name] = Agent(name=agent_b_name, instructions=preset_agents[agent_b_preset])
            st.write(f"Agents '{agent_a_name}' and '{agent_b_name}' added with presets.")

        # Display current agents and allow viewing instructions
        st.subheader("Current Agents")
        for agent_name, agent in st.session_state["agents"].items():
            st.write(f"**{agent_name}**: {agent.instructions}")

    # Step 4: Conversation Control
    st.subheader("Automated Conversation Control")
    user_input = st.text_input("💬 Enter your initial message to start the conversation:")
    max_cycles = st.slider("🔄 Set Maximum Cycles", min_value=1, max_value=20, value=5)

    if st.button("Start Automated Interaction") and "Agent A" in st.session_state["agents"] and "Agent B" in st.session_state["agents"]:
        agent_a = st.session_state["agents"]["Agent A"]
        agent_b = st.session_state["agents"]["Agent B"]

        # Start automated conversation between the selected agents
        st.write("**Starting automated interaction...**")
        st.session_state["history"].append({"role": "user", "content": user_input})
        automated_handoff(agent_a, agent_b, user_input, max_cycles=max_cycles)

    # Step 5: Display conversation history
    st.subheader("📝 Conversation History")
    for entry in st.session_state["history"]:
        st.write(f"{entry['role']}: {entry['content']}")

    # Clear conversation history button
    if st.button("🧹 Clear History"):
        st.session_state["history"] = []
        st.write("Conversation history cleared.")
else:
    st.warning("Please enter your OpenAI API key to proceed.")
