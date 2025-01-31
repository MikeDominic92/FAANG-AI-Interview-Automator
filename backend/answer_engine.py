from openai import AsyncOpenAI
import json
from typing import List, Dict

class AnswerGenerator:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def generate_response(self, question: str, context: List[Dict]) -> dict:
        system_prompt = f"""
        You are an interview coaching assistant. Help the user answer this question:
        {question}
        
        Context from their resume:
        {json.dumps(context, indent=2)}
        
        Respond in this JSON format:
        {{
            "answer": "concise answer using resume context",
            "improvement_suggestions": ["list of speaking tips"],
            "keywords_matched": ["list of matched skills"]
        }}
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
