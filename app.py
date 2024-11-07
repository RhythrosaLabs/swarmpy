import streamlit as st
from swarm import Swarm, Agent
import os

# Set up session state for agents and conversation history
if "agents" not in st.session_state:
    st.session_state["agents"] = {}
if "history" not in st.session_state:
    st.session_state["history"] = []
if "custom_functions" not in st.session_state:
    st.session_state["custom_functions"] = {}

# Title for the app
st.title("Advanced Swarm Multi-Agent Interface with File & Function Control")

# Step 1: API Key Input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key

    # Step 2: Agent Management
    with st.sidebar:
        st.header("Manage Agents")
        
        # Add a new agent
        agent_name = st.text_input("New Agent Name")
        agent_instructions = st.text_area("New Agent Instructions", "Provide specific instructions for the agent.")
        if st.button("Add Agent"):
            if agent_name and agent_name not in st.session_state["agents"]:
                # Create an Agent instance and store it in the session state
                st.session_state["agents"][agent_name] = Agent(name=agent_name, instructions=agent_instructions)
                st.write(f"Agent '{agent_name}' added.")
            else:
                st.warning("Agent name must be unique and not empty.")

        # Select an agent to edit or delete
        if st.session_state["agents"]:
            selected_agent = st.selectbox("Select Agent to Edit", list(st.session_state["agents"].keys()))
            if selected_agent:
                st.write(f"Editing {selected_agent}")
                agent_instance = st.session_state["agents"][selected_agent]
                
                # Display the current instructions and allow updates
                new_instructions = st.text_area("Update Instructions", agent_instance.instructions)
                if st.button("Update Instructions"):
                    st.session_state["agents"][selected_agent] = Agent(name=selected_agent, instructions=new_instructions)
                    st.write(f"Instructions for {selected_agent} updated.")
                
                if st.button("Delete Agent"):
                    del st.session_state["agents"][selected_agent]
                    st.write(f"Agent '{selected_agent}' deleted.")
        else:
            st.write("No agents available. Please add a new agent.")

    # Step 3: Define Custom Functions
    with st.sidebar:
        st.header("Define Custom Functions")
        function_name = st.text_input("Function Name")
        function_code = st.text_area("Function Code", "def custom_function():\n    return 'Your code here'")
        
        if st.button("Add Function"):
            try:
                exec(function_code, globals())
                st.session_state["custom_functions"][function_name] = eval(function_name)
                st.write(f"Function '{function_name}' added.")
            except Exception as e:
                st.error(f"Error in function definition: {e}")

    # Step 4: File Management
    st.subheader("File Management")
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "json"])
    if uploaded_file:
        content = uploaded_file.read()
        st.write("Uploaded File Content:", content.decode("utf-8"))
        st.session_state["history"].append({"role": "file", "content": content.decode("utf-8")})

    # Button to create a new file from conversation history
    if st.button("Save Conversation History to File"):
        with open("conversation_history.txt", "w") as file:
            for msg in st.session_state["history"]:
                if "role" in msg and "content" in msg:  # Check if keys exist
                    file.write(f"{msg['role']}: {msg['content']}\n")
        st.write("Conversation history saved to 'conversation_history.txt'.")

    # Step 5: Conversation Interaction
    st.subheader("Interact with Agents")
    conversation_input = st.text_input("Enter your message:")
    if st.button("Send Message"):
        if conversation_input and selected_agent:
            # Validate input message structure
            messages = [{"role": "user", "content": conversation_input}]
            if all(isinstance(msg.get("role"), str) and isinstance(msg.get("content"), str) for msg in messages):
                # Retrieve the Agent instance
                agent_instance = st.session_state["agents"][selected_agent]
                client = Swarm()
                try:
                    response = client.run(agent=agent_instance, messages=messages)
                    # Log response to check structure
                    st.write("API Response:", response)

                    # Update conversation history with valid response
                    st.session_state["history"].append({"role": "user", "content": conversation_input})
                    st.session_state["history"].append({"role": agent_instance.name, "content": response.messages[-1]["content"]})
                    st.write(f"{agent_instance.name} says: {response.messages[-1]['content']}")
                except Exception as e:
                    st.error(f"An error occurred during the API request: {e}")
            else:
                st.error("Invalid message format. Messages must have 'role' and 'content' keys with string values.")

    # Display conversation history
    st.subheader("Conversation History")
    for entry in st.session_state["history"]:
        if "role" in entry and "content" in entry:  # Ensure each entry has required keys
            st.write(f"{entry['role']}: {entry['content']}")
        else:
            st.write("Invalid entry format detected in history.")

    # Button to clear conversation history
    if st.button("Clear History"):
        st.session_state["history"] = []
        st.write("Conversation history cleared.")
