import requests
import streamlit as st

st.title("My Fine-Tuned AI Chatbot 🤖")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Retrieve your Hugging Face token safely from Streamlit secrets
                HF_API_TOKEN = st.secrets["HF_API_TOKEN"]
                
                # Replace with your actual Hugging Face model repository ID
                MODEL_URL = "https://api-inference.huggingface.co/models/DEVELOPERDARSHAN/electroq-16bit"
                
                headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
                payload = {
                    "inputs": prompt,
                    "parameters": {"max_new_tokens": 200}
                }
                
                response = requests.post(MODEL_URL, headers=headers, json=payload)
                result = response.json()
                
                # Parse the model's text output
                if isinstance(result, list) and len(result) > 0:
                    bot_reply = result[0].get("generated_text", "Sorry, I couldn't generate a response.")
                else:
                    bot_reply = result.get("error", "Error communicating with the model API. Make sure your model is finished loading.")
                
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
