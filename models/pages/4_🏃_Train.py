import cv2
import numpy as np
import mediapipe as mp
import streamlit as st
import tempfile
import time
from gtts import gTTS
import pygame
from typing import List
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from firebase_utils import save_session_to_firestore
import pandas as pd
import urllib.request


# ----------------- Exercise Configuration -----------------
EXERCISE_CONFIG = {
    "Left Dumbbell Curl": {
        "angle_points": [11, 13, 15],
        "down_angle": 160,
        "up_angle": 50,
        "direction": "up",
        "feedback_zones": [(160, 120, "Getting there"), (120, 50, "Good range")],
        "instruction": "Keep your elbow close to your body and only move your forearm."
    },
    "Right Dumbbell Curl": {
        "angle_points": [12, 14, 16],
        "down_angle": 160,
        "up_angle": 50,
        "direction": "up",
        "feedback_zones": [(160, 120, "Getting there"), (120, 50, "Good range")],
        "instruction": "Keep your elbow close to your body and only move your forearm."
    },
    "Squats": {
        "angle_points": [24, 26, 28],
        "down_angle": 170,
        "up_angle": 70,
        "direction": "down",
        "feedback_zones": [(170, 140, "Start descent"), (140, 70, "Good depth")],
        "instruction": "Keep your back straight and knees behind your toes."
    },
    "Pushups": {
        "angle_points": [11, 13, 15],
        "down_angle": 160,
        "up_angle": 80,
        "direction": "down",
        "feedback_zones": [(160, 120, "Lowering"), (120, 80, "Good depth")],
        "instruction": "Maintain a straight body line and go all the way down."
    },
    "Shoulder Press": {
        "angle_points": [11, 13, 15],
        "down_angle": 90,
        "up_angle": 170,
        "direction": "up",
        "feedback_zones": [(90, 120, "Start press"), (120, 170, "Full extension")],
        "instruction": "Press straight up until your arms are fully extended."
    }
}

EXERCISE_FEEDBACK = {
    "Left Dumbbell Curl": {
        "good": "Great job! You completed a perfect left dumbbell curl.",
        "start": "Start from a fully extended arm.",
        "range": "Try to curl all the way up for full range.",
        "form": "Keep your elbow close to your body."
    },
    "Right Dumbbell Curl": {
        "good": "Excellent! Right dumbbell curl completed.",
        "start": "Start from a fully extended arm.",
        "range": "Curl all the way up for best results.",
        "form": "Keep your elbow close to your body."
    },
    "Squats": {
        "good": "Nice squat! Great depth.",
        "start": "Stand up straight to start.",
        "range": "Go lower for a deeper squat.",
        "form": "Keep your back straight and knees behind your toes."
    },
    "Pushups": {
        "good": "Awesome pushup! Full range.",
        "start": "Start from the top plank position.",
        "range": "Lower your chest closer to the ground.",
        "form": "Keep your body straight."
    },
    "Shoulder Press": {
        "good": "Well done! Full shoulder press.",
        "start": "Start with arms down.",
        "range": "Press all the way up for full extension.",
        "form": "Press straight up and keep your core tight."
    }
}

pygame.mixer.init()

def get_exercise_image(exercise):
    # Only use reliable online images for each exercise
    online_images = {
        "Left Dumbbell Curl": "https://www.shutterstock.com/image-photo/muscular-sportswoman-doing-dumbbells-curls-600nw-2449204121.jpg",
        "Right Dumbbell Curl": "https://parade.com/.image/ar_1:1,c_fill,cs_srgb,fl_progressive,q_auto:good,w_1200/MTkxNjgzMTQ3NTY0MzI4NjEx/arm-toning-workouts-weights.jpg",
        "Squats": "https://physiolounge.co.uk/wp-content/uploads/2021/08/squat.jpg",
        "Pushups": "https://formatlive.com/wp-content/uploads/2021/08/0e7e9800cb65fd44_Tricep-Push-Up.jpg",
        "Shoulder Press": "https://cdn.mos.cms.futurecdn.net/LsqTqWvgpqXaCtdJoryCWn.jpg"
    }
    return online_images.get(exercise)

class ExerciseTracker:
    def __init__(self):
        self.cap = None
        self.pose = mp.solutions.pose.Pose(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            model_complexity=1
        )
        self.drawing = mp.solutions.drawing_utils
        self.drawing_styles = mp.solutions.drawing_styles
        self.last_audio_time = 0
        self.audio_cooldown = 2.5
        self.last_feedback = None
        self.last_stage = None
        self.last_message = None

    @staticmethod
    def calculate_angle(a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

    def play_audio(self, message: str, key: str):
        if time.time() - self.last_audio_time < self.audio_cooldown:
            return
        if self.last_message == message:
            return
        self.last_message = message
        # Use a unique filename for each playback
        unique_id = f"{key}_{int(time.time() * 1000)}"
        temp_path = os.path.join(tempfile.gettempdir(), f"{unique_id}.mp3")
        try:
            tts = gTTS(text=message, lang='en')
            tts.save(temp_path)
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            self.last_audio_time = time.time()
            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            # After playback, ensure the file is closed before deleting
            pygame.mixer.music.unload()
        except Exception as e:
            # Only show the error once per session
            if not hasattr(self, 'audio_error_shown'):
                st.warning(f"Audio playback failed: {str(e)}")
                self.audio_error_shown = True
        finally:
            # Try to delete the file, but ignore errors if it's still in use
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception:
                pass

    def get_landmark_coords(self, landmarks, landmark_idx, image_shape):
        if not landmarks or landmark_idx >= len(landmarks.landmark):
            return None
        height, width = image_shape[:2]
        landmark = landmarks.landmark[landmark_idx]
        return (int(landmark.x * width), int(landmark.y * height))

    def draw_feedback(self, image, angle, feedback_zones, direction):
        current_feedback = ""
        for max_angle, min_angle, feedback in feedback_zones:
            if direction == "up" and max_angle >= angle >= min_angle:
                cv2.putText(image, feedback, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                current_feedback = feedback
            elif direction == "down" and min_angle <= angle <= max_angle:
                cv2.putText(image, feedback, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                current_feedback = feedback
        return current_feedback

    def run_exercise(self, exercise_name: str, placeholder, username: str):
        config = EXERCISE_CONFIG[exercise_name]
        angle_points = config["angle_points"]
        down_angle = config["down_angle"]
        up_angle = config["up_angle"]
        direction = config["direction"]
        feedback_zones = config["feedback_zones"]

        stage = None
        correct_count = 0
        incorrect_count = 0
        rep_start_time = None
        rep_durations = []
        in_rep = False
        last_feedback = ""
        last_stage = None
        last_angle = None

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            st.error("Could not open webcam")
            return

        metrics_placeholder = st.empty()

        while self.cap.isOpened() and not st.session_state.get('stop_exercise', False):
            ret, frame = self.cap.read()
            if not ret:
                st.warning("Could not read from webcam")
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            landmarks = results.pose_landmarks

            if landmarks:
                a = [landmarks.landmark[angle_points[0]].x, landmarks.landmark[angle_points[0]].y]
                b = [landmarks.landmark[angle_points[1]].x, landmarks.landmark[angle_points[1]].y]
                c = [landmarks.landmark[angle_points[2]].x, landmarks.landmark[angle_points[2]].y]
                angle = self.calculate_angle(a, b, c)

                self.drawing.draw_landmarks(
                    image, landmarks, mp.solutions.pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.drawing_styles.get_default_pose_landmarks_style()
                )

                # Robust rep counting logic
                feedback_msgs = EXERCISE_FEEDBACK[exercise_name]
                if direction == "up":
                    if angle > down_angle:
                        if stage != "down":
                            stage = "down"
                            in_rep = True
                            rep_start_time = time.time()
                            self.play_audio(feedback_msgs["form"], f"form_{exercise_name}")
                    if angle < up_angle and stage == "down":
                        correct_count += 1
                        stage = "up"
                        if in_rep:
                            rep_durations.append(time.time() - rep_start_time)
                            in_rep = False
                        self.play_audio(feedback_msgs["good"], f"good_{exercise_name}")
                    elif angle < up_angle and stage != "down":
                        if not in_rep:
                            incorrect_count += 1
                            self.play_audio(feedback_msgs["start"], f"start_{exercise_name}")
                else:
                    if angle < up_angle:
                        if stage != "up":
                            stage = "up"
                            in_rep = True
                            rep_start_time = time.time()
                            self.play_audio(feedback_msgs["form"], f"form_{exercise_name}")
                    if angle > down_angle and stage == "up":
                        correct_count += 1
                        stage = "down"
                        if in_rep:
                            rep_durations.append(time.time() - rep_start_time)
                            in_rep = False
                        self.play_audio(feedback_msgs["good"], f"good_{exercise_name}")
                    elif angle > down_angle and stage != "up":
                        if not in_rep:
                            incorrect_count += 1
                            self.play_audio(feedback_msgs["start"], f"start_{exercise_name}")

                cv2.putText(image, f'Angle: {int(angle)}°', (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                current_feedback = self.draw_feedback(image, angle, feedback_zones, direction)
                if current_feedback and current_feedback != last_feedback:
                    self.play_audio(current_feedback, f"feedback_{exercise_name}")
                    last_feedback = current_feedback

                for i, point in enumerate(angle_points):
                    color = (0, 255, 0) if i == 1 else (0, 0, 255)
                    coords = self.get_landmark_coords(landmarks, point, image.shape)
                    if coords:
                        cv2.circle(image, coords, 10, color, -1)

            avg_duration = np.mean(rep_durations) if rep_durations else 0
            metrics_placeholder.markdown(f"""
            <div style="background-color:#f0f2f6;padding:10px;border-radius:10px">
                <h4 style="color:#222;font-weight:700;">{exercise_name} Metrics</h4>
                <p style="color:#222;font-size:1.1em;">✅ <b>Correct Reps:</b> {correct_count}</p>
                <p style="color:#222;font-size:1.1em;">❌ <b>Incorrect Reps:</b> {incorrect_count}</p>
                <p style="color:#222;font-size:1.1em;">⏱️ <b>Avg Rep Duration:</b> {avg_duration:.2f}s</p>
            </div>
            """, unsafe_allow_html=True)
            placeholder.image(image, channels='BGR', use_container_width=True)

        self.cap.release()
        self.show_summary(exercise_name, correct_count, incorrect_count, rep_durations, username)

    def show_summary(self, exercise_name: str, correct_count: int,
                     incorrect_count: int, rep_durations: List[float], username: str):
        total_reps = correct_count + incorrect_count
        accuracy = (correct_count / total_reps * 100) if total_reps > 0 else 0
        avg_duration = np.mean(rep_durations) if rep_durations else 0

        st.success("Workout Complete!")
        st.markdown(f"""
        <div style="background-color:#e8f5e9;padding:20px;border-radius:10px">
            <h3 style="color:#2e7d32;">{exercise_name} Summary</h3>
            <p>✅ <b>Correct Reps:</b> {correct_count}</p>
            <p>❌ <b>Incorrect Reps:</b> {incorrect_count}</p>
            <p>📊 <b>Accuracy:</b> {accuracy:.1f}%</p>
            <p>⏱️ <b>Average Rep Duration:</b> {avg_duration:.2f} seconds</p>
        </div>
        """, unsafe_allow_html=True)

        try:
            save_session_to_firestore(
                username=username,
                exercise=exercise_name,
                reps=correct_count,
                duration=np.sum(rep_durations)
            )
            st.info("✅ Session saved to Firebase!")
        except Exception as e:
            st.error(f"❌ Failed to save session: {str(e)}")

        st.session_state.stop_exercise = False


def main():
    st.set_page_config(
        page_title="AI Fitness Trainer Pro",
        layout="wide",
        page_icon="🏋️"
    )

    st.sidebar.title("🏋️ AI Fitness Trainer Pro")
    st.sidebar.markdown("Track your form in real-time with AI feedback")

    if "username" not in st.session_state:
        st.error("User not authenticated. Please log in via Firebase Auth.")
        return

    username = st.session_state["username"]

    exercise = st.sidebar.selectbox(
        "📌 Choose an exercise:",
        list(EXERCISE_CONFIG.keys()),
        index=0
    )

    config = EXERCISE_CONFIG[exercise]

    # Show the reference image and instructions in the white box only
    with st.sidebar:
        st.markdown(f"""
        <div style="background-color:#f8f9fa;padding:10px;border-radius:8px">
        """, unsafe_allow_html=True)
        img_url = get_exercise_image(exercise)
        if img_url:
            st.image(img_url, caption=f"{exercise} Reference", use_container_width=True)
        st.markdown(f"""
            <h4>{exercise} Instructions</h4>
            <p>{config['instruction']}</p>
            <p><b>Target Angles:</b> {config['up_angle']}° to {config['down_angle']}°</p>
        </div>
        """, unsafe_allow_html=True)

    st.title(f"{exercise} Tracker")
    st.caption("📸 Real-time form analysis and feedback")
    video_placeholder = st.empty()
    tracker = ExerciseTracker()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start Exercise", key="start"):
            st.session_state.stop_exercise = False
            tracker.run_exercise(exercise, video_placeholder, username)

    with col2:
        if st.button("⏹️ Stop Exercise", key="stop"):
            st.session_state.stop_exercise = True
            st.warning("Stopping exercise...")


if __name__ == "__main__":
    main()
