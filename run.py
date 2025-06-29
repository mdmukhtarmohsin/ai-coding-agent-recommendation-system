#!/usr/bin/env python3
"""
AI Coding Agent Recommendation System
Runner script for development and production
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import flask
        import google.generativeai
        from dotenv import load_dotenv
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("📦 Please install requirements: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path('.env')
    if not env_path.exists():
        print("⚠️  .env file not found")
        print("📝 Creating .env from template...")
        
        try:
            with open('.env.example', 'r') as template:
                with open('.env', 'w') as env_file:
                    env_file.write(template.read())
            print("✅ .env file created from template")
            print("🔑 Please add your GEMINI_API_KEY to the .env file")
        except FileNotFoundError:
            print("❌ .env.example template not found")
            return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if not gemini_key or gemini_key == 'your_gemini_api_key_here':
        print("⚠️  GEMINI_API_KEY not set in .env file")
        print("🤖 App will run with basic recommendations (without Gemini AI)")
        print("🔗 Get your key at: https://makersuite.google.com/app/apikey")
    else:
        print("✅ Gemini API key found")
    
    return True

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'recommendation_engine.py',
        'agents_db.json',
        'templates/index.html',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['templates', 'static', 'demo']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created/verified")

def run_app():
    """Run the Flask application"""
    print("🚀 Starting AI Coding Agent Recommendation System...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📱 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def main():
    """Main function to run all checks and start the app"""
    print("🧠 AI Coding Agent Recommendation System")
    print("=" * 50)
    
    # Run all checks
    if not check_requirements():
        sys.exit(1)
    
    if not check_files():
        sys.exit(1)
    
    create_directories()
    
    if not check_env_file():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    run_app()

if __name__ == "__main__":
    main() 