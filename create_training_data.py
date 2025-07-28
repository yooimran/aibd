"""
Create Basic Training Data Structure
This creates the training data files without requiring ML libraries
"""

import os
import json
from datetime import datetime

def create_basic_training_structure():
    """Create basic training data structure"""
    
    # Define paths
    project_dir = r"c:\Users\Admin\Desktop\React projects\aiBD"
    data_dir = os.path.join(project_dir, "training_data")
    
    # Create directory
    os.makedirs(data_dir, exist_ok=True)
    print(f"📁 Created training data directory: {data_dir}")
    
    # Sample conversations
    sample_conversations = [
        {
            "timestamp": datetime.now().isoformat(),
            "user_input": "Hello",
            "bot_response": "Hello! I'm AI-BD. How can I assist you today?",
            "context": []
        },
        {
            "timestamp": datetime.now().isoformat(),
            "user_input": "What's your name?",
            "bot_response": "I'm AI-BD, your custom AI assistant!",
            "context": ["hello"]
        },
        {
            "timestamp": datetime.now().isoformat(),
            "user_input": "How are you?",
            "bot_response": "I'm doing wonderfully! As an AI, I'm always excited to learn and chat.",
            "context": ["hello", "what's your name"]
        }
    ]
    
    # Sample feedback
    sample_feedback = [
        {
            "timestamp": datetime.now().isoformat(),
            "user_input": "Hello",
            "bot_response": "Hello! I'm AI-BD. How can I assist you today?",
            "rating": 5,
            "feedback": "Very friendly greeting!"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "user_input": "What's your name?",
            "bot_response": "I'm AI-BD, your custom AI assistant!",
            "rating": 4,
            "feedback": "Clear and helpful"
        }
    ]
    
    # Sample learned patterns
    sample_patterns = {
        "good_1": {
            "input_keywords": ["hello", "hi", "hey"],
            "good_response": "Hello! I'm AI-BD. How can I assist you today?",
            "learn_type": "positive"
        },
        "good_2": {
            "input_keywords": ["name", "who", "are", "you"],
            "good_response": "I'm AI-BD, your custom AI assistant!",
            "learn_type": "positive"
        }
    }
    
    # Write files
    files_created = []
    
    # conversations.json
    conv_file = os.path.join(data_dir, "conversations.json")
    with open(conv_file, 'w', encoding='utf-8') as f:
        json.dump(sample_conversations, f, indent=2, ensure_ascii=False)
    files_created.append(f"conversations.json ({len(sample_conversations)} conversations)")
    
    # feedback.json
    feedback_file = os.path.join(data_dir, "feedback.json")
    with open(feedback_file, 'w', encoding='utf-8') as f:
        json.dump(sample_feedback, f, indent=2, ensure_ascii=False)
    files_created.append(f"feedback.json ({len(sample_feedback)} feedback entries)")
    
    # learned_patterns.json
    patterns_file = os.path.join(data_dir, "learned_patterns.json")
    with open(patterns_file, 'w', encoding='utf-8') as f:
        json.dump(sample_patterns, f, indent=2, ensure_ascii=False)
    files_created.append(f"learned_patterns.json ({len(sample_patterns)} patterns)")
    
    return files_created

def main():
    print("🚀 AI-BD Training Data Creator")
    print("=" * 40)
    print()
    
    try:
        files_created = create_basic_training_structure()
        
        print("✅ Training data structure created successfully!")
        print()
        print("📄 Files created:")
        for file_info in files_created:
            print(f"   • {file_info}")
        
        print()
        print("💡 What you can do now:")
        print("   1. Run: manage_training_data.bat (to manage data)")
        print("   2. Run: run_chatbot.bat (to start chatting)")
        print("   3. Chat with AI-BD to add more training data")
        print("   4. Use feedback buttons (👍👎) to improve responses")
        print()
        print("🎯 Next steps:")
        print("   • Install training features: install_training.bat")
        print("   • Start AI-BD: run_chatbot.bat")
        print("   • Open data folder to see the files")
        
    except Exception as e:
        print(f"❌ Error creating training data: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    input(f"\nPress Enter to {'continue' if success else 'exit'}...")
