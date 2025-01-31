import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import websockets
import asyncio
import json
import os
import threading
from queue import Queue

# Get backend URL from environment variable or use default
BACKEND_URL = os.getenv('BACKEND_URL', 'ws://localhost:8000/ws')

class InterviewAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interview AI Assistant")
        self.root.geometry("800x600")
        
        # Message queue for communication between websocket and GUI
        self.message_queue = Queue()
        
        self.create_widgets()
        self.interview_active = False
        self.websocket = None
        
        # Start message processing
        self.process_messages()
        
    def create_widgets(self):
        # Status label
        self.status_label = ttk.Label(self.root, text="Status: Not Connected")
        self.status_label.pack(pady=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        # Resume upload button
        self.upload_btn = ttk.Button(btn_frame, text="Upload Resume", command=self.upload_resume)
        self.upload_btn.pack(side=tk.LEFT, padx=5)
        
        # Start/Stop button
        self.start_btn = ttk.Button(btn_frame, text="Start Interview", command=self.toggle_interview)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_output)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Output area
        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20)
        self.output_text.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
    def upload_resume(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt")]
        )
        if file_path:
            self.status_label.config(text=f"Status: Resume uploaded - {os.path.basename(file_path)}")
            
    async def connect_websocket(self):
        try:
            self.websocket = await websockets.connect(BACKEND_URL)
            while self.interview_active:
                try:
                    message = await self.websocket.recv()
                    self.message_queue.put(message)
                except websockets.exceptions.ConnectionClosed:
                    break
        except Exception as e:
            self.message_queue.put(f"Error: {str(e)}")
            
    def start_websocket(self):
        asyncio.run(self.connect_websocket())
        
    def toggle_interview(self):
        if not self.interview_active:
            self.start_interview()
        else:
            self.stop_interview()
            
    def start_interview(self):
        self.interview_active = True
        self.start_btn.config(text="Stop Interview")
        self.status_label.config(text="Status: Interview in progress")
        
        # Start websocket in a separate thread
        self.ws_thread = threading.Thread(target=self.start_websocket)
        self.ws_thread.daemon = True
        self.ws_thread.start()
        
    def stop_interview(self):
        self.interview_active = False
        self.start_btn.config(text="Start Interview")
        self.status_label.config(text="Status: Interview stopped")
        
    def process_messages(self):
        try:
            while not self.message_queue.empty():
                message = self.message_queue.get_nowait()
                try:
                    data = json.loads(message)
                    if "content" in data:
                        self.output_text.insert(tk.END, f"{data['content']}\n")
                        self.output_text.see(tk.END)
                except:
                    self.output_text.insert(tk.END, f"{message}\n")
                    self.output_text.see(tk.END)
        except:
            pass
        finally:
            # Schedule the next check
            self.root.after(100, self.process_messages)
            
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = InterviewAssistant()
    app.run()
