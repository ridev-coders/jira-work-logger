import os
from flask import Flask, render_template, jsonify, request
from datetime import datetime
from jira_worklog import JiraWorklogConfig, JiraWorklogAPI
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"  # Change this in production


@app.route("/")
def index():
    """Render the calendar page."""
    return render_template("index.html")


@app.route("/api/check-credentials")
def check_credentials():
    """Check if environment credentials are configured"""
    return jsonify(
        {"hasEnvCredentials": False}
    )  # Always false since we don't use env credentials anymore


@app.route("/api/validate-credentials", methods=["POST"])
def validate_credentials():
    """Validate Jira credentials."""
    try:
        data = request.json
        email = data.get("email")
        token = data.get("token")
        instance = data.get("instance", "foundever.atlassian.net")

        if not email or not token:
            return jsonify({"valid": False, "error": "Email and token are required"})

        # Create a test config and API instance
        config = JiraWorklogConfig(email=email, api_token=token, jira_instance=instance)
        api = JiraWorklogAPI(config)

        # Try a simple request to validate credentials
        # This is a simple GET request to the myself endpoint which should work with valid credentials
        url = f"https://{instance}/rest/api/3/myself"
        response = requests.get(
            url, auth=(email, token), headers={"Accept": "application/json"}
        )

        if response.status_code == 200:
            return jsonify({"valid": True})
        else:
            return jsonify(
                {
                    "valid": False,
                    "error": f"Authentication failed: {response.status_code}",
                }
            )

    except Exception as e:
        return jsonify({"valid": False, "error": str(e)})


@app.route("/api/log-work", methods=["POST"])
def log_work():
    """Handle work log submissions."""
    try:
        data = request.json
        events = data.get("events", [])
        issue_key = data.get("issueKey")

        if not issue_key:
            return jsonify({"error": "Issue key is required"}), 400

        # Get credentials from headers
        email = request.headers.get("X-Jira-Email")
        token = request.headers.get("X-Jira-Token")
        instance = request.headers.get("X-Jira-Instance", "foundever.atlassian.net")

        if not email or not token:
            return jsonify({"success": False, "error": "No valid credentials found"})

        # Create Jira API instance with user credentials
        jira_config = JiraWorklogConfig(
            email=email, api_token=token, jira_instance=instance
        )
        jira_api = JiraWorklogAPI(jira_config)

        results = []
        for event in events:
            start = datetime.fromisoformat(event["start"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(event["end"].replace("Z", "+00:00"))

            # Calculate duration in minutes
            duration = (end - start).total_seconds() / 60

            try:
                response = jira_api.log_work(
                    issue_key=issue_key,
                    time_spent_minutes=int(duration),
                    start_time=start,
                    comment=event.get("comment", ""),
                )
                results.append(
                    {
                        "success": True,
                        "start": event["start"],
                        "end": event["end"],
                        "response": response,
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "success": False,
                        "start": event["start"],
                        "end": event["end"],
                        "error": str(e),
                    }
                )

        return jsonify({"success": True, "results": results})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    # Get port from environment variable (for Cloud Run) or use 8080 as default
    port = int(os.environ.get("PORT", 8080))
    # Enable debug mode in development
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    app.run(host="0.0.0.0", port=port, debug=debug)
