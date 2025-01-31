import sounddevice as sd
import numpy as np
import whisper
import queue
import threading
import torch
from typing import Optional, Callable

class AudioTranscriber:
    def __init__(self, model_name: str = "base.en"):
        self.model = whisper.load_model(model_name)
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.sample_rate = 16000
        self.device_input = None
        self.device_output = None
        self._find_audio_devices()

    def _find_audio_devices(self):
        """Find the system's audio input and output devices"""
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                self.device_input = i
            if device['max_output_channels'] > 0:
                self.device_output = i

    def start_recording(self, callback: Optional[Callable] = None):
        """Start recording both system audio output and microphone input"""
        self.is_recording = True
        
        def audio_callback(indata, outdata, frames, time, status):
            if status:
                print(f"Status: {status}")
            # Process both input (mic) and output (system) audio
            self.audio_queue.put(indata.copy())
            if callback:
                callback(indata.copy())

        # Start the stream
        self.stream = sd.Stream(
            device=(self.device_input, self.device_output),
            samplerate=self.sample_rate,
            channels=1,
            callback=audio_callback,
            dtype=np.float32
        )
        self.stream.start()

        # Start processing thread
        self.process_thread = threading.Thread(target=self._process_audio)
        self.process_thread.start()

    def stop_recording(self):
        """Stop recording and close the audio stream"""
        self.is_recording = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        if hasattr(self, 'process_thread'):
            self.process_thread.join()

    def _process_audio(self):
        """Process audio chunks and transcribe them"""
        audio_buffer = []
        
        while self.is_recording:
            try:
                audio_chunk = self.audio_queue.get(timeout=1)
                audio_buffer.append(audio_chunk)
                
                # Process every 2 seconds of audio
                if len(audio_buffer) * (self.sample_rate / len(audio_chunk)) >= 2:
                    audio_data = np.concatenate(audio_buffer)
                    # Normalize audio data
                    audio_data = audio_data.astype(np.float32)
                    
                    # Transcribe the audio chunk
                    result = self.transcribe_chunk(audio_data)
                    if result and len(result.strip()) > 0:
                        print(f"Transcribed: {result}")
                    
                    # Clear the buffer
                    audio_buffer = []
                    
            except queue.Empty:
                continue

    def transcribe_chunk(self, audio_data: np.ndarray) -> str:
        """Transcribe a chunk of audio data"""
        try:
            # Convert to torch tensor
            audio_tensor = torch.from_numpy(audio_data)
            
            # Transcribe using Whisper
            result = self.model.transcribe(
                audio_tensor,
                language='en',
                task='transcribe',
                fp16=torch.cuda.is_available()
            )
            
            return result["text"].strip()
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return ""
