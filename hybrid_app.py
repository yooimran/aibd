import sys
import os
from flask import Flask, render_template, request, jsonify
import json
import re
from datetime import datetime
from collections import Counter
import pickle
import requests

class SimpleAITrainer:
    """Lightweight AI trainer that works without sklearn/pandas"""
    
    def __init__(self):
        self.conversations_file = "training_data/conversations.json"
        self.patterns_file = "training_data/learned_patterns.json"
        self.model_file = "training_data/simple_model.pkl"
        
        # Ensure directories exist
        os.makedirs("training_data", exist_ok=True)
        
        # Load existing data
        self.conversations = self.load_conversations()
        self.patterns = self.load_patterns()
        
    def load_conversations(self):
        """Load conversation history"""
        if os.path.exists(self.conversations_file):
            try:
                with open(self.conversations_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def load_patterns(self):
        """Load learned patterns"""
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_conversations(self):
        """Save conversations to file"""
        with open(self.conversations_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversations, f, indent=2, ensure_ascii=False)
    
    def save_patterns(self):
        """Save patterns to file"""
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, indent=2, ensure_ascii=False)
    
    def log_conversation(self, user_input, bot_response, feedback=None):
        """Log a conversation"""
        conversation = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'bot_response': bot_response,
            'feedback': feedback
        }
        
        self.conversations.append(conversation)
        self.save_conversations()
        
        # Auto-learn from positive feedback
        if feedback in ('good', 'User taught response'):
            self.learn_from_positive_feedback(user_input, bot_response)
    
    def learn_from_positive_feedback(self, user_input, bot_response):
        """Learn patterns from positive feedback"""
        # Extract keywords from user input
        keywords = self.extract_keywords(user_input.lower())
        
        # Store the successful response pattern
        for keyword in keywords:
            if keyword not in self.patterns:
                self.patterns[keyword] = []
            
            # Store response if not already there
            if bot_response not in self.patterns[keyword]:
                self.patterns[keyword].append(bot_response)
        
        self.save_patterns()
    
    def extract_keywords(self, text):
        """Extract meaningful keywords from text"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        
        # Extract words (simple tokenization)
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out stop words and short words
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords[:5]  # Return top 5 keywords
    
    def get_learned_response(self, user_input):
        """Get a response based on learned patterns or exact match"""
        # First, check for exact match in conversations with positive feedback
        for conv in reversed(self.conversations):
            if conv.get('feedback') in ('good', 'User taught response') and conv['user_input'].strip().lower() == user_input.strip().lower():
                return conv['bot_response']
        
        # Fallback to keyword-based matching
        keywords = self.extract_keywords(user_input.lower())
        possible_responses = []
        for keyword in keywords:
            if keyword in self.patterns:
                possible_responses.extend(self.patterns[keyword])
        
        # Return most common response if any found
        if possible_responses:
            response_counts = Counter(possible_responses)
            return response_counts.most_common(1)[0][0]
        
        return None
    
    def get_training_stats(self):
        """Get training statistics"""
        total_conversations = len(self.conversations)
        
        # Count feedback - include both 'good' and 'User taught response'
        positive_feedback = sum(1 for conv in self.conversations if conv.get('feedback') in ('good', 'User taught response'))
        negative_feedback = sum(1 for conv in self.conversations if conv.get('feedback') == 'bad')
        
        # Count learned patterns
        total_patterns = sum(len(responses) for responses in self.patterns.values())
        
        return {
            'total_conversations': total_conversations,
            'positive_feedback': positive_feedback,
            'negative_feedback': negative_feedback,
            'learned_patterns': len(self.patterns),
            'total_pattern_responses': total_patterns,
            'learning_rate': f"{(positive_feedback / max(total_conversations, 1)) * 100:.1f}%"
        }
    
    def train_simple_model(self):
        """Train a simple pattern-based model"""
        print("Training simple AI model...")
        
        # Count word frequencies in positive feedback conversations
        word_freq = Counter()
        response_patterns = {}
        
        for conv in self.conversations:
            if conv.get('feedback') in ('good', 'User taught response'):
                words = self.extract_keywords(conv['user_input'])
                word_freq.update(words)
                
                # Associate words with successful responses
                for word in words:
                    if word not in response_patterns:
                        response_patterns[word] = []
                    response_patterns[word].append(conv['bot_response'])
        
        # Save the simple model
        model_data = {
            'word_frequencies': dict(word_freq),
            'response_patterns': response_patterns,
            'training_date': datetime.now().isoformat(),
            'total_conversations': len(self.conversations)
        }
        
        with open(self.model_file, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Simple model trained with {len(self.conversations)} conversations")
        print(f"Learned {len(response_patterns)} word-response patterns")
        
        return True
    
    def export_training_data(self, filename="exported_training_data.json"):
        """Export all training data"""
        export_data = {
            'conversations': self.conversations,
            'patterns': self.patterns,
            'stats': self.get_training_stats(),
            'export_date': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def import_training_data(self, filename):
        """Import training data from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if 'conversations' in import_data:
                self.conversations.extend(import_data['conversations'])
                self.save_conversations()
            
            if 'patterns' in import_data:
                # Merge patterns
                for keyword, responses in import_data['patterns'].items():
                    if keyword not in self.patterns:
                        self.patterns[keyword] = []
                    self.patterns[keyword].extend(responses)
                    # Remove duplicates
                    self.patterns[keyword] = list(set(self.patterns[keyword]))
                self.save_patterns()
            
            return True
        except Exception as e:
            print(f"Import failed: {e}")
            return False

# Always try to initialize trainer
try:
    TRAINING_AVAILABLE = True
    print("✓ Training system ready")
except Exception as e:
    TRAINING_AVAILABLE = False
    print("✗ Training features not available:", e)

app = Flask(__name__)

class CustomAIChatbot:
    def __init__(self):
        # Only use training data for responses
        if TRAINING_AVAILABLE:
            self.trainer = SimpleAITrainer()
        else:
            self.trainer = None
    
    def get_response(self, user_input):
        """Get AI response from training data, else Wikipedia and self-learn"""
        if self.trainer:
            learned_response = self.trainer.get_learned_response(user_input)
            if learned_response:
                return learned_response
        # Wikipedia fallback
        wiki_summary = get_wikipedia_summary(user_input)
        # Self-learn: log Wikipedia answer as 'User taught response'
        if self.trainer:
            self.trainer.log_conversation(user_input, wiki_summary, feedback="User taught response")
        return wiki_summary
    
    def matches_pattern(self, text, patterns):
        """Check if text matches any of the given patterns"""
        for pattern in patterns:
            if pattern in text:
                return True
        return False
    
    def get_random_response(self, category):
        """Get a random response from a category"""
        import random
        return random.choice(self.responses[category])
    
    def log_conversation(self, user_input, bot_response, feedback=None):
        """Log conversation for training"""
        if self.trainer:
            self.trainer.log_conversation(user_input, bot_response, feedback)
            return True
        return False

# Initialize chatbot
chatbot = CustomAIChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '').strip()
        
        if not user_input:
            return jsonify({'response': 'Please enter a message!'})
        
        # Get AI response
        response = chatbot.get_response(user_input)
        
        # Log conversation if training is available
        if chatbot.trainer:
            chatbot.log_conversation(user_input, response)
        
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'response': f'Sorry, I encountered an error: {str(e)}'})

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.json
        user_input = data.get('user_input')
        bot_response = data.get('bot_response')
        feedback_type = data.get('feedback')
        
        if chatbot.trainer:
            chatbot.log_conversation(user_input, bot_response, feedback_type)
            return jsonify({'status': 'success', 'message': 'Feedback recorded!'})
        else:
            return jsonify({'status': 'info', 'message': 'Training features not available'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/training_report')
def training_report():
    if not TRAINING_AVAILABLE or not chatbot.trainer:
        return jsonify({
            'available': False,
            'message': 'Training features not available. Install training packages to enable this feature.'
        })
    
    try:
        stats = chatbot.trainer.get_training_stats()
        return jsonify({
            'available': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'available': False,
            'error': str(e)
        })

@app.route('/train_model', methods=['POST'])
def train_model():
    if not TRAINING_AVAILABLE or not chatbot.trainer:
        return jsonify({
            'success': False,
            'message': 'Training features not available'
        })
    
    try:
        success = chatbot.trainer.train_simple_model()
        if success:
            return jsonify({
                'success': True,
                'message': 'Simple AI model trained successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Training failed'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Training error: {str(e)}'
        })

@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain the AI model with current data"""
    if not TRAINING_AVAILABLE or not chatbot.trainer:
        return jsonify({
            'success': False,
            'message': 'Training features not available'
        })
    
    try:
        # Retrain the model with current conversation data
        success = chatbot.trainer.train_simple_model()
        if success:
            return jsonify({
                'success': True,
                'message': 'AI model retrained successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Retraining failed - no training data available'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Retraining error: {str(e)}'
        })

@app.route('/export_training')
def export_training():
    if not TRAINING_AVAILABLE or not chatbot.trainer:
        return jsonify({
            'success': False,
            'message': 'Training features not available'
        })
    
    try:
        filename = chatbot.trainer.export_training_data()
        return jsonify({
            'success': True,
            'message': f'Training data exported to {filename}',
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Export error: {str(e)}'
        })

@app.route('/import_training', methods=['POST'])
def import_training():
    if not TRAINING_AVAILABLE or not chatbot.trainer:
        return jsonify({
            'success': False,
            'message': 'Training features not available'
        })
    
    try:
        data = request.json
        filename = data.get('filename')
        
        if not filename:
            return jsonify({
                'success': False,
                'message': 'No filename provided'
            })
        
        success = chatbot.trainer.import_training_data(filename)
        if success:
            return jsonify({
                'success': True,
                'message': f'Training data imported from {filename}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Import failed'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Import error: {str(e)}'
        })

@app.route('/training_data')
def get_training_data():
    if not TRAINING_AVAILABLE or not chatbot.trainer:
        return jsonify({
            'available': False,
            'message': 'Training features not available'
        })
    
    try:
        return jsonify({
            'available': True,
            'conversations': chatbot.trainer.conversations[-10:],  # Last 10 conversations
            'patterns': list(chatbot.trainer.patterns.keys())[:20],  # Top 20 learned patterns
            'stats': chatbot.trainer.get_training_stats()
        })
    except Exception as e:
        return jsonify({
            'available': False,
            'error': str(e)
        })

def get_wikipedia_summary(query):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "No summary found.")
    except Exception:
        pass
    return "Sorry, I couldn't find an answer for that. Please try asking in a different way or teach me!"

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 AI-BD Chatbot Starting...")
    print("=" * 50)
    
    if TRAINING_AVAILABLE:
        print("✓ Training features: ENABLED")
        print("✓ Learning capabilities: ACTIVE")
    else:
        print("ℹ Training features: DISABLED")
        print("ℹ Install training packages for full features")
    
    print(f"🌐 Server starting at: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
