# AI-BD Chatbot Installation Guide

## Requirements
- Python 3.7 or higher
- pip (Python package installer)

## Step-by-Step Installation

1. **Clone or Download the Project**
   - Place the folder at: c:\Users\Admin\Desktop\React projects\aiBD

2. **Set Up Python Environment (Recommended)**
   - (Optional) Create a virtual environment:
     python -m venv .venv
   - Activate the environment:
     .venv\Scripts\activate

3. **Install Dependencies**
   - Run:
     pip install -r requirements.txt

4. **Start the Chatbot**
   - Run:
     python hybrid_app.py
   - Or use the batch file:
     run_chatbot.bat

5. **Access the Web Interface**
   - Open your browser and go to:
     http://localhost:5000

## Troubleshooting
- If you see errors about missing packages, re-run:
  pip install -r requirements.txt
- For Windows, make sure you have Python added to your PATH.
- For advanced features, ensure your browser supports modern JavaScript and CSS.

## Resetting Training Data
- To clear all learned responses, delete or empty:
  training_data/conversations.json
  training_data/learned_patterns.json

## Support
- For help, see README.md or contact the project author.
