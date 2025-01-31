import numpy as np
import soundfile as sf
from whispercpp import Whisper

class AudioTranscriber:
    def __init__(self, model_size='base.en'):
        self.whisper = Whisper(model_size)
        
    def transcribe(self, audio_data: bytes) -> str:
        # Convert bytes to numpy array
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        
        # Save to temp file for processing
        with open("temp.wav", "wb") as f:
            sf.write(f, audio_np, 16000, format='WAV', subtype='PCM_16')
            
        # Transcribe
        result = self.whisper.transcribe("temp.wav")
        return result["text"]
