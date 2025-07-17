import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import base64
from io import BytesIO

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Card styling */
    .tutorial-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .tutorial-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Text styling in cards */
    .tutorial-card h3 {
        color: #025246;
        font-size: 1.5em;
        margin-bottom: 15px;
    }
    
    .tutorial-card p {
        color: #333333;
        font-size: 1.1em;
        line-height: 1.6;
    }
    
    .tutorial-card ul {
        color: #333333;
        font-size: 1.1em;
        line-height: 1.8;
        padding-left: 20px;
    }
    
    .tutorial-card li {
        margin-bottom: 10px;
    }
    
    /* Header styling */
    .header {
        background: linear-gradient(135deg, #025246 0%, #013a32 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header h2 {
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #025246 0%, #013a32 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        transition: all 0.3s ease;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Image styling */
    .tutorial-image {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .tutorial-image:hover {
        transform: scale(1.02);
    }
    
    /* Progress bar styling */
    .progress-bar {
        height: 10px;
        background: linear-gradient(90deg, #025246 0%, #013a32 100%);
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Animation container */
    .animation-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .animation-container h3 {
        color: #025246;
        text-align: center;
        font-size: 1.5em;
    }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("""
<div class="header">
    <h2>🏋️‍♂️ Workout Tutorials</h2>
</div>
""", unsafe_allow_html=True)

# Load Lottie animations
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception as e:
        return None

# Load and display welcome animation
fitness_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_obhph3sh.json")
if fitness_animation:
    st_lottie(fitness_animation, height=200, key="welcome")

# Load animations
workout_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_2ks3pjua.json")

# Function to convert PIL Image to base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Load images
img1 = Image.open("models/images/dumbbell.webp")
img2 = Image.open("models/images/squats.jpg")
img3 = Image.open("models/images/pushups.jpeg")
img4 = Image.open("models/images/shoulder.jpeg")

# Convert images to base64
img1_base64 = image_to_base64(img1)
img2_base64 = image_to_base64(img2)
img3_base64 = image_to_base64(img3)
img4_base64 = image_to_base64(img4)

# Sidebar with enhanced styling
st.sidebar.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #025246 0%, #013a32 100%); border-radius: 10px;'>
    <h3 style='color: white;'>Choose Your Tutorial</h3>
</div>
""", unsafe_allow_html=True)

app_mode = st.sidebar.selectbox("", ["About", "Bicep Curls", "Squats", "Pushups", "Shoulder press"])

if app_mode == "About":
    st.markdown("""
    <div style='text-align: center; margin: 20px 0;'>
        <h2>Master Your Workout Form</h2>
        <p>Select a tutorial from the sidebar to learn proper exercise techniques</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tutorial cards with hover effects
    tutorials = [
        {
            "title": "Bicep Curls",
            "image_base64": img1_base64,
            "description": "Get armed with knowledge! Watch this bicep curl tutorial and unlock the secret to sleeve-busting strength!",
            "video_url": "https://youtu.be/ykJmrZ5v0Oo"
        },
        {
            "title": "Squats",
            "image_base64": img2_base64,
            "description": "Get lower, get stronger! Dive into this squat tutorial and unlock the power of a rock-solid foundation!",
            "video_url": "https://youtu.be/YaXPRqUwItQ"
        },
        {
            "title": "Pushups",
            "image_base64": img3_base64,
            "description": "Push your limits, pump up your power! Join us for this push-up tutorial and unleash your inner strength!",
            "video_url": "https://youtu.be/IODxDxX7oi4"
        },
        {
            "title": "Shoulder Press",
            "image_base64": img4_base64,
            "description": "Elevate your strength, shoulder to shoulder! Don't miss this shoulder press tutorial to reach new heights of power!",
            "video_url": "https://youtu.be/qEwKCR5JCog"
        }
    ]
    
    for tutorial in tutorials:
        st.markdown(f"""
        <div class="tutorial-card">
            <div style="display: flex; align-items: center; gap: 20px;">
                <div style="flex: 1;">
                    <img src="data:image/png;base64,{tutorial['image_base64']}" class="tutorial-image" style="width: 100%; max-width: 300px;">
                </div>
                <div style="flex: 2;">
                    <h3>{tutorial['title']}</h3>
                    <p>{tutorial['description']}</p>
                    <a href="{tutorial['video_url']}" target="_blank">
                        <button class="stButton">Watch Tutorial</button>
                    </a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif app_mode == "Bicep Curls":
    st.markdown("""
    <div class="header">
        <h2>💪 Bicep Curls Tutorial</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="tutorial-card">
            <h3>Step-by-Step Guide</h3>
            <div class="progress-bar"></div>
            <ul>
                <li>Stand up straight with a dumbbell in each hand</li>
                <li>Keep your elbows close to your torso</li>
                <li>Rotate palms forward</li>
                <li>Exhale and curl the weights</li>
                <li>Contract biceps fully</li>
                <li>Hold briefly at the top</li>
                <li>Inhale and lower slowly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.image("models/gif/bicep.gif", use_container_width=True)

elif app_mode == "Squats":
    st.markdown("""
    <div class="header">
        <h2>🦵 Squats Tutorial</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="tutorial-card">
            <h3>Step-by-Step Guide</h3>
            <div class="progress-bar"></div>
            <ul>
                <li>Stand with feet shoulder-width apart</li>
                <li>Engage your core</li>
                <li>Keep back straight</li>
                <li>Lower until thighs are parallel</li>
                <li>Push through heels to stand</li>
                <li>Keep chest up</li>
                <li>Breathe properly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.image("models/gif/squats.gif", use_container_width=True)

elif app_mode == "Pushups":
    st.markdown("""
    <div class="header">
        <h2>💪 Pushups Tutorial</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="tutorial-card">
            <h3>Step-by-Step Guide</h3>
            <div class="progress-bar"></div>
            <ul>
                <li>Start in high plank position</li>
                <li>Hands shoulder-width apart</li>
                <li>Lower body to floor</li>
                <li>Keep elbows close</li>
                <li>Push back up</li>
                <li>Maintain straight body</li>
                <li>Breathe steadily</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.image("models/gif/pushups.gif", use_container_width=True)

elif app_mode == "Shoulder press":
    st.markdown("""
    <div class="header">
        <h2>💪 Shoulder Press Tutorial</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="tutorial-card">
            <h3>Step-by-Step Guide</h3>
            <div class="progress-bar"></div>
            <ul>
                <li>Stand with feet shoulder-width apart</li>
                <li>Hold dumbbells at shoulders</li>
                <li>Press weights overhead</li>
                <li>Keep head and neck still</li>
                <li>Lower weights slowly</li>
                <li>Maintain control</li>
                <li>Breathe properly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.image("models/gif/shoulder.gif", use_container_width=True)

# Add a footer with animation
if workout_animation:
    st.markdown("""
    <div class="animation-container">
        <div style="text-align: center;">
            <h3>Keep pushing your limits! 💪</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st_lottie(workout_animation, height=100, key="footer")