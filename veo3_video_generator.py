import time
import os
from google import genai
from google.genai import types

# Initialize the Gemini API client using your API key
client = genai.Client(api_key="AIzaSyD8ZDvncRoQ-1FwAYJCQXO9TcjCBdfTLe8")

def generate_video(scene_description: str, dialogue_script: str) -> str:
    """
    Generate a video using Veo 3 (Gemini API) from a scene description and dialogue.
    Returns the filepath of the downloaded video.
    """
    # Combine scene description and dialogue into one prompt.
    # Ensure dialogue is properly quoted for the model to generate speech.
    prompt = scene_description.strip()
    if dialogue_script.strip():
        prompt += " " + dialogue_script.strip()
    
    print(f"Sending prompt to Gemini API: {prompt}")
    
    try:
        # Send request to generate video (using Veo 3 preview model)
        operation = client.models.generate_videos(
            model="veo-3.0-generate-preview",  # Veo 3 model (8s video + audio)
            prompt=prompt,
            # You can also pass additional parameters via config:
            # config=types.GenerateVideosConfig(negative_prompt="text to avoid", aspect_ratio="16:9", ...)
        )
        
        # Poll the operation status until the video is ready
        print("Starting video generation... This may take 20-60 seconds.")
        while not operation.done:
            time.sleep(10)  # wait before polling again
            operation = client.operations.get(operation)
            print("Waiting for video generation to complete...")
        
        # Once done, get the generated video result
        result = operation.result  # (could also use operation.response)
        
        if hasattr(result, 'generated_videos') and result.generated_videos:
            video_obj = result.generated_videos[0]  # The first (and only) video generated
            
            # Download the video content
            output_path = "generated_video.mp4"
            
            # Save the video file locally
            with open(output_path, "wb") as f:
                video_data = client.files.download(file=video_obj.video)
                f.write(video_data)
            
            print(f"Video saved to {output_path}")
            return output_path
        else:
            raise Exception("No video was generated in the response")
            
    except Exception as e:
        print(f"Error generating video: {e}")
        raise e

if __name__ == "__main__":
    # Test the function with sample inputs
    scene = "A medieval marketplace at dusk, people bustling around, warm torchlight flickering"
    dialogue = 'Merchant: "Fresh apples! Get your fresh apples here!" Customer: "I\'ll take two, please."'
    
    try:
        video_path = generate_video(scene, dialogue)
        print(f"Successfully generated video: {video_path}")
    except Exception as e:
        print(f"Failed to generate video: {e}")