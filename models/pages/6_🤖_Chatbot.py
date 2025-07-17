import streamlit as st
import requests
import json
import toml
import time
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO

# Set up Streamlit page
st.set_page_config(
    page_title="💪🤖 Fit-Bot: Your Gym Assistant",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS for enhanced styling
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            background: linear-gradient(135deg, #1a1c2e 0%, #2d3748 100%);
            color: white;
            padding: 2rem;
            min-height: 100vh;
        }

        /* Title styling with animation */
        .title {
            text-align: center;
            color: #3498DB;
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            animation: fadeInDown 1s ease-out;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Subtitle styling */
        .subtitle {
            text-align: center;
            color: #ADBAC7;
            font-size: 1.4rem;
            margin-bottom: 2rem;
            animation: fadeInUp 1s ease-out;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Chatbox styling */
        .chatbox {
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-radius: 15px;
            background-color: rgba(32, 43, 58, 0.8);
            color: #ADBAC7;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            animation: slideIn 0.5s ease-out;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            position: relative;
            overflow: hidden;
        }

        .chatbox::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3498DB, #2ECC71);
        }

        /* User message styling */
        .user {
            color: #2ECC71;
            border-left: 4px solid #2ECC71;
            background: linear-gradient(90deg, rgba(46,204,113,0.1) 0%, rgba(32,43,58,0.8) 100%);
        }

        /* Bot message styling */
        .bot {
            color: #3498DB;
            border-left: 4px solid #3498DB;
            background: linear-gradient(90deg, rgba(52,152,219,0.1) 0%, rgba(32,43,58,0.8) 100%);
        }

        /* Input box styling */
        .stTextInput>div>div>input {
            color: black;
            background-color: rgba(255,255,255,0.9);
            border-radius: 20px;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid transparent;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .stTextInput>div>div>input:focus {
            border-color: #3498DB;
            box-shadow: 0 0 0 2px rgba(52,152,219,0.2);
        }

        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
            color: white;
            border-radius: 20px;
            padding: 12px 24px;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.2);
            background: linear-gradient(135deg, #2980B9 0%, #3498DB 100%);
        }

        .stButton>button::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            animation: shine 3s infinite;
        }

        /* Animations */
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        @keyframes shine {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
        }

        /* Feature icons styling */
        .feature-icon {
            font-size: 2.5rem;
            margin: 0.5rem;
            animation: bounce 2s infinite;
        }

        .feature-text {
            font-size: 1rem;
            color: #ADBAC7;
            margin-top: 0.5rem;
        }

        /* Message icons */
        .message-icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
            vertical-align: middle;
        }

        /* Progress bar styling */
        .stProgress > div > div > div {
            background-color: #3498DB;
        }

        /* Loading spinner styling */
        .stSpinner>div {
            border-color: #3498DB !important;
        }

        /* Success message styling */
        .success-message {
            background-color: rgba(46,204,113,0.1);
            border: 1px solid #2ECC71;
            color: #2ECC71;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            animation: fadeIn 0.5s ease-out;
        }

        /* Error message styling */
        .error-message {
            background-color: rgba(231,76,60,0.1);
            border: 1px solid #E74C3C;
            color: #E74C3C;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            animation: fadeIn 0.5s ease-out;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: #3498DB;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #2980B9;
        }
    </style>
""", unsafe_allow_html=True)

# Add a decorative header with animations and icons
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 3.5rem; color: #3498DB; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); animation: fadeInDown 1s ease-out;">
            <span style="font-size: 4rem;">💪</span> Fit-Bot
        </h1>
        <p style="font-size: 1.4rem; color: #ADBAC7; animation: fadeInUp 1s ease-out;">
            Your virtual gym buddy! Ask anything about workouts, routines, tips, or fitness goals.
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
            <div style="text-align: center;">
                <span class="feature-icon">🏋️‍♂️</span>
                <p class="feature-text">Workout Plans</p>
            </div>
            <div style="text-align: center;">
                <span class="feature-icon">🥗</span>
                <p class="feature-text">Nutrition</p>
            </div>
            <div style="text-align: center;">
                <span class="feature-icon">💡</span>
                <p class="feature-text">Fitness Tips</p>
            </div>
            <div style="text-align: center;">
                <span class="feature-icon">🔥</span>
                <p class="feature-text">Motivation</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Load Google API key securely from secrets file
try:
    with open("models/secrets.toml", "r") as f:
        config = toml.load(f)
        api_key = config["google"]["api_key"]
except Exception:
    st.error("❌ Could not load API key. Please check your `models/secrets.toml` file.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=api_key)

# List available models and select the appropriate one
try:
    # First try to use gemini-1.5-flash
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("✅ Successfully connected to gemini-1.5-flash")
    except:
        # If that fails, try to find any available model
        available_models = [m for m in genai.list_models() 
                          if 'generateContent' in m.supported_generation_methods 
                          and 'vision' not in m.name.lower()]  # Exclude vision models
        if not available_models:
            st.error("❌ No suitable models found. Please check your API key and internet connection.")
            st.stop()
        
        # Use the first available model that supports generateContent
        model = genai.GenerativeModel(available_models[0].name)
        st.success(f"✅ Successfully connected to {available_models[0].name}")
except Exception as e:
    st.error(f"❌ Error initializing Gemini model: {str(e)}")
    st.stop()

# Base prompt to define bot behavior
BASE_PROMPT = """You are Donnie, a professional fitness trainer and nutritionist with 10+ years of experience. \
Your expertise includes:\n- Personalized workout planning\n- Nutrition advice\n- Exercise form and technique\n- Fitness motivation and goal setting\n- Injury prevention\n- Recovery strategies\n\nGuidelines for your responses:\n1. Be professional yet friendly and encouraging\n2. Provide detailed, accurate, and actionable information\n3. Always give specific examples, lists, and practical tips when asked\n4. Never answer with only generalities; always include at least 5 concrete items for food or exercise questions\n5. Ask follow-up questions to better understand the user's needs\n6. Consider safety and proper form in all advice\n7. Stay focused on fitness and health-related topics\n8. If asked about non-fitness topics, politely redirect to fitness-related subjects\n\nAlways maintain a supportive and motivational tone while ensuring your advice is safe and appropriate for the user's level.\nIf the user asks for a list, always provide a numbered list of at least 5 specific items.\nAlways provide exact, Google-like answers with specific details and actionable advice.\n"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "last_input" not in st.session_state:
    st.session_state["last_input"] = ""

def display_message(role, content):
    """Display a message with enhanced visual effects"""
    # Clean the content of any HTML tags
    content = content.replace('</div>', '').replace('<div>', '')
    
    if role == "user":
        st.markdown(f"""
            <div class="chatbox user" style="animation: slideIn 0.5s ease-out;">
                <span class="message-icon">👤</span>
                <strong>You:</strong><br>
                {content}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chatbox bot" style="animation: slideIn 0.5s ease-out;">
                <span class="message-icon">🤖</span>
                <strong>Donnie:</strong><br>
                {content}
            </div>
        """, unsafe_allow_html=True)

# Create a container for the chat interface
chat_container = st.container()
with chat_container:
    # Display previous messages
    for message in st.session_state["messages"]:
        display_message(message["role"], message["content"])

def get_chat_response(prompt):
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                top_p=0.95,
                top_k=40,
                max_output_tokens=2048,
            )
        )
        if response.text:
            # Clean the response text of any HTML tags
            cleaned_text = response.text.replace('</div>', '').replace('<div>', '')
            return cleaned_text
        else:
            st.error("❌ No response generated. Please try again.")
            return None
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        return None

# Input from user
user_input = st.text_input("💬 Ask your question:", key="input_text")

# Generate chatbot reply
if user_input and user_input != st.session_state["last_input"]:
    st.session_state["last_input"] = user_input
    st.session_state["messages"].append({"role": "user", "content": user_input})
    display_message("user", user_input)

    # Add progress bar for visual feedback
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)

    try:
        with st.spinner("💭 Donnie is thinking..."):
            # Prepare the conversation history
            conversation = BASE_PROMPT + "\n\n"
            for msg in st.session_state["messages"]:
                if msg["role"] == "user":
                    conversation += f"User: {msg['content']}\n"
                else:
                    conversation += f"Assistant: {msg['content']}\n"
            
            # Get response from Gemini API
            reply = get_chat_response(conversation)
            
            if not reply:
                reply = "I apologize, but I'm having trouble generating a response right now. Please try again."
            
            st.session_state["messages"].append({"role": "assistant", "content": reply})
            display_message("assistant", reply)
            time.sleep(0.3)  # Reduced delay for better UX

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        error_message = "I apologize for the technical difficulty. Please try asking your question again, or rephrase it slightly differently."
        st.session_state["messages"].append({"role": "assistant", "content": error_message})
        display_message("assistant", error_message)

# Clear chat button
if st.button("🧹 Clear Conversation"):
    st.session_state["messages"] = []
    st.session_state["last_input"] = ""
    st.experimental_rerun()