import os
from flask import Flask, render_template, jsonify, request
from datetime import datetime
from jira_worklog import JiraWorklogConfig, JiraWorklogAPI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

@app.route('/')
def index():
    """Render the calendar page."""
    return render_template('index.html')

@app.route('/api/check-credentials')
def check_credentials():
    """Check if environment credentials are configured"""
    return jsonify({'hasEnvCredentials': False})  # Always false since we don't use env credentials anymore

@app.route('/api/log-work', methods=['POST'])
def log_work():
    """Handle work log submissions."""
    try:
        data = request.json
        events = data.get('events', [])
        issue_key = data.get('issueKey')
        
        if not issue_key:
            return jsonify({'error': 'Issue key is required'}), 400
            
        # Get credentials from headers
        email = request.headers.get('X-Jira-Email')
        token = request.headers.get('X-Jira-Token')
        
        if not email or not token:
            return jsonify({'success': False, 'error': 'No valid credentials found'})
        
        # Create Jira API instance with user credentials
        jira_config = JiraWorklogConfig(
            email=email,
            api_token=token,
            jira_instance='foundever.atlassian.net'
        )
        jira_api = JiraWorklogAPI(jira_config)
        
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
    app.run(host='0.0.0.0',debug=True) 