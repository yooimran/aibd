from flask import Flask, render_template, request, jsonify
import re
import random
import datetime
import json

app = Flask(__name__)

class CustomAIChatbot:
    def __init__(self):
        self.conversation_patterns = {
            # Greetings
            r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b': [
                "Hello! I'm AI-BD. How can I assist you today?",
                "Hi there! Welcome to our conversation. What's on your mind?",
                "Hey! Great to meet you. I'm here to help and chat!",
                "Greetings! I'm AI-BD, designed to have meaningful conversations with you."
            ],
            
            # How are you
            r'\b(how are you|how do you feel|what\'s up)\b': [
                "I'm doing wonderfully! As an AI, I'm always excited to learn and chat.",
                "I'm functioning perfectly and ready to help you with anything!",
                "I'm great! Every conversation teaches me something new.",
                "I'm doing well, thank you for asking! How are you feeling today?"
            ],
            
            # Name questions
            r'\b(what is your name|who are you|what are you called)\b': [
                "I'm AI-BD, your custom AI assistant! You can call me whatever you'd like.",
                "I'm AI-BD, a unique AI chatbot created specifically for meaningful conversations.",
                "I'm AI-BD, your personal AI companion - no fancy API needed, just genuine conversation!",
                "I'm AI-BD, an AI assistant built with care and attention to provide helpful responses."
            ],
            
            # Time and date
            r'\b(what time|current time|what date|today\'s date)\b': [
                f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')} and today's date is {datetime.datetime.now().strftime('%B %d, %Y')}.",
                f"Right now it's {datetime.datetime.now().strftime('%I:%M %p')} on {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
            ],
            
            # Weather (simulated)
            r'\b(weather|temperature|forecast)\b': [
                "I don't have access to real-time weather data, but I'd recommend checking your local weather app!",
                "While I can't check the actual weather, I hope it's a beautiful day wherever you are!",
                "I wish I could tell you the weather! Maybe in a future update I'll have that capability."
            ],
            
            # Technology questions
            r'\b(artificial intelligence|AI|machine learning|technology)\b': [
                "AI is fascinating! I'm a simple example of how technology can simulate conversation.",
                "Technology is amazing! I'm built using pattern recognition and response generation.",
                "AI and machine learning are revolutionizing how we interact with computers!",
                "I'm a basic AI that shows how technology can create engaging conversations."
            ],
            
            # Help requests
            r'\b(help|assist|support|guide)\b': [
                "I'm here to help! I can chat about various topics, answer questions, and provide information.",
                "I'd be happy to assist you! What specific topic would you like to discuss?",
                "I'm designed to be helpful! Feel free to ask me about anything you're curious about.",
                "Let me know what you need help with - I'll do my best to provide useful information!"
            ],
            
            # Programming questions
            r'\b(programming|coding|python|javascript|html|css)\b': [
                "Programming is exciting! I love discussing code and development concepts.",
                "Coding is like digital art - creating something functional and beautiful!",
                "Programming languages are tools for bringing ideas to life in the digital world.",
                "I enjoy talking about programming! What specific language or concept interests you?"
            ],
            
            # Emotions
            r'\b(sad|happy|excited|angry|frustrated|confused)\b': [
                "I understand emotions play a big role in our daily experiences. How can I help?",
                "Emotions are complex and important. Would you like to talk about what you're feeling?",
                "I may be an AI, but I recognize that emotions are a vital part of human experience.",
                "Feelings are natural and valid. I'm here to listen if you'd like to share more."
            ],
            
            # Training and learning
            r'\b(train|learn|teach|improve|feedback)\b': [
                "I'm always learning! You can help me improve by chatting with me regularly.",
                "I love learning from our conversations! Every chat helps me become smarter and more helpful.",
                "Training me is easy! Just chat with me regularly and I'll learn from our interactions.",
                "I'm designed to learn and adapt! The more we talk, the better I become at understanding you."
            ],
            
            # Goodbye
            r'\b(goodbye|bye|see you|farewell|take care)\b': [
                "Goodbye! It was wonderful chatting with you. Come back anytime!",
                "See you later! I enjoyed our conversation and hope to chat again soon!",
                "Farewell! Thank you for the engaging conversation. Take care!",
                "Bye for now! I'll be here whenever you want to chat again."
            ],
            
            # Questions about the future
            r'\b(future|tomorrow|next week|prediction)\b': [
                "The future is full of possibilities! While I can't predict it, I'm optimistic about what's to come.",
                "I can't see the future, but I believe in the power of human creativity and innovation!",
                "The future is unwritten and full of potential. What are your hopes for tomorrow?",
                "While I can't predict the future, I think it will be shaped by the choices we make today."
            ]
        }
        
        self.fallback_responses = [
            "That's an interesting point! Can you tell me more about your thoughts on that?",
            "I find that topic fascinating. What's your perspective on it?",
            "I'm still learning about that topic. What would you like to know specifically?",
            "That's something I'd love to explore more with you. What aspects interest you most?",
            "I appreciate you sharing that with me. What made you think about this topic?",
            "That's a great question! While I might not have all the answers, I enjoy discussing it.",
            "I'm curious about your viewpoint on this. Can you elaborate a bit more?",
            "Every conversation teaches me something new. What's your experience with this?",
            "That's definitely worth discussing! What would you like to know about it?",
            "I find human perspectives on topics like this really valuable. What do you think?"
        ]
        
        self.context_memory = []
    
    def get_response(self, user_input):
        user_input_lower = user_input.lower()
        
        # Store context
        self.context_memory.append(user_input_lower)
        if len(self.context_memory) > 5:  # Keep last 5 messages for context
            self.context_memory.pop(0)
        
        # Check for patterns
        for pattern, responses in self.conversation_patterns.items():
            if re.search(pattern, user_input_lower):
                response = random.choice(responses)
                return self.add_personality(response, user_input_lower)
        
        # If no pattern matches, use fallback with context awareness
        return self.contextual_fallback(user_input_lower)
    
    def add_personality(self, response, user_input):
        # Add some personality based on input
        if "thanks" in user_input or "thank you" in user_input:
            response += " You're very welcome!"
        elif "?" in user_input:
            response += " Feel free to ask me anything else!"
        elif "!" in user_input:
            response += " I love your enthusiasm!"
        
        return response
    
    def contextual_fallback(self, user_input):
        # Try to create contextual responses based on previous conversation
        if any(word in " ".join(self.context_memory) for word in ["programming", "code", "python"]):
            return "Since we've been talking about programming, I'd love to continue that discussion! What specific aspect interests you?"
        elif any(word in " ".join(self.context_memory) for word in ["help", "problem", "issue"]):
            return "I see you might need some assistance. I'm here to help however I can!"
        else:
            return random.choice(self.fallback_responses)

# Initialize the chatbot
chatbot = CustomAIChatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if user_message.strip():
        bot_response = chatbot.get_response(user_message)
        return jsonify({
            'response': bot_response,
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
            'training_enabled': False  # Training disabled in simple version
        })
    return jsonify({'response': 'I didn\'t catch that. Could you please try again?'})

# Dummy routes for training features (return not available)
@app.route('/feedback', methods=['POST'])
def feedback():
    return jsonify({'success': False, 'message': 'Training features not available in simple mode'})

@app.route('/training_report')
def training_report():
    return jsonify({'error': 'Training not available in simple mode'})

@app.route('/retrain', methods=['POST'])
def retrain():
    return jsonify({'success': False, 'message': 'Training not available in simple mode'})

@app.route('/export_training')
def export_training():
    return jsonify({'error': 'Training not available in simple mode'})

if __name__ == '__main__':
    print("Starting AI-BD Chatbot (Simple Mode)")
    print("Training features disabled - install requirements.txt for full features")
    print("Server starting at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
