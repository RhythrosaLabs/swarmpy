import streamlit as st
from swarm import Swarm, Agent

# Title for the app
st.title("Swarm Multi-Agent Chat Interface")

# Input field for the OpenAI API Key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# Proceed only if an API key is entered
if api_key:
    # Set the API key dynamically
    import os
    os.environ['OPENAI_API_KEY'] = api_key

    # Define a function for handoff
    def handoff_to_agent_b():
        return agent_b

    # Initialize agents
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

    # Input area for the user's message
    user_input = st.text_input("Enter your message:")

    # Button to submit the message
    if st.button("Send"):
        if user_input:
            # Run the conversation starting with Agent A
            response = client.run(
                agent=agent_a,
                messages=[{"role": "user", "content": user_input}],
            )
            
            # Display response from the agent
            st.write(f"Agent B says: {response.messages[-1]['content']}")
        else:
            st.write("Please enter a message to start the conversation.")
else:
    st.warning("Please enter your OpenAI API key to proceed.")
