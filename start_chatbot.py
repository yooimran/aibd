#!/usr/bin/env python3
"""
AI-BD Chatbot Launcher
Run this script to start the chatbot server
"""
import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def main():
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    
    # Check if Flask is installed
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask==2.3.3", "Werkzeug==2.3.7"])
        print("✅ Flask installed successfully")
    
    # Change to the script directory
    os.chdir(script_dir)
    
    print(f"📁 Working directory: {script_dir}")
    print("🚀 Starting AI-BD Chatbot...")
    print("🧠 Training system enabled!")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📝 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start the Flask app
    try:
        # Try to open browser automatically
        import threading
        def open_browser():
            import time
            time.sleep(2)  # Wait 2 seconds for server to start
            try:
                webbrowser.open('http://localhost:5000')
                print("🌟 Browser opened automatically!")
            except:
                print("💡 Please open your browser and go to: http://localhost:5000")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n👋 Chatbot server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Make sure you're in the correct directory and all dependencies are installed")

if __name__ == "__main__":
    main()
