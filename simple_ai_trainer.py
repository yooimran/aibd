import json
import os
import re
from datetime import datetime
from collections import Counter
import pickle

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
        if feedback == 'good':
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
        """Get a response based on learned patterns"""
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
        
        # Count feedback
        positive_feedback = sum(1 for conv in self.conversations if conv.get('feedback') == 'good')
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
            if conv.get('feedback') == 'good':
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

# Test the trainer
if __name__ == "__main__":
    trainer = SimpleAITrainer()
    
    # Test conversation logging
    trainer.log_conversation("Hello", "Hi there!", "good")
    trainer.log_conversation("How are you?", "I'm doing well, thanks!", "good")
    trainer.log_conversation("What's the weather?", "I don't have weather data.", "bad")
    
    # Get stats
    stats = trainer.get_training_stats()
    print("Training Stats:", stats)
    
    # Test learned response
    response = trainer.get_learned_response("Hello there")
    print("Learned response:", response)
    
    # Train model
    trainer.train_simple_model()
