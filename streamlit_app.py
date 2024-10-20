import streamlit as st
import google.generativeai as genai
import json

# Show title and description.
st.title(" Chatbot")
st.write(
    "This is a simple chatbot that uses Google's GenerativeAI models to generate responses. "
    "To use this app, you need to provide a Google GenerativeAI API key, which you can get from [Google Cloud Platform](https://console.cloud.google.com/apis/credentials). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their Google GenerativeAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
genai_api_key = st.text_input("GenerativeAI API Key", type="password")
if not genai_api_key:
    st.info("Please add your GenerativeAI API key to continue.", icon="️🗝️")
else:

    # Configure the GenerativeAI client
    genai.configure(api_key=genai_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the GenerativeAI API.
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # Choose appropriate model name

        response = model.generate_content(prompt, stream=True)
        # Process the streamed response
        for chunk in response:
            if chunk:  # Check if the chunk is not empty
                if hasattr(chunk, 'text'):
                    text_value = chunk.text
                    with st.chat_message("assistant"):
                        response = st.write(text_value)
                    st.session_state.messages.append({"role": "assistant", "content": text_value})
        
        