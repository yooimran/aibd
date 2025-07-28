"""
AI-BD Training System
This module provides various ways to train and improve the AI-BD chatbot
"""

import json
import re
import pickle
import os
from datetime import datetime
from collections import defaultdict, Counter
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class AITrainer:
    def __init__(self, data_dir="training_data"):
        self.data_dir = data_dir
        self.conversation_log_file = os.path.join(data_dir, "conversations.json")
        self.feedback_file = os.path.join(data_dir, "feedback.json")
        self.learned_patterns_file = os.path.join(data_dir, "learned_patterns.json")
        self.model_file = os.path.join(data_dir, "trained_model.pkl")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize data structures
        self.conversations = self.load_conversations()
        self.feedback_data = self.load_feedback()
        self.learned_patterns = self.load_learned_patterns()
        self.ml_model = None
        self.vectorizer = None
        
        # Load or create ML model
        self.load_or_create_model()
    
    def load_conversations(self):
        """Load conversation history"""
        if os.path.exists(self.conversation_log_file):
            with open(self.conversation_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def load_feedback(self):
        """Load user feedback data"""
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def load_learned_patterns(self):
        """Load learned conversation patterns"""
        if os.path.exists(self.learned_patterns_file):
            with open(self.learned_patterns_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_data(self):
        """Save all training data"""
        with open(self.conversation_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversations, f, indent=2, ensure_ascii=False)
        
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)
        
        with open(self.learned_patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_patterns, f, indent=2, ensure_ascii=False)
    
    def log_conversation(self, user_input, bot_response, context=None):
        """Log a conversation for training"""
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "bot_response": bot_response,
            "context": context or []
        }
        self.conversations.append(conversation_entry)
        self.save_data()
    
    def add_feedback(self, user_input, bot_response, rating, feedback_text=""):
        """Add user feedback for a response (1-5 rating)"""
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "bot_response": bot_response,
            "rating": rating,
            "feedback": feedback_text
        }
        self.feedback_data.append(feedback_entry)
        self.save_data()
        
        # Learn from negative feedback
        if rating <= 2:
            self.learn_from_negative_feedback(user_input, bot_response, feedback_text)
    
    def learn_from_negative_feedback(self, user_input, bot_response, feedback):
        """Learn from poor responses to improve future ones"""
        # Extract keywords from user input
        keywords = self.extract_keywords(user_input)
        
        # Store as a pattern to avoid in future
        pattern_key = f"avoid_{len(self.learned_patterns)}"
        self.learned_patterns[pattern_key] = {
            "input_keywords": keywords,
            "bad_response": bot_response,
            "feedback": feedback,
            "learn_type": "negative"
        }
    
    def learn_from_positive_feedback(self, user_input, bot_response):
        """Learn from good responses to use similar ones"""
        keywords = self.extract_keywords(user_input)
        
        pattern_key = f"good_{len(self.learned_patterns)}"
        self.learned_patterns[pattern_key] = {
            "input_keywords": keywords,
            "good_response": bot_response,
            "learn_type": "positive"
        }
    
    def extract_keywords(self, text):
        """Extract important keywords from text"""
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text.lower())
        keywords = [word for word in words if word.isalnum() and word not in stop_words]
        return keywords
    
    def train_ml_model(self):
        """Train a machine learning model on conversation data"""
        if len(self.conversations) < 10:
            print("Need at least 10 conversations to train ML model")
            return False
        
        # Prepare training data
        inputs = []
        responses = []
        
        for conv in self.conversations:
            inputs.append(conv['user_input'])
            responses.append(conv['bot_response'])
        
        # Create TF-IDF vectorizer and Naive Bayes classifier
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.ml_model = Pipeline([
            ('tfidf', self.vectorizer),
            ('classifier', MultinomialNB())
        ])
        
        # Train the model
        try:
            # For simplicity, we'll create response categories
            response_categories = self.categorize_responses(responses)
            self.ml_model.fit(inputs, response_categories)
            
            # Save the model
            with open(self.model_file, 'wb') as f:
                pickle.dump((self.ml_model, self.vectorizer), f)
            
            print(f"✅ ML model trained on {len(inputs)} conversations")
            return True
        except Exception as e:
            print(f"❌ Error training ML model: {e}")
            return False
    
    def categorize_responses(self, responses):
        """Categorize responses for training"""
        categories = []
        for response in responses:
            if any(word in response.lower() for word in ['hello', 'hi', 'hey', 'greet']):
                categories.append('greeting')
            elif any(word in response.lower() for word in ['help', 'assist', 'support']):
                categories.append('help')
            elif any(word in response.lower() for word in ['time', 'date', 'clock']):
                categories.append('time')
            elif any(word in response.lower() for word in ['weather', 'temperature']):
                categories.append('weather')
            elif any(word in response.lower() for word in ['programming', 'code', 'python']):
                categories.append('programming')
            else:
                categories.append('general')
        return categories
    
    def load_or_create_model(self):
        """Load existing ML model or create new one"""
        if os.path.exists(self.model_file):
            try:
                with open(self.model_file, 'rb') as f:
                    self.ml_model, self.vectorizer = pickle.load(f)
                print("✅ Loaded existing ML model")
            except Exception as e:
                print(f"❌ Error loading model: {e}")
                self.ml_model = None
                self.vectorizer = None
    
    def get_ml_suggestion(self, user_input):
        """Get ML model suggestion for response"""
        if self.ml_model is None:
            return None
        
        try:
            category = self.ml_model.predict([user_input])[0]
            confidence = max(self.ml_model.predict_proba([user_input])[0])
            
            return {
                'category': category,
                'confidence': confidence
            }
        except Exception as e:
            print(f"Error getting ML suggestion: {e}")
            return None
    
    def find_similar_conversations(self, user_input, top_k=3):
        """Find similar past conversations"""
        if not self.conversations:
            return []
        
        # Use TF-IDF to find similar conversations
        all_inputs = [conv['user_input'] for conv in self.conversations]
        all_inputs.append(user_input)
        
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(all_inputs)
        
        # Calculate similarity with the new input (last item)
        similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
        
        # Get top similar conversations
        similar_indices = similarities.argsort()[-top_k:][::-1]
        
        similar_conversations = []
        for idx in similar_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                similar_conversations.append({
                    'conversation': self.conversations[idx],
                    'similarity': similarities[idx]
                })
        
        return similar_conversations
    
    def get_adaptive_response(self, user_input, base_response):
        """Get an adaptive response based on learning"""
        # Check if we have learned patterns that apply
        keywords = self.extract_keywords(user_input)
        
        for pattern_key, pattern_data in self.learned_patterns.items():
            if pattern_data['learn_type'] == 'positive':
                # If current input has similar keywords to a positively rated response
                if any(keyword in pattern_data['input_keywords'] for keyword in keywords):
                    return f"{base_response} (I've learned you might like responses like this!)"
            
            elif pattern_data['learn_type'] == 'negative':
                # Avoid responses similar to negatively rated ones
                if base_response.lower() == pattern_data['bad_response'].lower():
                    return "Let me try a different approach to answer that better."
        
        return base_response
    
    def generate_training_report(self):
        """Generate a report on training progress"""
        report = {
            "total_conversations": len(self.conversations),
            "total_feedback": len(self.feedback_data),
            "learned_patterns": len(self.learned_patterns),
            "average_rating": 0,
            "ml_model_trained": self.ml_model is not None
        }
        
        if self.feedback_data:
            ratings = [f['rating'] for f in self.feedback_data]
            report['average_rating'] = sum(ratings) / len(ratings)
        
        # Conversation topics analysis
        if self.conversations:
            all_text = ' '.join([conv['user_input'] for conv in self.conversations])
            keywords = self.extract_keywords(all_text)
            common_topics = Counter(keywords).most_common(10)
            report['common_topics'] = common_topics
        
        return report
    
    def export_training_data(self, filename="ai_bd_training_export.json"):
        """Export all training data for backup or sharing"""
        export_data = {
            "conversations": self.conversations,
            "feedback": self.feedback_data,
            "learned_patterns": self.learned_patterns,
            "export_date": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Training data exported to {filename}")
    
    def import_training_data(self, filename):
        """Import training data from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            self.conversations.extend(import_data.get('conversations', []))
            self.feedback_data.extend(import_data.get('feedback', []))
            self.learned_patterns.update(import_data.get('learned_patterns', {}))
            
            self.save_data()
            print(f"✅ Training data imported from {filename}")
            return True
        except Exception as e:
            print(f"❌ Error importing training data: {e}")
            return False

# Training data examples for quick start
def create_sample_training_data(trainer):
    """Create some sample training data to get started"""
    sample_conversations = [
        ("Hi there!", "Hello! Great to meet you! How can I help you today?"),
        ("What's your name?", "I'm AI-BD, your personal AI assistant!"),
        ("How are you?", "I'm doing great! Thanks for asking. How are you feeling today?"),
        ("Tell me a joke", "Why don't scientists trust atoms? Because they make up everything! 😄"),
        ("What can you do?", "I can chat with you, answer questions, help with various topics, and learn from our conversations!"),
        ("Help me with programming", "I'd love to help with programming! What language or concept are you working on?"),
        ("What's the weather like?", "I don't have access to real-time weather data, but I hope it's beautiful where you are!"),
        ("Thank you", "You're very welcome! I'm always happy to help! 😊"),
        ("Goodbye", "Goodbye! It was wonderful chatting with you. Come back anytime!"),
        ("Tell me about AI", "AI is fascinating! I'm an example of how technology can simulate conversation and learning.")
    ]
    
    for user_input, bot_response in sample_conversations:
        trainer.log_conversation(user_input, bot_response)
    
    # Add some sample feedback
    sample_feedback = [
        ("Hi there!", "Hello! Great to meet you! How can I help you today?", 5, "Very friendly!"),
        ("What's your name?", "I'm AI-BD, your personal AI assistant!", 4, "Clear and helpful"),
        ("Tell me a joke", "Why don't scientists trust atoms? Because they make up everything! 😄", 5, "Funny!"),
    ]
    
    for user_input, bot_response, rating, feedback in sample_feedback:
        trainer.add_feedback(user_input, bot_response, rating, feedback)
    
    print("✅ Sample training data created!")

if __name__ == "__main__":
    # Example usage
    trainer = AITrainer()
    
    # Create sample data if no conversations exist
    if len(trainer.conversations) == 0:
        print("Creating sample training data...")
        create_sample_training_data(trainer)
    
    # Generate training report
    report = trainer.generate_training_report()
    print("\n📊 Training Report:")
    for key, value in report.items():
        print(f"  {key}: {value}")
    
    # Try to train ML model
    if len(trainer.conversations) >= 10:
        trainer.train_ml_model()
    else:
        print(f"Need {10 - len(trainer.conversations)} more conversations to train ML model")
