import streamlit as st
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

st.title("🤖 Electroq Chatbot")
st.markdown("Running live on Streamlit Cloud with a GGUF model from Hugging Face.")

# 1. Automatically download the GGUF file from your Hugging Face repository cache
@st.cache_resource
def get_model():
    model_path = hf_hub_download(
        repo_id="DEVELOPERDARSHAN/electroq-4bit", 
        filename="electroq-Q4_K_M.gguf"
    )
    # Load the downloaded model into llama-cpp
    return Llama(model_path=model_path, n_ctx=2048, verbose=False)

with st.spinner("Downloading and loading model into memory... (This happens only once)"):
    llm = get_model()

# 2. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Render chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle user input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.create_chat_completion(
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            reply = response["choices"][0]["message"]["content"]
            st.markdown(reply)
            
    st.session_state.messages.append({"role": "assistant", "content": reply})
    
              
          
