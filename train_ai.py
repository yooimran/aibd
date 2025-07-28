"""
AI-BD Training Example
This script shows how to train your AI-BD chatbot
"""

from ai_trainer import AITrainer, create_sample_training_data

def main():
    print("🤖 AI-BD Training System")
    print("=" * 40)
    
    # Initialize trainer
    trainer = AITrainer()
    
    # Create sample data if needed
    if len(trainer.conversations) == 0:
        print("📚 Creating sample training data...")
        create_sample_training_data(trainer)
    
    # Show current stats
    report = trainer.generate_training_report()
    print("\n📊 Current Training Stats:")
    print(f"  • Conversations: {report['total_conversations']}")
    print(f"  • Feedback entries: {report['total_feedback']}")
    print(f"  • Average rating: {report['average_rating']:.1f}/5" if report['average_rating'] else "  • Average rating: No ratings yet")
    print(f"  • Learned patterns: {report['learned_patterns']}")
    print(f"  • ML Model trained: {'Yes ✅' if report['ml_model_trained'] else 'No ❌'}")
    
    # Show common topics if available
    if 'common_topics' in report and report['common_topics']:
        print(f"\n🔍 Most discussed topics:")
        for topic, count in report['common_topics'][:5]:
            print(f"  • {topic}: {count} times")
    
    # Train ML model if enough data
    print(f"\n🧠 Machine Learning Model:")
    if len(trainer.conversations) >= 10:
        print("  Training ML model...")
        success = trainer.train_ml_model()
        if success:
            print("  ✅ ML model trained successfully!")
        else:
            print("  ❌ ML model training failed")
    else:
        needed = 10 - len(trainer.conversations)
        print(f"  ⏳ Need {needed} more conversations to train ML model")
    
    # Interactive training session
    print(f"\n🎓 Interactive Training Session")
    print("You can train AI-BD by adding new conversation patterns:")
    print("(Type 'quit' to exit)")
    
    while True:
        print(f"\n" + "-" * 40)
        user_input = input("If someone says: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
            
        bot_response = input("AI-BD should respond: ").strip()
        if not bot_response:
            continue
            
        # Add as positive feedback (rating 5)
        trainer.add_feedback(user_input, bot_response, 5, "User training")
        trainer.learn_from_positive_feedback(user_input, bot_response)
        
        print("✅ Added to AI-BD's knowledge!")
        
        # Ask for rating simulation
        rating = input("Rate this response (1-5, or press Enter for 5): ").strip()
        if rating and rating.isdigit():
            rating = int(rating)
            if 1 <= rating <= 5:
                trainer.add_feedback(user_input, bot_response, rating, "Training session rating")
    
    # Final stats
    final_report = trainer.generate_training_report()
    print(f"\n📈 Final Training Stats:")
    print(f"  • Total conversations: {final_report['total_conversations']}")
    print(f"  • Total feedback: {final_report['total_feedback']}")
    print(f"  • Learned patterns: {final_report['learned_patterns']}")
    
    # Export training data
    export_choice = input("\n💾 Export training data? (y/n): ").strip().lower()
    if export_choice in ['y', 'yes']:
        filename = f"ai_bd_training_backup.json"
        trainer.export_training_data(filename)
        print(f"✅ Training data exported to {filename}")
    
    print(f"\n🎉 Training session complete!")
    print(f"Your AI-BD is now smarter and ready to chat!")

if __name__ == "__main__":
    main()
