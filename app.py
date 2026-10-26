import streamlit as st
from generate_answer import generate_rag_answer

# Browser tab settings
st.set_page_config(
    page_title="Enterprise IT Policy Assistant", page_icon="🛡️", layout="centered")

# Title and instructions
st.title("🛡️ Enterprise IT Policy Assistant")
st.markdown("Ask any internal IT policy question below. Responses are grounded in official documentation and backed by transparent source citations.")

# Creates a list called 'messages' if it doesn't yet exist, which keeps all chat history while the browser window is open. Otherwise, this code is ignored.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous prior chat history (role name and query/response) between the user and Gemini when the app reruns
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If Gemini's response contained sources (the user's query won't have this), render the collapsible expander
        if "sources" in message and message["sources"]:
            with st.expander("🔍 View Retrieved Source Excerpts"):
                for i, source in enumerate(message["sources"], 1): # Assigns an id number to each source chunk and puts each source chunk into 'source'
                    st.markdown(f"**Source {i}:**\n{source}") # Displays the list of ids and source chunks, separated by line breaks
                    if i < len(message["sources"]):
                        st.markdown("---") # Draw a divider of 3 dashes if the source number is less than the total number of sources, so that it is formatted neatly

# 'st.chat_input' renders a chat box for the user to type in their query. ':=' assigns the query text to 'query' and also checks to see if text was actually entered at the same time' 
if query := st.chat_input("Ask about IT policies (e.g., password reset, MFA)..."):
    
    # Add a new dictionary item to the 'messages' list for the user's query. Display a chat bubble on screen and populate it with the user's query
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate and display Gemini's response
    with st.chat_message("assistant"):
        with st.spinner("Searching policies and generating grounded answer..."):
            try:
                answer, sources = generate_rag_answer(query)
                st.markdown(answer)
                
                # Display sources in a collapsible dropdown
                with st.expander("🔍 View Retrieved Source Excerpts"):
                    for i, source in enumerate(sources, 1):
                        st.markdown(f"**Source {i}:**\n{source}")
                        if i < len(sources):
                            st.markdown("---")
                            
                # Save Gemini's response and sources to the history (the 'messages' list) so that it can be displayed again after the next query
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": sources
                })
                
            except Exception as e:
                error_msg = f"An error occurred while generating the answer: {e}"
                st.error(error_msg)