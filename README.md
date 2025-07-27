# AI-BD Chatbot 🤖

A unique, custom-built AI chatbot with a beautiful interface and intelligent conversation system. Built with HTML, CSS, Python Flask, and no external AI APIs!

## ✨ Features

- **Custom AI Logic**: Pattern-matching conversation system with contextual responses
- **Machine Learning Training**: Train your AI with conversation data and user feedback
- **Training Analytics**: Track performance, ratings, and learning progress
- **Interactive Teaching**: Teach AI-BD new responses through the web interface
- **Feedback System**: Rate responses to improve AI performance
- **Beautiful UI**: Modern, responsive design with multiple color themes
- **Interactive Elements**: Message suggestions, typing indicators, and smooth animations
- **Smart Responses**: Context-aware conversations that remember recent chat history
- **Unique Design**: Glass-morphism effects, floating particles, and smooth transitions
- **Multiple Themes**: Ocean, Forest, Sunset, and Default color schemes
- **Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **Keyboard Shortcuts**: Ctrl+K to focus input, Enter to send messages
- **Sound Effects**: Optional audio feedback for interactions
- **Easter Eggs**: Hidden features for fun discoveries!

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**
   ```bash
   cd "c:\Users\Admin\Desktop\React projects\aiBD"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python hybrid_app.py
   ```

4. **Open your browser and visit**
   ```
   http://localhost:5000
   ```

## 🧠 Training & Teaching

- Use the web interface to chat, give feedback, and teach new responses
- Access the Training Panel by clicking the brain icon 🧠
- Export/import training data from the Training Panel
- Reset all responses by clearing `training_data/conversations.json` and `training_data/learned_patterns.json`

## 🏗️ Project Structure

```
aiBD/
├── hybrid_app.py           # Main Flask backend with AI logic
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── QUICK_START.txt         # Quick start guide
├── INSTALLATION_GUIDE.md   # Installation instructions
├── templates/
│   └── index.html          # Main HTML template
└── static/
    ├── style.css           # CSS styles and themes
    └── script.js           # Frontend JavaScript
```

## 🔧 Advanced Usage
- Customize conversation patterns in `hybrid_app.py`
- Add new themes in `static/style.css`
- Modify AI personality in the chatbot class
- Change port in `hybrid_app.py` (`app.run(...)`)

## 🎯 Resetting Data
- To reset all responses and training data, clear:
  - `training_data/conversations.json`
  - `training_data/learned_patterns.json`

## 🤖 Technology Used
- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Design**: Custom CSS, Font Awesome, Google Fonts
- **Data Storage**: JSON files for conversations and patterns

## 📝 License
MIT License

---
**Enjoy chatting with your custom AI companion!** 🚀✨
