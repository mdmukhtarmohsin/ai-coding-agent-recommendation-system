# 🧠 AI Coding Agent Recommendation System

A smart web application that accepts natural language coding task descriptions and recommends the top 3 AI coding agents (GitHub Copilot, Cursor, Replit Ghostwriter, CodeWhisperer, etc.), enhanced with **Gemini AI** for intelligent task understanding and agent recommendation.

![Demo](demo/screenshot-main.png)

## ✨ Features

### 🧾 Task Input Interface

- Clean, modern web UI with natural language input
- Free-text task description with intelligent parsing
- Real-time task analysis powered by Gemini AI

### 🤖 Gemini AI Integration

- **Task Analysis**: Automatically detects programming language, task type, complexity, and domain
- **Smart Matching**: Uses AI to match tasks with ideal coding agents
- **Natural Language Justifications**: Provides human-readable explanations for recommendations

### 📚 Comprehensive Agent Database

6 AI coding agents with detailed metadata:

- **GitHub Copilot** - AI pair programmer with real-time suggestions
- **Cursor** - AI-first code editor with codebase understanding
- **Replit Ghostwriter** - Cloud-based coding assistant
- **Amazon CodeWhisperer** - ML-powered with security focus
- **Tabnine** - Privacy-first with local AI models
- **Codeium** - Free AI-powered acceleration toolkit

### 🧠 Intelligent Recommendation Engine

- **Multi-factor Scoring**: Language match, task type, domain, complexity
- **Gemini-Enhanced Reasoning**: AI-generated justifications for each recommendation
- **Fallback Logic**: Works even without Gemini API for basic recommendations

### 📊 Results Display

- Top 3 ranked agents with scores and explanations
- Detailed feature breakdown and pricing information
- Direct links to agent websites
- Beautiful, responsive UI with rank badges

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Gemini API Key (optional but recommended)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd ai-coding-agent-recommendation-system
   ```

2. **Set up Python virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env file and add your GEMINI_API_KEY
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔑 API Keys Setup

### Gemini API Key (Recommended)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

**Note**: The system works without Gemini API but provides basic recommendations. With Gemini, you get intelligent task analysis and natural language justifications.

## 📁 Project Structure

```
/agent-recommender
├── app.py                     # Flask web application
├── recommendation_engine.py   # Core logic with Gemini AI
├── agents_db.json            # Knowledge base of AI agents
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .env.example             # Environment variables template
├── templates/
│   └── index.html           # Web interface
└── demo/
    ├── screenshot-main.png  # Main interface screenshot
    ├── screenshot-results.png # Results page screenshot
    └── demo-video.mp4       # Usage demonstration
```

## 🔧 How It Works

### 1. Task Analysis (Gemini AI)

When you input a task like "Write a Python script to scrape LinkedIn job posts", Gemini AI analyzes:

- **Programming Language**: Python
- **Task Type**: Data scraping/automation
- **Complexity**: Medium
- **Domain**: Data analysis
- **Keywords**: scraping, LinkedIn, data extraction

### 2. Agent Scoring

Each agent is scored based on:

- Language support match (+2 points)
- Task domain expertise (+3 points)
- Feature relevance (+1 point each)
- Complexity handling (+1 point)

### 3. Gemini Justification

For each top agent, Gemini generates specific explanations:

> "GitHub Copilot excels at Python development and offers excellent support for web scraping tasks with its real-time code suggestions and extensive library knowledge."

## 🎯 Usage Examples

### Example 1: Web Development

**Input**: "Build a React dashboard with charts and real-time data"
**Analysis**: JavaScript, Frontend Development, Medium complexity
**Top Recommendation**: Cursor (codebase understanding) → GitHub Copilot → Replit

### Example 2: Data Science

**Input**: "Analyze customer data and create ML models in Python"
**Analysis**: Python, Machine Learning, High complexity
**Top Recommendation**: GitHub Copilot → Cursor → Tabnine

### Example 3: Bug Fixing

**Input**: "Debug performance issues in Java Spring application"
**Analysis**: Java, Bug fixing, Medium complexity
**Top Recommendation**: CodeWhisperer → GitHub Copilot → Cursor

## 🌐 API Endpoints

- `GET /` - Main web interface
- `POST /api/recommend` - Get agent recommendations
- `GET /api/agents` - List all available agents

### API Usage Example

```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"task": "Write a Python script for data analysis"}'
```

## 🛠️ Development

### Adding New Agents

Edit `agents_db.json` to add new AI coding agents:

```json
{
  "name": "New Agent",
  "description": "Description of the agent",
  "features": ["feature1", "feature2"],
  "supported_languages": ["Python", "JavaScript"],
  "ideal_use_cases": ["use case 1", "use case 2"],
  "pricing": "Pricing information",
  "website": "https://agent-website.com"
}
```

### Customizing Scoring Logic

Modify the `_score_agent` method in `recommendation_engine.py` to adjust scoring criteria.

### Extending Gemini Prompts

Update prompts in `_analyze_task_with_gemini` and `_generate_justification_with_gemini` methods.

## 🚨 Troubleshooting

### Common Issues

1. **ImportError: No module named 'google.generativeai'**

   ```bash
   pip install google-generativeai
   ```

2. **Gemini API errors**

   - Check your API key is valid
   - Ensure you have API quota available
   - Verify internet connection

3. **Template not found**

   ```bash
   mkdir templates
   # Make sure index.html is in templates/
   ```

4. **Port already in use**
   ```bash
   # Change port in app.py or kill existing process
   lsof -ti:5000 | xargs kill -9
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent task analysis
- **Bootstrap** for responsive UI components
- **Font Awesome** for beautiful icons
- **Flask** for the web framework

## 📞 Support

For issues and questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Search existing [issues](https://github.com/your-repo/issues)
3. Create a new issue with detailed description

---

**Built with ❤️ and powered by Gemini AI**
