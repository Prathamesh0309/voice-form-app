import tempfile
import whisper

# Load once
_MODEL = whisper.load_model("base")

def transcribe_audio(audio_bytes) -> str:
    """
    Accepts audio bytes from Streamlit audio_input
    Returns transcription text
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        result = _MODEL.transcribe(tmp.name)

    return result.get("text", "").strip()