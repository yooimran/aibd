"""
AI-BD Training Data Manager
Manage your AI training data easily
"""

import os
import json
import shutil
from datetime import datetime

class DataManager:
    def __init__(self):
        self.project_dir = r"c:\Users\Admin\Desktop\React projects\aiBD"
        self.data_dir = os.path.join(self.project_dir, "training_data")
        self.backup_dir = os.path.join(self.project_dir, "data_backups")
        
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def show_data_location(self):
        """Show where training data is stored"""
        print("📁 AI-BD Training Data Location:")
        print(f"   {self.data_dir}")
        print()
        
        if os.path.exists(self.data_dir):
            files = os.listdir(self.data_dir)
            if files:
                print("📄 Current Data Files:")
                for file in files:
                    file_path = os.path.join(self.data_dir, file)
                    size = os.path.getsize(file_path)
                    size_str = self.format_size(size)
                    print(f"   ✓ {file} ({size_str})")
            else:
                print("   📂 Training data folder exists but is empty")
                print("   💡 Files will be created when you start training")
        else:
            print("   ⚠️ No training data directory found")
            print("   💡 Directory and files will be created automatically when you:")
            print("      • Start chatting with AI-BD")
            print("      • Use feedback buttons (👍👎)")
            print("      • Run training features")
            print()
            print("   🚀 To create training data now:")
            print("      1. Run: run_chatbot.bat")
            print("      2. Chat with AI-BD")
            print("      3. Rate some responses")
            print("      4. Training data will appear here!")
    
    def format_size(self, bytes):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"
    
    def backup_data(self):
        """Create a backup of training data"""
        if not os.path.exists(self.data_dir):
            print("❌ No training data to backup")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"ai_bd_backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            shutil.copytree(self.data_dir, backup_path)
            print(f"✅ Backup created: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def restore_data(self, backup_name=None):
        """Restore data from backup"""
        if not os.path.exists(self.backup_dir):
            print("❌ No backups found")
            return False
        
        backups = [d for d in os.listdir(self.backup_dir) 
                  if os.path.isdir(os.path.join(self.backup_dir, d))]
        
        if not backups:
            print("❌ No backup directories found")
            return False
        
        print("📋 Available Backups:")
        for i, backup in enumerate(backups, 1):
            print(f"   {i}. {backup}")
        
        if backup_name is None:
            choice = input("\nEnter backup number to restore (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return False
            
            try:
                backup_index = int(choice) - 1
                backup_name = backups[backup_index]
            except (ValueError, IndexError):
                print("❌ Invalid selection")
                return False
        
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        # Backup current data first
        if os.path.exists(self.data_dir):
            current_backup = f"before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            current_backup_path = os.path.join(self.backup_dir, current_backup)
            shutil.copytree(self.data_dir, current_backup_path)
            print(f"💾 Current data backed up to: {current_backup}")
        
        try:
            if os.path.exists(self.data_dir):
                shutil.rmtree(self.data_dir)
            shutil.copytree(backup_path, self.data_dir)
            print(f"✅ Data restored from: {backup_name}")
            return True
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False
    
    def show_data_stats(self):
        """Show training data statistics"""
        try:
            from ai_trainer import AITrainer
            trainer = AITrainer()
            report = trainer.generate_training_report()
            
            print("📊 Training Data Statistics:")
            print(f"   Conversations: {report.get('total_conversations', 0)}")
            print(f"   Feedback entries: {report.get('total_feedback', 0)}")
            print(f"   Average rating: {report.get('average_rating', 0):.1f}/5")
            print(f"   Learned patterns: {report.get('learned_patterns', 0)}")
            print(f"   ML model trained: {'Yes' if report.get('ml_model_trained') else 'No'}")
            
            if 'common_topics' in report:
                print("\n🔍 Most discussed topics:")
                for topic, count in report['common_topics'][:5]:
                    print(f"   • {topic}: {count} times")
                    
        except ImportError:
            print("⚠️ Training modules not installed")
            print("💡 Run install_training.bat to enable statistics")
        except Exception as e:
            print(f"❌ Error reading stats: {e}")
    
    def clear_data(self, confirm=True):
        """Clear all training data"""
        if confirm:
            choice = input("⚠️ This will delete ALL training data. Continue? (yes/no): ").strip().lower()
            if choice != 'yes':
                print("❌ Operation cancelled")
                return False
        
        if os.path.exists(self.data_dir):
            try:
                shutil.rmtree(self.data_dir)
                print("✅ All training data cleared")
                return True
            except Exception as e:
                print(f"❌ Clear failed: {e}")
                return False
        else:
            print("💡 No training data to clear")
            return True
    
    def export_data(self):
        """Export training data to a single file"""
        try:
            from ai_trainer import AITrainer
            trainer = AITrainer()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_bd_export_{timestamp}.json"
            filepath = os.path.join(self.project_dir, filename)
            
            trainer.export_training_data(filepath)
            print(f"✅ Data exported to: {filename}")
            return filepath
        except ImportError:
            print("⚠️ Training modules not installed")
            return None
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return None
    
    def create_sample_data(self):
        """Create sample training data for demonstration"""
        try:
            from ai_trainer import AITrainer, create_sample_training_data
            
            print("🎯 Creating sample training data...")
            trainer = AITrainer()
            create_sample_training_data(trainer)
            
            print("✅ Sample training data created!")
            print("📄 Files created:")
            print(f"   • conversations.json ({len(trainer.conversations)} conversations)")
            print(f"   • feedback.json ({len(trainer.feedback_data)} feedback entries)")
            print(f"   • learned_patterns.json ({len(trainer.learned_patterns)} patterns)")
            print()
            print("💡 You can now:")
            print("   • View training statistics (option 2)")
            print("   • Export the data (option 6)")
            print("   • Start chatting with AI-BD to add more data")
            
        except ImportError:
            print("⚠️ Training modules not installed")
            print("💡 Install training features first:")
            print("   1. Run install_training.bat")
            print("   2. Then try this option again")
        except Exception as e:
            print(f"❌ Failed to create sample data: {e}")

def main():
    manager = DataManager()
    
    while True:
        print("\n" + "="*50)
        print("🤖 AI-BD Training Data Manager")
        print("="*50)
        print("1. Show data location and files")
        print("2. Show training statistics")
        print("3. Create sample training data")
        print("4. Backup training data")
        print("5. Restore from backup")
        print("6. Export training data")
        print("7. Clear all training data")
        print("8. Open data folder")
        print("9. Quit")
        print()
        
        choice = input("Choose an option (1-9): ").strip()
        
        if choice == '1':
            manager.show_data_location()
        elif choice == '2':
            manager.show_data_stats()
        elif choice == '3':
            manager.create_sample_data()
        elif choice == '4':
            manager.backup_data()
        elif choice == '5':
            manager.restore_data()
        elif choice == '6':
            manager.export_data()
        elif choice == '7':
            manager.clear_data()
        elif choice == '8':
            os.system(f'explorer "{manager.data_dir}"')
        elif choice == '9':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
