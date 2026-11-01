from huggingface_hub import InferenceClient
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
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Generate assistant response
  with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
      try:
        # Initialize Hugging Face client securely using Streamlit secrets
        client = InferenceClient(api_key=st.secrets["HF_API_TOKEN"])

        # Call your fine-tuned model via the official client
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-1.5B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )

        bot_reply = completion.choices[0].message.content

        st.markdown(bot_reply)
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )

      except Exception as e:
        st.error(f"An error occurred: {e}")
          
