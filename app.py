import os
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
from jira_worklog import JiraWorklogConfig, JiraWorklogAPI
from dotenv import load_dotenv
import requests
from base64 import b64encode

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

# Initialize Jira API
jira_config = JiraWorklogConfig.from_env()
jira_api = JiraWorklogAPI(jira_config)

JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_BASE_URL = os.getenv('JIRA_BASE_URL', 'https://foundever.atlassian.net')

@app.route('/')
def index():
    """Render the calendar page."""
    return render_template('index.html')

@app.route('/api/check-credentials')
def check_credentials():
    """Check if environment credentials are configured"""
    has_env_credentials = bool(JIRA_EMAIL and JIRA_API_TOKEN)
    return jsonify({'hasEnvCredentials': has_env_credentials})

@app.route('/api/log-work', methods=['POST'])
def log_work():
    """Handle work log submissions."""
    try:
        data = request.json
        events = data.get('events', [])
        issue_key = data.get('issueKey')
        
        if not issue_key:
            return jsonify({'error': 'Issue key is required'}), 400
            
        # Get credentials (try headers first, then env variables)
        email = request.headers.get('X-Jira-Email') or JIRA_EMAIL
        token = request.headers.get('X-Jira-Token') or JIRA_API_TOKEN
        
        if not email or not token:
            return jsonify({'success': False, 'error': 'No valid credentials found'})
        
        auth = b64encode(f"{email}:{token}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json'
        }
        
        results = []
        for event in events:
            start = datetime.fromisoformat(event['start'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(event['end'].replace('Z', '+00:00'))
            
            # Calculate duration in minutes
            duration = (end - start).total_seconds() / 60
            
            try:
                response = jira_api.log_work(
                    issue_key=issue_key,
                    time_spent_minutes=int(duration),
                    start_time=start,
                    comment=event.get('comment', '')
                )
                results.append({
                    'success': True,
                    'start': event['start'],
                    'end': event['end'],
                    'response': response
                })
            except Exception as e:
                results.append({
                    'success': False,
                    'start': event['start'],
                    'end': event['end'],
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 