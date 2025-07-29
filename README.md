# Veo 3 Video Generator

A simple local application that uses Google's Gemini API (Veo 3 model) to generate short videos with audio from text descriptions and dialogue.

## Features

- **Text-to-Video Generation**: Create 8-second videos from scene descriptions
- **Audio Generation**: Automatic speech synthesis from dialogue text
- **Local UI**: Easy-to-use Streamlit web interface
- **Download Support**: Save generated videos as MP4 files

## Setup

1. **Install Dependencies**:
   ```bash
   pip install google-genai streamlit
   ```

2. **API Key**: The application uses the provided Google Gemini API key: `AIzaSyD8ZDvncRoQ-1FwAYJCQXO9TcjCBdfTLe8`

## Usage

### Option 1: Run the Streamlit App (Recommended)
```bash
streamlit run veo3_app.py
```

This will open a web interface at `http://localhost:8501` where you can:
- Enter scene descriptions
- Add dialogue (optional)
- Generate and preview videos
- Download the results

### Option 2: Use the Backend Directly
```bash
python veo3_video_generator.py
```

## Example Prompts

**Scene Description:**
```
A medieval marketplace at dusk, people bustling around, warm torchlight flickering
```

**Dialogue:**
```
Merchant: "Fresh apples! Get your fresh apples here!" Customer: "I'll take two, please."
```

## Tips for Better Results

- **Scene Descriptions**: Be specific about setting, lighting, atmosphere, and character actions
- **Dialogue**: Use quotes around spoken words and include character names
- **Audio Cues**: Describe sound effects and ambient sounds for richer audio
- **Duration**: Videos are automatically generated as 8-second clips with 720p resolution

## Technical Details

- **Model**: `veo-3.0-generate-preview` (Google's Veo 3)
- **Output**: 8-second MP4 videos with synchronized audio
- **Resolution**: 720p
- **Format**: MP4 with audio track

## Files

- `veo3_app.py` - Streamlit web interface
- `veo3_video_generator.py` - Backend video generation logic
- `generated_video.mp4` - Output file (created after first generation)

---

*Powered by Google's Veo 3 via Gemini API*