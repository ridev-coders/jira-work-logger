import requests
from datetime import datetime
import os
from typing import Optional
from dataclasses import dataclass
import json
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from config.env
env_path = Path('.') / 'config.env'
load_dotenv(dotenv_path=env_path)

@dataclass
class JiraWorklogConfig:
    email: str
    api_token: str
    jira_instance: str  # e.g., "foundever.atlassian.net"

    @classmethod
    def from_env(cls) -> 'JiraWorklogConfig':
        """Create a config instance from environment variables."""
        return cls(
            email=os.getenv('JIRA_EMAIL'),
            api_token=os.getenv('JIRA_API_TOKEN'),
            jira_instance=os.getenv('JIRA_INSTANCE', 'foundever.atlassian.net')
        )

class JiraWorklogAPI:
    def __init__(self, config: JiraWorklogConfig):
        self.config = config
        self.base_url = f"https://{config.jira_instance}"
        self.auth = (config.email, config.api_token)
    
    def log_work(
        self,
        issue_key: str,
        time_spent_minutes: int,
        start_time: Optional[datetime] = None,
        comment: str = "",
        adjust_estimate: str = "new",
        new_estimate: str = "0m"
    ) -> dict:
        """
        Log work time on a Jira issue.
        
        Args:
            issue_key: The Jira issue key (e.g., 'AI-152')
            time_spent_minutes: Time spent in minutes
            start_time: When the work started (defaults to now if not specified)
            comment: Optional comment for the worklog
            adjust_estimate: How to adjust the remaining estimate ('new', 'leave', 'manual', 'auto')
            new_estimate: New estimate when adjust_estimate is 'new'
        
        Returns:
            Response from Jira API
        """
        if start_time is None:
            start_time = datetime.now()
            
        url = f"{self.base_url}/rest/internal/3/issue/{issue_key}/worklog"
        
        params = {
            "adjustEstimate": adjust_estimate,
            "newEstimate": new_estimate
        }
        
        # Convert minutes to Jira format (e.g., "240m")
        time_spent = f"{time_spent_minutes}m"
        
        # Format the date in ISO format with timezone
        started = start_time.strftime("%Y-%m-%dT%H:%M:%S.000%z")
        if not started.endswith("+0000") and "+" not in started and "-" not in started[10:]:
            started += "+0000"

        data = {
            "timeSpent": time_spent,
            "started": started,
            "comment": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment}]
                    }
                ] if comment else []
            }
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(
            url,
            params=params,
            json=data,
            headers=headers,
            auth=self.auth
        )
        
        response.raise_for_status()
        return response.json()

def main():
    # Example usage - now using from_env() class method
    try:
        config = JiraWorklogConfig.from_env()
        api = JiraWorklogAPI(config)
        
        # Example: Log 4 hours of work
        response = api.log_work(
            issue_key="AI-152",
            time_spent_minutes=240,  # 4 hours
            comment="Development work"
        )
        print("Work logged successfully:", json.dumps(response, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error logging work: {e}")
    except Exception as e:
        print(f"Configuration error: {e}")

if __name__ == "__main__":
    main() 