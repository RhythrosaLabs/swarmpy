import streamlit as st
from swarm import Swarm, Agent
import os
from datetime import datetime
from PIL import Image
from io import BytesIO

# Set up session state for agent configurations and conversation history
if "agent_configs" not in st.session_state:
    st.session_state["agent_configs"] = {}
if "history" not in st.session_state:
    st.session_state["history"] = []

# Title for the app with icons
st.title("🤖 Collaborative Multi-Agent Interface with DALL-E, Web Scraping, and Analysis")

# Step 1: API Key Input
st.subheader("🔐 Step 1: API Key Input")
api_key = st.text_input("Enter your OpenAI API Key:", type="password", help="Your API key is required to interact with the agents.")
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key

    # Sidebar for Agent Management
    with st.sidebar:
        st.header("👥 Agent Management")
        agent_name = st.text_input("Agent Name", help="Provide a unique name for the agent.")
        agent_instructions = st.text_area("Agent Instructions", "Provide specific instructions for this agent.", help="Describe the agent's purpose or behavior.")
        if st.button("➕ Add Agent", key="add_agent"):
            if agent_name and agent_name not in st.session_state["agent_configs"]:
                st.session_state["agent_configs"][agent_name] = {"name": agent_name, "instructions": agent_instructions}
                st.success(f"Agent '{agent_name}' added successfully!")
            else:
                st.warning("Agent name must be unique and not empty.")

    # Collaboration Setup
    st.subheader("🤝 Step 2: Collaboration Setup")
    if len(st.session_state["agent_configs"]) >= 2:
        agent_a_name = st.selectbox("Select Agent A", list(st.session_state["agent_configs"].keys()), key="agent_a")
        agent_b_name = st.selectbox("Select Agent B", [name for name in st.session_state["agent_configs"].keys() if name != agent_a_name], key="agent_b")
        max_turns = st.slider("🔄 Number of Turns", min_value=1, max_value=10, value=5)
        
        # Step 3: Initial Prompt for Conversation
        st.subheader("💬 Step 3: Initial Prompt")
        user_input = st.text_input("Enter Initial User Message:", help="Start the conversation by entering an initial message.")
        
        if st.button("🚀 Start Collaborative Interaction"):
            agent_a_config = st.session_state["agent_configs"][agent_a_name]
            agent_b_config = st.session_state["agent_configs"][agent_b_name]
            agent_a = Agent(name=agent_a_config["name"], instructions=agent_a_config["instructions"])
            agent_b = Agent(name=agent_b_config["name"], instructions=agent_b_config["instructions"])
            client = Swarm()
            st.session_state["history"] = []  # Reset history for new conversation
            
            # Initialize conversation with user input
            conversation = [{"role": "user", "content": user_input}]
            current_agent = agent_a

            # Perform turn-based interaction between the two agents
            for turn in range(max_turns):
                try:
                    # Run the Swarm client with the actual Agent instance
                    response = client.run(agent=current_agent, messages=conversation)
                    response_content = response.messages[-1]["content"]
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state["history"].append({"role": current_agent.name, "content": response_content, "time": timestamp})
                    conversation.append({"role": "assistant", "name": current_agent.name, "content": response_content})
                    current_agent = agent_b if current_agent == agent_a else agent_a
                except Exception as e:
                    st.error(f"Error during API call: {e}")
                    break

    # DALL-E 3 Content Creation Section
    st.subheader("🖼️ DALL-E 3 Content Creation")
    dalle_prompt = st.text_input("Enter a prompt for image generation:", help="Create images using DALL-E 3.")
    if st.button("Generate Image"):
        # Assuming DALL-E 3 API is available as a function called `generate_image(prompt)`
        image_bytes = generate_dalle_image(dalle_prompt)  # This function should return bytes of the image
        if image_bytes:
            image = Image.open(BytesIO(image_bytes))
            st.image(image, caption="Generated by DALL-E 3")

    # Web Scraping Section
    st.subheader("🌐 Web Scraping")
    url = st.text_input("Enter URL to scrape:", help="Provide a URL to scrape data from.")
    if st.button("Scrape URL"):
        scraped_data = scrape_url(url)  # This function should be implemented to return scraped data as text
        st.text_area("Scraped Data", value=scraped_data, height=300)

    # File and Image Analysis Section
    st.subheader("📂 File and Image Analysis")
    uploaded_file = st.file_uploader("Upload a file (PDF, image, CSV):")
    if uploaded_file:
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            pdf_text = analyze_pdf(uploaded_file)  # This function should extract text from the PDF
            st.text_area("Extracted Text from PDF", pdf_text, height=300)
        elif file_type.startswith("image/"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image")
            analysis_result = analyze_image(image)  # Analyze the image for content (e.g., OCR)
            st.text_area("Image Analysis Result", analysis_result)
        elif file_type == "text/csv":
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            st.write(df)
            st.text("Data analysis can be added here.")

    # Save and Clear Chat History
    st.subheader("📜 Conversation History")
    for entry in st.session_state["history"]:
        if entry["role"] == "user":
            st.markdown(
                f"<div style='text-align: right; background-color: #1c1c1c; padding: 10px; border-radius: 10px; margin: 5px;'>"
                f"<strong>You:</strong> {entry['content']} <span style='font-size: small; color: #6c757d;'>({entry['time']})</span></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='text-align: left; background-color: #1c1c1c; padding: 10px; border-radius: 10px; margin: 5px;'>"
                f"<strong>{entry['role']}:</strong> {entry['content']} <span style='font-size: small; color: #6c757d;'>({entry['time']})</span></div>",
                unsafe_allow_html=True
            )
    if st.button("💾 Save Chat"):
        if st.session_state["history"]:
            history_text = "\n".join(
                [f"[{entry['time']}] {entry['role']}: {entry['content']}" for entry in st.session_state["history"]]
            )
            with open("/mnt/data/conversation_history.txt", "w") as f:
                f.write(history_text)
            st.success("Chat history saved successfully. You can download it below.")
            st.download_button("📥 Download Chat History", data=history_text, file_name="conversation_history.txt", mime="text/plain")
        else:
            st.warning("No chat history to save.")
    if st.button("🗑️ Clear History"):
        st.session_state["history"] = []
        st.info("Conversation history cleared.")
