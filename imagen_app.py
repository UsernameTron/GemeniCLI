import streamlit as st
from imagen_generator import generate_images, get_available_models, get_aspect_ratios
import zipfile
import io

# Page configuration
st.set_page_config(
    page_title="Imagen Generator",
    page_icon="🎨",
    layout="wide"
)

# Title and instructions
st.title("🎨 Imagen AI Image Generator")
st.markdown("Create stunning AI-generated images using Google's Imagen models. Enter a detailed prompt and customize your generation settings.")

# Sidebar for settings
with st.sidebar:
    st.header("🎛️ Generation Settings")
    
    # Model selection
    models = get_available_models()
    selected_model = st.selectbox(
        "Model",
        options=list(models.keys()),
        format_func=lambda x: models[x],
        index=0,
        help="Choose the Imagen model for generation"
    )
    
    # Number of images
    num_images = st.slider(
        "Number of Images",
        min_value=1,
        max_value=4,
        value=1,
        help="How many images to generate"
    )
    
    # Aspect ratio
    aspect_ratios = get_aspect_ratios()
    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        options=aspect_ratios,
        index=0,
        help="Choose the aspect ratio for your images"
    )

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("✏️ Prompt")
    
    # Main prompt input
    prompt = st.text_area(
        "Describe the image you want to create",
        placeholder="Example: A majestic mountain landscape at golden hour, with snow-capped peaks reflecting in a crystal-clear alpine lake, painted in the style of romantic landscape art",
        height=120,
        help="Be descriptive and specific for better results"
    )
    
    # Note about negative prompts
    st.info("💡 **Note:** Negative prompts are not supported in the current Imagen API. Focus on detailed positive descriptions instead.")
    
    # Generate button
    generate_button = st.button("🎨 Generate Images", type="primary", use_container_width=True)

with col2:
    st.subheader("🖼️ Generated Images")
    
    # Generate images when button is clicked
    if generate_button:
        if not prompt.strip():
            st.warning("⚠️ Please enter a prompt to generate images.")
        else:
            with st.spinner(f"🎨 Generating {num_images} image(s)... This may take 10-30 seconds."):
                try:
                    image_paths = generate_images(
                        prompt=prompt,
                        model=selected_model,
                        number_of_images=num_images,
                        aspect_ratio=aspect_ratio,
                        negative_prompt=""  # Not supported in current API
                    )
                    
                    if image_paths:
                        st.success(f"✅ Successfully generated {len(image_paths)} image(s)!")
                        
                        # Display images
                        for i, image_path in enumerate(image_paths):
                            st.image(image_path, caption=f"Generated Image {i+1}", use_container_width=True)
                        
                        # Download buttons
                        st.subheader("📥 Download")
                        
                        if len(image_paths) == 1:
                            # Single image download
                            with open(image_paths[0], "rb") as f:
                                st.download_button(
                                    label="📥 Download Image",
                                    data=f.read(),
                                    file_name=f"imagen_generated.png",
                                    mime="image/png",
                                    use_container_width=True
                                )
                        else:
                            # Multiple images as ZIP
                            zip_buffer = io.BytesIO()
                            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                                for i, image_path in enumerate(image_paths):
                                    zip_file.write(image_path, f"imagen_generated_{i+1}.png")
                            
                            st.download_button(
                                label=f"📥 Download All Images ({len(image_paths)} files)",
                                data=zip_buffer.getvalue(),
                                file_name="imagen_generated_images.zip",
                                mime="application/zip",
                                use_container_width=True
                            )
                    else:
                        st.error("❌ No images were generated. Please try again.")
                        
                except Exception as e:
                    st.error(f"❌ Error generating images: {str(e)}")
                    st.info("💡 Make sure your API key is valid and you have access to Imagen models.")

# Tips and examples section
with st.expander("💡 Tips for Better Image Generation"):
    st.markdown("""
    **Prompt Writing Tips:**
    - Be specific and descriptive about what you want
    - Include details about style, lighting, composition, and mood
    - Mention specific art styles or techniques if desired
    - Use adjectives to describe colors, textures, and atmosphere
    
    **Good Example Prompts:**
    - "A cyberpunk cityscape at night with neon lights reflecting on wet streets, rain falling, dramatic lighting, highly detailed digital art"
    - "A cozy cottage in an enchanted forest, surrounded by glowing mushrooms and fireflies, magical atmosphere, fairy tale illustration style"
    - "Portrait of a wise elderly wizard with a long white beard, wearing ornate robes, ancient library background, oil painting style"
    
    **Instead of Negative Prompts:**
    - Be very specific about what you DO want
    - Use quality descriptors: "high quality, detailed, sharp, professional"
    - Specify style clearly: "photorealistic", "digital art", "oil painting"
    
    **Model Differences:**
    - **Imagen 3.0**: High quality text-to-image generation
    - **Imagen 4 (Preview)**: Latest model with enhanced quality and detail
    - **Imagen 4 Ultra (Preview)**: Highest quality, most detailed results
    """)

# Footer
st.markdown("---")
st.markdown("*Powered by Google's Imagen via Gemini API*")