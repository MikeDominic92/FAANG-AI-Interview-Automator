from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from dotenv import load_dotenv
import asyncio
from audio_processor import AudioTranscriber
from answer_engine import AnswerGenerator
from resume_processor import ResumeKnowledgeBase
import base64
import numpy as np

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
transcriber = AudioTranscriber(model_name="base.en")
answer_generator = AnswerGenerator(api_key=os.getenv("OPENAI_API_KEY"))
knowledge_base = ResumeKnowledgeBase()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Start audio processing
    audio_buffer = []
    last_transcription = ""
    
    def audio_callback(audio_data):
        audio_buffer.append(audio_data)
    
    transcriber.start_recording(callback=audio_callback)
    
    try:
        while True:
            # Process incoming messages (e.g., resume updates)
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "resume":
                # Update resume context
                knowledge_base.add_documents(message["content"])
                await websocket.send_json({"type": "status", "content": "Resume updated"})
            
            # Process audio buffer
            if len(audio_buffer) > 0:
                # Combine audio chunks
                audio_data = np.concatenate(audio_buffer)
                audio_buffer.clear()
                
                # Transcribe
                transcription = transcriber.transcribe_chunk(audio_data)
                
                if transcription and transcription != last_transcription:
                    last_transcription = transcription
                    
                    # Quick analysis while generating full response
                    analysis = answer_generator.analyze_question(transcription)
                    await websocket.send_json({
                        "type": "analysis",
                        "content": analysis["content"]
                    })
                    
                    # Get relevant resume context
                    context = knowledge_base.query(transcription)
                    
                    # Generate and stream response
                    async for response_chunk in answer_generator.generate_response(transcription, context):
                        await websocket.send_json(response_chunk)
            
            await asyncio.sleep(0.1)  # Small delay to prevent overwhelming the connection
            
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")
    finally:
        transcriber.stop_recording()

@app.post("/upload/resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    knowledge_base.add_document(content)
    return {"status": "success", "message": "Resume processed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
