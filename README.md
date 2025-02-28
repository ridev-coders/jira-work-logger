# Jira Worklog API

A simple Python API to log work time in Jira issues. This tool allows you to programmatically log your work hours without using the Jira web interface.

## Prerequisites

- Python 3.6 or higher
- A Jira account with API token
- Access to your Jira instance

## Setup

1. Clone this repository or download the files:
   - `jira_worklog.py`
   - `requirements.txt`
   - `config.env`

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Jira API token:
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Give it a meaningful name (e.g., "Worklog API")
   - Copy the generated token

4. Configure your credentials:
   - Copy the `config.env` file
   - Fill in your details:
     ```env
     JIRA_EMAIL=your.email@foundever.com
     JIRA_API_TOKEN=your-api-token
     JIRA_INSTANCE=foundever.atlassian.net
     ```

## Usage

### Basic Usage

Run the script directly with the example configuration:

```bash
python jira_worklog.py
```

### Using in Your Own Code

```python
from jira_worklog import JiraWorklogConfig, JiraWorklogAPI
from datetime import datetime

# Load config from environment variables
config = JiraWorklogConfig.from_env()
api = JiraWorklogAPI(config)

# Log work example
response = api.log_work(
    issue_key="PROJECT-123",      # Your Jira issue key
    time_spent_minutes=240,       # 4 hours
    comment="Development work",   # Optional comment
    start_time=datetime.now()     # Optional start time
)
```

### API Parameters

The `log_work` method accepts the following parameters:

- `issue_key` (required): The Jira issue key (e.g., 'AI-152')
- `time_spent_minutes` (required): Time spent in minutes
- `start_time` (optional): When the work started (defaults to current time)
- `comment` (optional): Comment for the worklog
- `adjust_estimate` (optional): How to adjust the remaining estimate ('new', 'leave', 'manual', 'auto')
- `new_estimate` (optional): New estimate when adjust_estimate is 'new'

## Examples

### Log 2 Hours of Work

```python
api.log_work(
    issue_key="AI-152",
    time_spent_minutes=120,  # 2 hours
    comment="Feature development"
)
```

### Log Work for a Specific Time

```python
from datetime import datetime

# Log work for a specific date/time
start_time = datetime(2024, 2, 24, 14, 0)  # 2024-02-24 14:00
api.log_work(
    issue_key="AI-152",
    time_spent_minutes=180,  # 3 hours
    start_time=start_time,
    comment="Code review and testing"
)
```

## Error Handling

The API will raise exceptions in the following cases:
- Invalid credentials or API token
- Network connectivity issues
- Invalid issue key
- Server-side errors

Example with error handling:

```python
try:
    response = api.log_work(
        issue_key="AI-152",
        time_spent_minutes=60
    )
    print("Work logged successfully!")
except requests.exceptions.RequestException as e:
    print(f"Error logging work: {e}")
```

## Security Notes

1. Never commit your `config.env` file to version control
2. Add `config.env` to your `.gitignore` file
3. Keep your API token secure and rotate it periodically
4. Use environment-specific configuration for different environments

## Contributing

Feel free to submit issues and enhancement requests! 