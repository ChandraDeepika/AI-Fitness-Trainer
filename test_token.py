import requests
import toml

def test_huggingface_token():
    # Load the API key from secrets.toml
    try:
        with open("models/secrets.toml", "r") as f:
            config = toml.load(f)
            api_key = config["huggingface"]["api_key"]
    except Exception as e:
        print(f"❌ Error loading API key: {e}")
        return

    # Test API endpoint
    API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {api_key}"}

    # Simple test query
    test_payload = {
        "inputs": "Hello, I'm interested in fitness. Can you help me?",
        "parameters": {
            "max_length": 100,
            "temperature": 0.7
        }
    }

    print("🔄 Testing your Hugging Face API token...")
    
    try:
        response = requests.post(API_URL, headers=headers, json=test_payload)
        
        if response.status_code == 200:
            print("✅ Token is working correctly!")
            print("\nTest response:")
            print(response.json())
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during API call: {e}")

if __name__ == "__main__":
    test_huggingface_token() 