from huggingface_hub import InferenceClient
import streamlit as st

st.title("My AI Chatbot 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = InferenceClient(api_key=st.secrets["HF_API_TOKEN"])

                # Using a fully provider-backed serverless model
                completion = client.chat.completions.create(
                    model="meta-llama/Llama-3.1-8B-Instruct",
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
              
          
