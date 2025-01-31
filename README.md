# Interview AI Assistant

A real-time interview coaching application that uses your resume and stories to help you answer behavioral and technical questions.

## Features

- Real-time audio transcription
- Resume-based context matching
- AI-generated response suggestions
- Improvement tips and feedback
- Practice session history
- Secure WebSocket communication

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- Whisper.cpp
- ChromaDB
- OpenAI GPT-4

### Frontend
- React 18
- Material-UI
- Web Audio API
- WebSocket

## Setup

1. Clone the repository
```bash
git clone https://github.com/mikedominic92/interview-ai.git
cd interview-ai
```

2. Backend Setup
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

3. Frontend Setup
```powershell
cd ../frontend
npm install
```

4. Configuration
- Create `.env` file in backend directory
```ini
OPENAI_API_KEY=your_key_here
WHISPER_MODEL=base.en
```

## Usage

1. Start Backend
```powershell
cd backend
python server.py
```

2. Start Frontend
```powershell
cd ../frontend
npm start
```

3. Open `http://localhost:3000`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License
MIT
