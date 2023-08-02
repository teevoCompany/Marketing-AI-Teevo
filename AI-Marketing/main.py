import streamlit as st
import openai
import secret_key
import time
from PIL import Image

# Dummy user data
users = {"admin": "password"}

# OpenAI API
def communicate():
    try:
        messages = st.session_state["messages"]

        user_message = {"role": "user", "content": st.session_state["user_input"]}
        messages.append(user_message)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        bot_message = response["choices"][0]["message"]
        messages.append(bot_message)

        st.session_state["user_input"] = ""
    except Exception as e:
        st.write(f"Error: {e}")

def login():
    st.sidebar.markdown("## Login")
    st.sidebar.markdown("Please enter your credentials to login.")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')

    if st.sidebar.button("Login"):
        progress_text = "Operation in progress. Please wait."
        my_bar = st.sidebar.progress(0)
        st.sidebar.text(progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)  # Optional, you might want to adjust this
            my_bar.progress(percent_complete + 1)

        if username in users and users[username] == password:
            st.session_state["user"] = username
            st.success("Logged in successfully, Click the button again!")
        else:
            st.error("Incorrect username or password")

def main_app():
    openai.api_key = secret_key.openai_api_key
    system_prompt = "You are an excellent marketing and sales expert. Your task is to optimize the conversion of outreach for every business to busines transactions."

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": system_prompt}
            ]

    st.title("Assistant AI Bot")
    st.image("image.jpg")
    st.write("🤖 Hello! Feel free to ask me anything.")
    st.sidebar.markdown("## AUTOMATION MARKETING & OUTREACH")
    st.sidebar.markdown("AI excellent marketing and sales expert. expert on optimize the conversion of marketing outreach and sales.")

    st.markdown("**Instructions:**")
    st.markdown("1. Type your message in the text input field below.")
    st.markdown("2. Your message will be processed and an appropriate response will be displayed.")
    st.markdown("3. You can give feedback to optimized the desire response by told the AI your feedback.")
    user_input = st.text_input("Please write your message.", key="user_input", on_change=communicate)

    if st.session_state["messages"]:
        messages = st.session_state["messages"]

        for i in range(len(messages)-1, 0, -1):
            message = messages[i]
            speaker = "🙂" if message["role"] == "user" else "🤖"
            st.write(f"{speaker}: {message['content']}")

def run_app():
    st.sidebar.title("Assistant AI Bot")
    
    # Load and resize image
    img = Image.open("sidebar.jpg")
    img.thumbnail((300, 150))  # specify your desired width and height here
    
    st.sidebar.image(img)  # Display resized image
    if "user" in st.session_state:
        main_app()
    else:
        login()

if __name__ == "__main__":
    run_app()
