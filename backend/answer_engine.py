import openai
from typing import Dict, List
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json

class AnswerGenerator:
    def __init__(self, api_key: str, model: str = "gpt-4-1106-preview"):
        openai.api_key = api_key
        self.model = model
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.context_window = []
        self.max_context_length = 4  # Keep last 4 exchanges
        
    def _prepare_prompt(self, question: str, resume_context: List[str]) -> str:
        """Prepare the prompt with resume context and conversation history"""
        context = "\n".join(resume_context)
        history = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.context_window])
        
        return f"""You are an AI interview assistant helping with a real-time job interview.
Use the following resume context to personalize your answers:
{context}

Previous conversation:
{history}

Current interview question: {question}

Provide a concise, professional response that:
1. Directly addresses the question
2. Uses specific examples from the resume
3. Follows the STAR method where applicable
4. Keeps the response brief but impactful

Response:"""

    async def generate_response(self, question: str, resume_context: List[str]) -> Dict:
        """Generate a response to an interview question asynchronously"""
        try:
            # Add streaming for real-time response generation
            prompt = self._prepare_prompt(question, resume_context)
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional interview coach providing real-time assistance."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300,  # Shorter responses for faster generation
                stream=True  # Enable streaming
            )
            
            # Process the streaming response
            collected_chunks = []
            collected_messages = []
            
            async for chunk in response:
                collected_chunks.append(chunk)
                chunk_message = chunk['choices'][0]['delta'].get('content', '')
                collected_messages.append(chunk_message)
                
                # Yield each part of the response as it's generated
                if chunk_message:
                    yield {
                        "type": "partial",
                        "content": chunk_message
                    }
            
            # Store the complete response in context
            full_response = ''.join(collected_messages)
            self.context_window.append((question, full_response))
            if len(self.context_window) > self.max_context_length:
                self.context_window.pop(0)
            
            yield {
                "type": "complete",
                "content": full_response
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "content": f"Error generating response: {str(e)}"
            }
    
    def analyze_question(self, question: str) -> Dict:
        """Quickly analyze the question to provide immediate guidance"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Faster model for quick analysis
                messages=[
                    {"role": "system", "content": "Analyze interview questions and provide quick guidance."},
                    {"role": "user", "content": f"Analyze this interview question and provide quick tips: {question}"}
                ],
                temperature=0.3,
                max_tokens=100
            )
            return {
                "type": "analysis",
                "content": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "type": "error",
                "content": f"Error analyzing question: {str(e)}"
            }
