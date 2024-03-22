# chatbot_app.py

# main.py (Streamlit app)
import streamlit as st
from chatbot import generate_output  # Import your chatbot function

def main():
    st.title("Chatbot Demo")
    user_query = st.text_input("Enter your question:")
    
    if st.button("Ask"):
        chatbot_response = generate_output(user_query)
        st.write("Chatbot:", chatbot_response)

if __name__ == "__main__":
    main()

#################################################
    #code below is for chat history

# import streamlit as st
# from chatbot import generate_output
# def main():
#     st.title("Chatbot App")
    
#     # Initialize chat history list
#     chat_history = st.session_state.get('chat_history', [])
    
#     # Sidebar for loading chat histories from previous sessions
#     st.sidebar.title("Chat History")
#     for i, chat in enumerate(chat_history, 1):
#         if st.sidebar.button(f"Session {i}"):
#             show_chat_history(chat)
    
#     # Main section for current session chat history
#     st.header("Current Session Chat History")
#     with st.container():
#         for chat in chat_history:
#             display_chat(chat)
    
#     # User input for the current session
#     st.write("Type your message below:")
#     user_query = st.text_input("Enter your question: ")
#     if user_query:
#         # Process user input (you can replace this with your chatbot logic)
#         response = generate_output(question=user_query)
        
#         # Append user and chatbot responses to chat history
#         chat_history.append({'user': user_query, 'chatbot': response})
        
#         # Display the conversation
#         display_chat({'user': user_query, 'chatbot': response})
        
#         # Save chat history in session state
#         st.session_state['chat_history'] = chat_history

# def display_chat(chat):
#     st.text(f"User: {chat['user']}")
#     st.text(f"Chatbot: {chat['chatbot']}")

# def show_chat_history(chat):
#     st.header("Chat History")
#     display_chat(chat)

# def generate_output(question):
#     # Implement your chatbot logic here
#     # For example, you can use a pre-trained model, or simple rule-based responses
#     # For demonstration, let's just echo the input for now
#     return "Echo: " + question

# if __name__ == "__main__":
#     main()
