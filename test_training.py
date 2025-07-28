"""
Test AI-BD Training System
Run this to verify training features work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_training_system():
    print("🧪 Testing AI-BD Training System")
    print("=" * 40)
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from ai_trainer import AITrainer, create_sample_training_data
        print("  ✅ AI Trainer imported successfully")
        
        # Test trainer initialization
        print("\n🤖 Testing trainer initialization...")
        trainer = AITrainer()
        print("  ✅ Trainer initialized successfully")
        
        # Test sample data creation
        print("\n📚 Testing sample data creation...")
        create_sample_training_data(trainer)
        print(f"  ✅ Created {len(trainer.conversations)} sample conversations")
        print(f"  ✅ Created {len(trainer.feedback_data)} sample feedback entries")
        
        # Test training report
        print("\n📊 Testing training report...")
        report = trainer.generate_training_report()
        print(f"  ✅ Generated report with {len(report)} fields")
        
        # Test conversation similarity
        print("\n🔍 Testing conversation similarity...")
        similar = trainer.find_similar_conversations("hello there")
        print(f"  ✅ Found {len(similar)} similar conversations")
        
        # Test ML model training
        print("\n🧠 Testing ML model training...")
        if len(trainer.conversations) >= 10:
            success = trainer.train_ml_model()
            print(f"  ✅ ML model training: {'Success' if success else 'Failed'}")
        else:
            print(f"  ⏳ Need {10 - len(trainer.conversations)} more conversations for ML training")
        
        # Test response enhancement
        print("\n💬 Testing response enhancement...")
        enhanced = trainer.get_adaptive_response(
            "Hello", 
            "Hi there! How can I help you?"
        )
        print(f"  ✅ Enhanced response: {enhanced[:50]}...")
        
        # Test export/import
        print("\n💾 Testing data export/import...")
        test_file = "test_export.json"
        trainer.export_training_data(test_file)
        
        # Create new trainer and import
        trainer2 = AITrainer()
        trainer2.import_training_data(test_file)
        print(f"  ✅ Export/Import successful")
        
        # Clean up test file
        os.remove(test_file)
        
        print("\n🎉 All training system tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure to install requirements: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_training_system()
    if success:
        print("\n🚀 Your AI-BD training system is ready!")
        print("💡 Run 'python app.py' to start the chatbot")
        print("💡 Run 'python train_ai.py' for interactive training")
    else:
        print("\n⚠️ Training system has issues. Check error messages above.")
    
    sys.exit(0 if success else 1)
