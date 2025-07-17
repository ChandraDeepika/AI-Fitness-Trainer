import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import logging
import os

# Initialize Firebase only once
if not firebase_admin._apps:
    try:
        # Correct filename: 'firebase_key.json'
        cred_path = os.path.join(os.path.dirname(__file__), "firebase_key.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        logging.info("✅ Firebase initialized successfully.")
    except Exception as e:
        logging.error(f"❌ Firebase initialization failed: {e}")

# Get Firestore DB client
db = firestore.client()

def save_session_to_firestore(username, exercise, reps, duration):
    """
    Saves a workout session under users/{username}/sessions/{docID}
    """
    try:
        session_data = {
            "exercise": exercise,
            "reps": reps,
            "duration": duration,
            "timestamp": datetime.utcnow()
        }

        user_ref = db.collection("users").document(username)
        user_ref.collection("sessions").add(session_data)

        logging.info(f"🔥 Session saved for user '{username}': {exercise}, {reps} reps.")
    except Exception as e:
        logging.error(f"❌ Failed to save session to Firestore: {e}")


def fetch_sessions_from_firestore(username):
    """
    Fetches all workout sessions for a given user from Firestore, ordered by timestamp.
    Returns a list of session dictionaries.
    """
    try:
        sessions = []
        docs = db.collection("users").document(username).collection("sessions") \
                 .order_by("timestamp", direction=firestore.Query.DESCENDING) \
                 .stream()
        for doc in docs:
            session = doc.to_dict()
            session["id"] = doc.id
            sessions.append(session)
        logging.info(f"📥 Retrieved {len(sessions)} sessions for {username}.")
        return sessions
    except Exception as e:
        logging.error(f"❌ Error fetching sessions: {e}")
        return []
