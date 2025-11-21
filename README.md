# AI-chatbot
# AI Chatbot with Flask & Groq API

A modern, responsive AI chatbot built using **Flask** and **Groq’s LLaMA models**.  
It features real-time chat, message history, typing indicators, theme toggle, and a smooth animated UI.  
The backend interacts with the Groq API to generate fast and intelligent responses.

---

## 🚀 Features

- 🔹 Start new chat with welcome message  
- 🔹 Real-time AI responses using Groq API  
- 🔹 Chat history (load, view, delete)  
- 🔹 Typing indicator animation  
- 🔹 Light/Dark theme support  
- 🔹 Responsive modern UI  
- 🔹 Local history rendering  
- 🔹 Error handling & loading states  

---

## 🛠️ Tech Stack

**Frontend:**  
- HTML  
- CSS  
- JavaScript  

**Backend:**  
- Flask  
- Groq API  
- Python  

---

## 📦 Installation

1. Clone the repository
2. pip install -r requirements.txt
3. GROQ_API_KEY = "your_api_key_here"
4. python app.py
5. http://127.0.0.1:5000

project/
│── app.py
│── groq_api.py
│── requirements.txt
│── templates/
│     └── index.html

🧠 How It Works

Flask handles routing, chat creation, message sending, and history.

The backend sends user messages to Groq’s LLaMA model.

Responses are returned to the UI and displayed in the chat container.

Chat history updates automatically for each session.

.

📜 License

This project is released under the MIT License.


⭐ Contribute

Pull requests and improvements are welcome!
