import streamlit as st
import google.generativeai as genai
if st.button("Back"):
    st.switch_page("pages/Utilities.py")
# Configure Gemini API
genai.configure(api_key="AIzaSyBpHPk6zpfN5uKRztE3SGQ4Df1N6vPJDlI")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def chatbot_interface():
    st.subheader("Chat with your Health Assistant")

    # Initialize chat state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for chat in st.session_state.chat_history:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")

    # User input
    user_input = st.text_input("Type your message", key="user_input")

    if st.button("Send"):
        if user_input.strip() != "":
            try:
                with st.spinner("Thinking..."):
                    response_area = st.empty()
                    bot_reply = ""
                    for chunk in model.generate_content(user_input, stream=True):
                        bot_reply += chunk.text
                        response_area.markdown(f"**Bot:** {bot_reply}")
            except Exception as e:
                bot_reply = f"Error: {e}"

            # Save chat to history
            st.session_state.chat_history.append({"user": user_input, "bot": bot_reply})
            st.rerun()
if __name__ == "__main__":
    chatbot_interface()