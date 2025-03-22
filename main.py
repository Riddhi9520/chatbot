import streamlit as st
import time
import backend

# Streamed response emulator (Move this to the top)
def response_generator(prompt):  # Function definition
    response = backend.GenerateResponse(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("My chat")  # Title of the chat page

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):  # Default input (input tab/bar)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Save chat to database
    backend.save_chat(prompt, response)  # Store chat in MySQL
