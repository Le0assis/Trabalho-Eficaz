import streamlit as st
import gemini
import random
import time


# Streamed response emulator
def response_generator(prompt):
    response = gemini.generate(prompt)  # Chama a gemini

    if hasattr(response, "text"):  # Verifica se a resposta tem o atributo "text"
        response_text = response.text
    else:
        response_text = str(response)  # Converte para string caso necessário

    for word in response_text.split():  # Agora não dá erro!
        yield word + " "  # Retorna palavra por palavra
        time.sleep(0.05)  # Simula



st.title("Leonardo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Escreva aqui..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})