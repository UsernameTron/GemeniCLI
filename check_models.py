from google import genai

# Initialize the client
client = genai.Client(api_key="AIzaSyD8ZDvncRoQ-1FwAYJCQXO9TcjCBdfTLe8")

print("Available models:")
try:
    models = client.models.list()
    for model in models:
        print(f"- {model.name}: {model.display_name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"  Methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")