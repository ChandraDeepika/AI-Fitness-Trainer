import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import pyrebase
import firebase_admin
from firebase_admin import credentials
import time
from requests.exceptions import ChunkedEncodingError
from http.client import IncompleteRead

# --- Firebase Admin Initialization ---
if not firebase_admin._apps:
    cred = credentials.Certificate("models/firebase_key.json")
    firebase_admin.initialize_app(cred)


# --- Firebase Client Config for Pyrebase ---
firebase_config = {
    "apiKey": "AIzaSyAuGMFFNwGxY_qGm9-JjmAXe4bwVDHtwmE",
    "authDomain": "ai-fitness-trainer-9ead5.firebaseapp.com",
    "databaseURL": "",
    "storageBucket": "ai-fitness-trainer-9ead5.appspot.com",
}

firebase = pyrebase.initialize_app(firebase_config)
auth_pyre = firebase.auth()

# --- Lottie Loader ---
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except (ChunkedEncodingError, IncompleteRead) as e:
        st.warning(f"Animation download interrupted. Using fallback. ({e})")
        return None
    except Exception as e:
        st.warning(f"Couldn't load animation from {url}. Using fallback. ({e})")
        return None

# --- Lottie Animations with Fallbacks ---
welcome_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_2ks3pjua.json")
fitness_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_obhph3sh.json")
workout_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_2ks3pjua.json")
music_animation = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ikk4jhps.json")
podcast_animation = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_JjpNLdaKYX.json")
particles_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_2ks3pjua.json")

# Function to safely display Lottie animations
def safe_lottie(animation, height, key):
    if animation:
        try:
            st_lottie(animation, height=height, key=key)
        except Exception as e:
            st.warning(f"Couldn't display animation {key}. Using fallback.")
            st.image("https://img.icons8.com/color/96/000000/fitness.png", width=height)
    else:
        st.image("https://img.icons8.com/color/96/000000/fitness.png", width=height)

# --- Load Lottie and Images ---
lottie_coding = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_FYx0Ph.json")
music = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ikk4jhps.json")
podcast = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_JjpNLdaKYX.json")
img_contact_form = Image.open("models/images/home.jpg")

# Add more Lottie animations
fitness_animation = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_obhph3sh.json")
welcome_animation = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_kkflmtur.json")
success_animation = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_obhph3sh.json")
workout_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_2ks3pjua.json")
music_animation = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_ikk4jhps.json")
podcast_animation = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_JjpNLdaKYX.json")
particles_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_2ks3pjua.json")

# --- Local CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("models/styles/styles.css")

# Enhanced CSS with more animations and effects
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            background: linear-gradient(-45deg, #1a1c2e, #3498db, #2d3748, #6dd5ed);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: white;
            padding: 2rem;
            min-height: 100vh;
            position: relative;
            overflow: hidden;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Floating icons */
        .floating-icon {
            position: absolute;
            animation: floating 3s ease-in-out infinite;
            opacity: 0.7;
            z-index: 0;
        }

        @keyframes floating {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(5deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }

        /* Section styling */
        .section {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
            animation: fadeInSection 1.2s;
            transition: transform 0.3s;
        }

        .section:hover {
            transform: translateY(-5px) scale(1.01);
        }

        /* Title styling */
        .section-title {
            color: #3498DB;
            font-size: 2rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 0;
            width: 50px;
            height: 3px;
            background: linear-gradient(90deg, #3498DB, #2980B9);
            border-radius: 3px;
        }

        /* Card styling */
        .card {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s;
        }

        .card:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-5px);
        }

        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
            color: white;
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: bold;
            border: none;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.2);
            background: linear-gradient(135deg, #2980B9 0%, #3498DB 100%);
        }

        /* Link styling */
        a {
            color: #3498DB;
            text-decoration: none;
            transition: all 0.3s;
        }

        a:hover {
            color: #2980B9;
            text-decoration: underline;
        }

        @keyframes fadeInSection {
            from { opacity: 0; transform: translateY(30px);}
            to { opacity: 1; transform: translateY(0);}
        }
    </style>
""", unsafe_allow_html=True)

# Add floating icons to the background
st.markdown("""
    <div class="floating-icons">
        <img src="https://img.icons8.com/color/48/000000/dumbbell.png" class="floating-icon" style="top: 10%; left: 5%;" />
        <img src="https://img.icons8.com/color/48/000000/yoga.png" class="floating-icon" style="top: 20%; right: 10%;" />
        <img src="https://img.icons8.com/color/48/000000/heart-with-pulse.png" class="floating-icon" style="bottom: 15%; left: 15%;" />
        <img src="https://img.icons8.com/color/48/000000/running.png" class="floating-icon" style="bottom: 25%; right: 20%;" />
        <img src="https://img.icons8.com/color/48/000000/boxing-glove.png" class="floating-icon" style="top: 40%; left: 40%;" />
        <img src="https://img.icons8.com/color/48/000000/meditation.png" class="floating-icon" style="bottom: 10%; right: 5%;" />
    </div>
""", unsafe_allow_html=True)

# --- Animated Particles Background (optional, subtle) ---
st_lottie(particles_animation, height=80, key="particles")

# --- Authentication UI ---
def show_auth_ui():
    # Welcome animation
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        safe_lottie(welcome_animation, height=200, key="welcome")

    st.markdown("""
        <div class="auth-container">
            <h1 class="auth-title">🏋️ AI Fitness Trainer Pro</h1>
            <p class="auth-subtitle">Your journey to a healthier lifestyle starts here</p>
        </div>
    """, unsafe_allow_html=True)

    # Fitness animation
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        safe_lottie(fitness_animation, height=150, key="fitness")

    auth_mode = st.radio("", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")

    with st.form("auth_form"):
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        submit = st.form_submit_button(f"{'Login' if auth_mode == 'Login' else 'Sign Up'}")

        if submit:
            if not email or not password:
                st.markdown("""
                    <div class="error-message">
                        Please enter both email and password.
                    </div>
                """, unsafe_allow_html=True)
                return

            try:
                if auth_mode == "Login":
                    user = auth_pyre.sign_in_with_email_and_password(email, password)
                    st.markdown(f"""
                        <div class="success-message">
                            Welcome back, {email}! 🎉
                        </div>
                    """, unsafe_allow_html=True)
                    # Success animation
                    safe_lottie(success_animation, height=150, key="success")
                else:
                    user = auth_pyre.create_user_with_email_and_password(email, password)
                    st.markdown(f"""
                        <div class="success-message">
                            Account created successfully! Welcome aboard, {email}! 🚀
                        </div>
                    """, unsafe_allow_html=True)
                    # Success animation
                    safe_lottie(success_animation, height=150, key="success")

                st.session_state["username"] = email
                time.sleep(1)  # Give user time to see the success message
                st.rerun()

            except Exception as e:
                err = e.args[1] if len(e.args) > 1 else str(e)
                st.markdown(f"""
                    <div class="error-message">
                        Authentication failed. {err}
                    </div>
                """, unsafe_allow_html=True)

# --- Show Auth UI if not logged in ---
if "username" not in st.session_state:
    show_auth_ui()
    st.stop()

# -------------------------------
# 🚀 Authenticated Section Starts
# -------------------------------
# ---- HEADER SECTION ----
with st.container():
    safe_lottie(welcome_animation, height=120, key="welcome")
    st.markdown(f"""
        <div class="section">
            <h1 class="section-title">Welcome, {st.session_state['username']}! 👋</h1>
            <p>Step into a fitter future: Welcome to your fitness revolution!</p>
        </div>
    """, unsafe_allow_html=True)

# ---- Animated Divider ----
st.markdown("""
    <div style="height: 8px; background: linear-gradient(90deg, #3498db, #6dd5ed); border-radius: 4px; margin: 32px 0;"></div>
""", unsafe_allow_html=True)

# ---- ABOUT US ----
with st.container():
    st.markdown("""
        <div class="section">
            <h2 class="section-title">About Us :point_down:</h2>
            <div class="card">
                <h3 style="color: #3498DB; margin-bottom: 1rem;">Your Journey to a Healthier You Starts Here</h3>
                <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem;">
                    At AI Fitness Trainer Pro, we believe that everyone deserves access to personalized fitness guidance. 
                    Our mission is to empower you to achieve your fitness goals through innovative technology and expert knowledge.
                </p>
                <div style="display: flex; gap: 1rem; margin: 1.5rem 0;">
                    <div style="flex: 1; padding: 1rem; background: rgba(52, 152, 219, 0.1); border-radius: 10px;">
                        <h4 style="color: #3498DB; margin-bottom: 0.5rem;">🎯 Personalized Approach</h4>
                        <p>Get customized workout plans and nutrition advice tailored to your specific goals and needs.</p>
                    </div>
                    <div style="flex: 1; padding: 1rem; background: rgba(52, 152, 219, 0.1); border-radius: 10px;">
                        <h4 style="color: #3498DB; margin-bottom: 0.5rem;">🏠 Home Comfort</h4>
                        <p>Transform your living space into your personal fitness studio with our home-based workout solutions.</p>
                    </div>
                </div>
                <div style="display: flex; gap: 1rem; margin: 1.5rem 0;">
                    <div style="flex: 1; padding: 1rem; background: rgba(52, 152, 219, 0.1); border-radius: 10px;">
                        <h4 style="color: #3498DB; margin-bottom: 0.5rem;">🤖 AI-Powered Guidance</h4>
                        <p>Experience the future of fitness with our advanced AI technology that adapts to your progress.</p>
                    </div>
                    <div style="flex: 1; padding: 1rem; background: rgba(52, 152, 219, 0.1); border-radius: 10px;">
                        <h4 style="color: #3498DB; margin-bottom: 0.5rem;">💪 Holistic Wellness</h4>
                        <p>Focus on both physical and mental well-being with our comprehensive fitness approach.</p>
                    </div>
                </div>
                <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 1.5rem; font-style: italic;">
                    "Join our community of fitness enthusiasts and start your journey to a healthier, stronger, and more confident you. 
                    Your transformation begins today!"
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    safe_lottie(workout_animation, height=200, key="workout")

# ---- Animated Divider ----
st.markdown("""
    <div style="height: 8px; background: linear-gradient(90deg, #6dd5ed, #3498db); border-radius: 4px; margin: 32px 0;"></div>
""", unsafe_allow_html=True)

# ---- MUSIC & PODCAST ----
with st.container():
    st.markdown("""
        <div class="section">
            <h2 class="section-title">Get fit, Jam on, Repeat 🎧</h2>
        </div>
    """, unsafe_allow_html=True)

    # Music Section
    col1, col2 = st.columns((1, 2))
    with col1:
        safe_lottie(music_animation, height=180, key="music")
    with col2:
        st.markdown("""
            <div class="card">
                <h3>Workout music</h3>
                <p>Power up your workout with the ultimate music fuel!</p>
                <a href="https://open.spotify.com/playlist/6N0Vl77EzPm13GIOlEkoJn" target="_blank">Listen on Spotify</a>
            </div>
        """, unsafe_allow_html=True)

    # Podcast Section
    col1, col2 = st.columns((1, 2))
    with col1:
        safe_lottie(podcast_animation, height=180, key="podcast")
    with col2:
        st.markdown("""
            <div class="card">
                <h3>Podcast</h3>
                <p>Pump up your workouts with our energizing podcast.</p>
                <a href="https://open.spotify.com/playlist/09Ig7KfohF5WmU9RhbDBjs" target="_blank">Listen on Spotify</a>
            </div>
        """, unsafe_allow_html=True)

# ---- Animated Divider ----
st.markdown("""
    <div style="height: 8px; background: linear-gradient(90deg, #3498db, #6dd5ed); border-radius: 4px; margin: 32px 0;"></div>
""", unsafe_allow_html=True)

# ---- CONTACT ----
with st.container():
    st.markdown("""
        <div class="section">
            <h2 class="section-title">Get In Touch With Me!</h2>
            <div class="card">
                <form action="https://formsubmit.co/YOUR_EMAIL@example.com" method="POST">
                    <input type="hidden" name="_captcha" value="false">
                    <input type="text" name="name" placeholder="Your name" required>
                    <input type="email" name="email" placeholder="Your email" required>
                    <textarea name="message" placeholder="Your message here" required></textarea>
                    <button type="submit">Send</button>
                </form>
            </div>
        </div>
    """, unsafe_allow_html=True)
