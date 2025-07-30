import os
from typing import List
from google import genai
from google.genai import types

# Initialize the Gemini API client using your API key
client = genai.Client(api_key="AIzaSyD8ZDvncRoQ-1FwAYJCQXO9TcjCBdfTLe8")

# Available Imagen models (updated for current API)
IMAGEN_MODELS = {
    "imagen-3.0-generate-002": "Imagen 3.0",
    "imagen-4.0-generate-preview-06-06": "Imagen 4 (Preview)", 
    "imagen-4.0-ultra-generate-preview-06-06": "Imagen 4 Ultra (Preview)"
}

ASPECT_RATIOS = ["1:1", "3:4", "4:3", "9:16", "16:9"]

def generate_images(
    prompt: str, 
    model: str = "imagen-3.0-generate-002",
    number_of_images: int = 1,
    aspect_ratio: str = "1:1",
    negative_prompt: str = ""
) -> List[str]:
    """
    Generate images using Imagen models via Gemini API.
    Returns a list of local file paths to the generated images.
    """
    
    print(f"Generating {number_of_images} image(s) with {IMAGEN_MODELS.get(model, model)}")
    print(f"Prompt: {prompt}")
    if negative_prompt:
        print(f"Note: Negative prompt provided but not supported in current API version")
    
    try:
        # Configure generation parameters (negative_prompt not supported in current API)
        config = types.GenerateImagesConfig(
            number_of_images=number_of_images,
            aspect_ratio=aspect_ratio,
            include_rai_reason=True,
        )
        
        # Send request to generate images
        response = client.models.generate_images(
            model=model,
            prompt=prompt,
            config=config
        )
        
        # Process the response and save images locally
        saved_paths = []
        
        if response and hasattr(response, 'generated_images') and response.generated_images:
            print(f"Successfully received {len(response.generated_images)} image(s)")
            
            for i, generated_image in enumerate(response.generated_images):
                if hasattr(generated_image, 'image') and generated_image.image:
                    if hasattr(generated_image.image, 'image_bytes') and generated_image.image.image_bytes:
                        # Save image locally
                        filename = f"generated_image_{i+1}.png"
                        with open(filename, "wb") as f:
                            f.write(generated_image.image.image_bytes)
                        saved_paths.append(filename)
                        print(f"Saved image: {filename}")
                    else:
                        print(f"Image {i+1} has no image_bytes")
                else:
                    print(f"Image {i+1} has no image data")
        else:
            print("No images were generated or response was empty")
            
        return saved_paths
        
    except Exception as e:
        print(f"Error generating images: {e}")
        raise e

def get_available_models():
    """Return dictionary of available Imagen models"""
    return IMAGEN_MODELS

def get_aspect_ratios():
    """Return list of supported aspect ratios"""
    return ASPECT_RATIOS

if __name__ == "__main__":
    # Test the function with sample inputs
    prompt = "A serene mountain landscape at sunset, with vibrant orange and purple skies reflecting on a calm lake"
    
    try:
        image_paths = generate_images(
            prompt=prompt,
            model="imagen-3.0-generate-002",
            number_of_images=1,
            aspect_ratio="16:9",
            negative_prompt="blurry, low quality"
        )
        print(f"Successfully generated {len(image_paths)} images: {image_paths}")
    except Exception as e:
        print(f"Failed to generate images: {e}")