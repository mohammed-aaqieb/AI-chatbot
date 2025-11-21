# app.py
from flask import Flask, render_template, request, jsonify, session
from groq_api import get_groq_response
import uuid
import json
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'ai-chatbot-secret-key-2024'
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)

# In-memory storage for chat history
chat_sessions = {}

@app.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['current_chat_id'] = None
    
    return render_template('index.html')

@app.route('/start_chat', methods=['POST'])
def start_chat():
    user_id = session['user_id']
    
    # Create new chat session
    chat_id = str(uuid.uuid4())
    session['current_chat_id'] = chat_id
    
    if user_id not in chat_sessions:
        chat_sessions[user_id] = {}
    
    chat_sessions[user_id][chat_id] = {
        'title': 'New Chat',
        'messages': [],
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    # Add welcome message
    welcome_message = {
        'role': 'assistant',
        'content': "Hello! I'm your AI assistant. I'm here to help you with anything you need. How can I assist you today? 😊",
        'timestamp': datetime.now().isoformat()
    }
    
    chat_sessions[user_id][chat_id]['messages'].append(welcome_message)
    
    return jsonify({
        'success': True,
        'chat_id': chat_id,
        'welcome_message': welcome_message
    })

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        user_id = session.get('user_id')
        chat_id = session.get('current_chat_id')
        
        if not user_id or not chat_id:
            return jsonify({'error': 'Session expired. Please refresh the page.'}), 401
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        if user_id not in chat_sessions or chat_id not in chat_sessions[user_id]:
            return jsonify({'error': 'Chat session not found'}), 404
        
        # Add user message to history
        user_msg_obj = {
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        }
        
        chat_sessions[user_id][chat_id]['messages'].append(user_msg_obj)
        
        # Update chat title if it's the first user message
        if len(chat_sessions[user_id][chat_id]['messages']) == 2:  # Welcome + first user message
            title = user_message[:50] + "..." if len(user_message) > 50 else user_message
            chat_sessions[user_id][chat_id]['title'] = title
            
        # Update timestamp
        chat_sessions[user_id][chat_id]['updated_at'] = datetime.now().isoformat()
        
        # Get conversation history for context (last 10 messages for context)
        conversation_history = [
            {"role": msg['role'], "content": msg['content']} 
            for msg in chat_sessions[user_id][chat_id]['messages'][-10:]
        ]
        
        # Get AI response
        ai_response = get_groq_response(conversation_history)
        
        # Add AI response to history
        ai_msg_obj = {
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now().isoformat()
        }
        
        chat_sessions[user_id][chat_id]['messages'].append(ai_msg_obj)
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'chat_id': chat_id
        })
        
    except Exception as e:
        print(f"Error in send_message: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'chats': []})
            
        if user_id in chat_sessions:
            # Return list of chats with basic info
            chats = []
            for chat_id, chat_data in chat_sessions[user_id].items():
                chats.append({
                    'id': chat_id,
                    'title': chat_data['title'],
                    'created_at': chat_data['created_at'],
                    'updated_at': chat_data.get('updated_at', chat_data['created_at']),
                    'message_count': len(chat_data['messages'])
                })
            
            # Sort by updated date, newest first
            chats.sort(key=lambda x: x['updated_at'], reverse=True)
            
            return jsonify({'success': True, 'chats': chats})
        
        return jsonify({'success': True, 'chats': []})
        
    except Exception as e:
        print(f"Error in get_chat_history: {str(e)}")
        return jsonify({'success': False, 'chats': []})

@app.route('/get_chat_messages/<chat_id>', methods=['GET'])
def get_chat_messages(chat_id):
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'Session expired'}), 401
            
        if user_id in chat_sessions and chat_id in chat_sessions[user_id]:
            return jsonify({
                'success': True,
                'messages': chat_sessions[user_id][chat_id]['messages']
            })
        
        return jsonify({'error': 'Chat not found'}), 404
        
    except Exception as e:
        print(f"Error in get_chat_messages: {str(e)}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/delete_chat/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'Session expired'}), 401
            
        if user_id in chat_sessions and chat_id in chat_sessions[user_id]:
            del chat_sessions[user_id][chat_id]
            
            # If we deleted the current chat, clear current_chat_id
            if session.get('current_chat_id') == chat_id:
                session['current_chat_id'] = None
            
            return jsonify({'success': True})
        
        return jsonify({'error': 'Chat not found'}), 404
        
    except Exception as e:
        print(f"Error in delete_chat: {str(e)}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/new_chat', methods=['POST'])
def new_chat():
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'Session expired'}), 401
            
        # Create new chat session
        chat_id = str(uuid.uuid4())
        session['current_chat_id'] = chat_id
        
        if user_id not in chat_sessions:
            chat_sessions[user_id] = {}
        
        chat_sessions[user_id][chat_id] = {
            'title': 'New Chat',
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Add welcome message to new chat
        welcome_message = {
            'role': 'assistant',
            'content': "Hello! I'm here to help you with your new conversation. What would you like to talk about? 🚀",
            'timestamp': datetime.now().isoformat()
        }
        
        chat_sessions[user_id][chat_id]['messages'].append(welcome_message)
        
        return jsonify({
            'success': True,
            'chat_id': chat_id,
            'welcome_message': welcome_message
        })
        
    except Exception as e:
        print(f"Error in new_chat: {str(e)}")
        return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)