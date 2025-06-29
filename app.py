from flask import Flask, render_template, request, jsonify
import json
import os
from recommendation_engine import RecommendationEngine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Initialize recommendation engine
rec_engine = RecommendationEngine()

@app.route('/')
def index():
    """Main page with task input interface"""
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend_agents():
    """API endpoint to get agent recommendations"""
    try:
        data = request.get_json()
        task_description = data.get('task', '').strip()
        
        if not task_description:
            return jsonify({'error': 'Task description is required'}), 400
        
        # Get recommendations from the engine
        recommendations = rec_engine.get_recommendations(task_description)
        
        return jsonify({
            'success': True,
            'task_analysis': recommendations['task_analysis'],
            'recommendations': recommendations['agents']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/api/agents')
def get_agents():
    """API endpoint to get all available agents"""
    try:
        with open('agents_db.json', 'r') as f:
            agents = json.load(f)
        return jsonify({'success': True, 'agents': agents})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 