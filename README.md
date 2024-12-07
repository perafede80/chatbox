# Real-Time Chatbot with OpenAI Integration

A simple FastAPI application that interacts with the OpenAI API to provide a real-time chatbot experience.

## Installation and Setup

**Install dependencies:**
```bash
   pip install -r requirements.txt
```
## Private OpenAI API Key
In order to run the project is necessary to create an API key from your personal account on https://platform.openai.com/.

Create a .env file in your project's root directory and add your OpenAI API key:
OPENAI_API_KEY=YOUR_API_KEY

## Running the application
To start the chatbot server, follow these steps:

1. **Start the application:**
```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Note: You can replace `8000` with your desired port number if needed.

2. **Connect to the Chatbot:**

Open `http://localhost:8000/ws` in your web browser or use a WebSocket client library to interact with the chatbot.

### Additional Notes

- Ensure you have a stable internet connection for the OpenAI API to function properly.
- The chatbot will be available at `http://localhost:8000/ws` once the server is running.
- For best performance, consider using a reverse proxy like Nginx in production environments.
