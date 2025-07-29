import streamlit as st
from veo3_video_generator import generate_video

# Title and instructions
st.title("🎬 Veo 3 Video Generator")
st.markdown("Enter a scene description and dialogue, then click **Generate Video** to create an AI-generated clip with audio.")

# Input fields for scene and dialogue
scene_text = st.text_area(
    "Scene Description",
    placeholder="Example: A medieval marketplace at dusk, people bustling around, warm torchlight flickering",
    help="Describe the setting, visuals, and actions for the scene.",
    height=100
)

dialogue_text = st.text_area(
    "Dialogue (optional)",
    placeholder='Example: Merchant: "Fresh apples! Get your fresh apples here!" Customer: "I\'ll take two, please."',
    help="Dialogue lines or sound cues. Use quotes to indicate spoken words.",
    height=100
)

# Generate button
if st.button("🎥 Generate Video", type="primary"):
    if not scene_text.strip():
        st.warning("⚠️ Please enter a scene description.")
    else:
        # Show a spinner/progress indicator while generating
        with st.spinner("🎬 Generating video... please wait (~30-60 seconds)"):
            try:
                video_file = generate_video(scene_text, dialogue_text)
                st.success("✅ Video generated successfully!")
                
                # Display the video in the app
                st.video(video_file)
                
                # Provide a download button for the video
                with open(video_file, "rb") as f:
                    video_bytes = f.read()
                    st.download_button(
                        label="📥 Download Video",
                        data=video_bytes,
                        file_name="veo3_output.mp4",
                        mime="video/mp4"
                    )
                    
            except Exception as e:
                st.error(f"❌ Error generating video: {str(e)}")
                st.info("💡 Make sure your API key is valid and you have access to Veo 3.")

# Instructions and tips
with st.expander("💡 Tips for better video generation"):
    st.markdown("""
    **Scene Description Tips:**
    - Be specific about the setting, lighting, and atmosphere
    - Describe character actions and movements
    - Include visual details like colors, textures, and mood
    
    **Dialogue Tips:**
    - Use quotes around spoken words: "Hello there!"
    - Include character names: John: "How are you?"
    - Describe sound effects: *sound of footsteps*, *gentle wind*
    - Mention ambient sounds: bustling crowd, crackling fire
    
    **Example Prompts:**
    - Scene: "A cozy coffee shop on a rainy day, soft jazz playing, warm lighting"
    - Dialogue: 'Barista: "What can I get you today?" Customer: "I\'ll have a cappuccino, please."'
    """)

# Footer
st.markdown("---")
st.markdown("*Powered by Google's Veo 3 via Gemini API*")