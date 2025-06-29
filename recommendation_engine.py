import json
import os
import google.generativeai as genai
from typing import Dict, List, Any
import re

class RecommendationEngine:
    def __init__(self):
        """Initialize the recommendation engine with Gemini AI"""
        # Configure Gemini AI
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            print("Warning: GEMINI_API_KEY not found. Gemini features will be disabled.")
            self.model = None
        
        # Load agents database
        self.agents = self._load_agents()
    
    def _load_agents(self) -> List[Dict]:
        """Load agents from the JSON database"""
        try:
            with open('agents_db.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: agents_db.json not found. Using empty agents list.")
            return []
    
    def _analyze_task_with_gemini(self, task_description: str) -> Dict[str, Any]:
        """Use Gemini AI to analyze the task and extract key information"""
        if not self.model:
            # Fallback analysis without Gemini
            return self._fallback_task_analysis(task_description)
        
        try:
            prompt = f"""
            You are a task analyzer for AI coding agent recommendations. Given this natural language input, analyze and return information in JSON format:

            Task: "{task_description}"

            Please analyze and return JSON with these fields:
            - programming_language: detected language (or "unknown" if unclear)
            - task_type: category like "bug fix", "feature development", "refactoring", "testing", "data analysis", "frontend", "backend", "devops", etc.
            - complexity: "low", "medium", or "high"
            - keywords: array of relevant technical keywords
            - domain: "web", "mobile", "data science", "machine learning", "automation", "general", etc.
            - summary: brief 1-sentence summary of the task

            Return only valid JSON, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            json_text = response.text.strip()
            if json_text.startswith('```json'):
                json_text = json_text[7:-3]
            elif json_text.startswith('```'):
                json_text = json_text[3:-3]
            
            return json.loads(json_text)
            
        except Exception as e:
            print(f"Gemini analysis failed: {e}")
            return self._fallback_task_analysis(task_description)
    
    def _fallback_task_analysis(self, task_description: str) -> Dict[str, Any]:
        """Fallback task analysis without Gemini"""
        task_lower = task_description.lower()
        
        # Simple language detection
        languages = {
            'python': ['python', 'py', 'django', 'flask', 'pandas', 'numpy'],
            'javascript': ['javascript', 'js', 'react', 'vue', 'angular', 'node'],
            'java': ['java', 'spring', 'maven', 'gradle'],
            'c++': ['c++', 'cpp', 'cmake'],
            'html': ['html', 'css', 'frontend', 'ui'],
            'sql': ['sql', 'database', 'mysql', 'postgres']
        }
        
        detected_lang = "unknown"
        for lang, keywords in languages.items():
            if any(keyword in task_lower for keyword in keywords):
                detected_lang = lang
                break
        
        # Simple task type detection
        task_types = {
            'bug fix': ['bug', 'fix', 'error', 'debug'],
            'testing': ['test', 'testing', 'unit test', 'integration'],
            'refactoring': ['refactor', 'clean up', 'optimize', 'improve'],
            'feature development': ['feature', 'implement', 'create', 'build', 'develop']
        }
        
        detected_type = "general development"
        for t_type, keywords in task_types.items():
            if any(keyword in task_lower for keyword in keywords):
                detected_type = t_type
                break
        
        return {
            'programming_language': detected_lang,
            'task_type': detected_type,
            'complexity': 'medium',
            'keywords': task_lower.split()[:5],
            'domain': 'general',
            'summary': task_description[:100] + "..." if len(task_description) > 100 else task_description
        }
    
    def _score_agent(self, agent: Dict, task_analysis: Dict) -> int:
        """Calculate agent score based on task analysis"""
        score = 0
        
        # Language match bonus
        if task_analysis['programming_language'] in [lang.lower() for lang in agent.get('supported_languages', [])]:
            score += 2
        
        # Task type match bonus
        task_type = task_analysis['task_type'].lower()
        for use_case in agent.get('ideal_use_cases', []):
            if task_type in use_case.lower() or use_case.lower() in task_type:
                score += 3
                break
        
        # Keyword matching
        keywords = [kw.lower() for kw in task_analysis['keywords']]
        agent_features = ' '.join(agent.get('features', [])).lower()
        for keyword in keywords:
            if keyword in agent_features:
                score += 1
        
        # Domain match
        domain = task_analysis['domain'].lower()
        if domain in ' '.join(agent.get('ideal_use_cases', [])).lower():
            score += 2
        
        # Complexity consideration
        complexity = task_analysis['complexity']
        if complexity == 'high' and 'enterprise' in agent.get('features', []):
            score += 1
        elif complexity == 'low' and 'beginner' in agent.get('description', '').lower():
            score += 1
        
        return max(score, 1)  # Minimum score of 1
    
    def _generate_justification_with_gemini(self, agent: Dict, task_analysis: Dict, score: int) -> str:
        """Generate natural language justification using Gemini"""
        if not self.model:
            return self._fallback_justification(agent, task_analysis, score)
        
        try:
            prompt = f"""
            Generate a concise 2-3 sentence justification for why this AI coding agent is recommended for the given task.

            Agent: {agent['name']}
            Agent Description: {agent['description']}
            Agent Features: {', '.join(agent['features'])}
            Agent Ideal Use Cases: {', '.join(agent['ideal_use_cases'])}
            Agent Supported Languages: {', '.join(agent['supported_languages'])}

            Task Analysis:
            - Programming Language: {task_analysis['programming_language']}
            - Task Type: {task_analysis['task_type']}
            - Complexity: {task_analysis['complexity']}
            - Domain: {task_analysis['domain']}
            - Summary: {task_analysis['summary']}

            Score: {score}/10

            Write a clear, specific justification explaining why this agent is well-suited for this task. Focus on concrete matches between the agent's capabilities and the task requirements.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Gemini justification failed: {e}")
            return self._fallback_justification(agent, task_analysis, score)
    
    def _fallback_justification(self, agent: Dict, task_analysis: Dict, score: int) -> str:
        """Generate fallback justification without Gemini"""
        justifications = []
        
        # Language match
        if task_analysis['programming_language'] in [lang.lower() for lang in agent.get('supported_languages', [])]:
            justifications.append(f"supports {task_analysis['programming_language']} development")
        
        # Use case match
        for use_case in agent.get('ideal_use_cases', []):
            if task_analysis['task_type'].lower() in use_case.lower():
                justifications.append(f"excels at {use_case}")
                break
        
        # General capabilities
        if agent.get('features'):
            justifications.append(f"offers {', '.join(agent['features'][:2])}")
        
        if justifications:
            return f"{agent['name']} is recommended because it " + " and ".join(justifications) + f". (Score: {score})"
        else:
            return f"{agent['name']} is a solid choice for this task with its comprehensive coding assistance features. (Score: {score})"
    
    def get_recommendations(self, task_description: str) -> Dict[str, Any]:
        """Get top 3 agent recommendations for the given task"""
        # Analyze task with Gemini
        task_analysis = self._analyze_task_with_gemini(task_description)
        
        # Score all agents
        scored_agents = []
        for agent in self.agents:
            score = self._score_agent(agent, task_analysis)
            justification = self._generate_justification_with_gemini(agent, task_analysis, score)
            
            scored_agents.append({
                'agent': agent,
                'score': score,
                'justification': justification
            })
        
        # Sort by score and get top 3
        scored_agents.sort(key=lambda x: x['score'], reverse=True)
        top_3 = scored_agents[:3]
        
        # Format recommendations
        recommendations = []
        for i, item in enumerate(top_3, 1):
            recommendations.append({
                'rank': i,
                'name': item['agent']['name'],
                'description': item['agent']['description'],
                'score': item['score'],
                'justification': item['justification'],
                'features': item['agent']['features'],
                'supported_languages': item['agent']['supported_languages'],
                'pricing': item['agent']['pricing'],
                'website': item['agent']['website']
            })
        
        return {
            'task_analysis': task_analysis,
            'agents': recommendations
        } 