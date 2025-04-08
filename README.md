# Jira Work Logger

A web-based calendar application for logging work hours to Jira issues. Built with Flask, FullCalendar, and Bootstrap.

## Features

### Calendar Interface
- Interactive weekly calendar view
- Customizable working hours and days
- Visual distinction between submitted and unsubmitted time slots
- Resize time slots by dragging edges
- Delete unsubmitted time slots with one click
- Real-time summary of selected time slots

### Time Management
- Set custom start and end times for working hours
- Configure working days (e.g., Monday to Friday)
- 30-minute time slot intervals
- Today indicator and business hours highlighting
- Automatic time zone handling

### Jira Integration
- Direct work log submission to Jira issues
- Secure credential management
- Support for Jira API tokens
- Visual confirmation of successful submissions
- Links to Jira issues for quick access

### User Settings
- Remember working hours preferences
- Optional credential storage (session or persistent)
- Developer mode for advanced features
- Clear all functionality for stored data

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access the application at `http://localhost:8080`

## Running Locally with Docker

1. Build the container image:
```bash
docker build -t jira-work-logger .
```

2. Run the container:
```bash
docker run --rm -p 8080:8080 jira-work-logger
```

3. Access the application at `http://localhost:8080`

## Deployment to Google Cloud Run

### Prerequisites

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Make sure Docker is installed on your machine

### Using Make Commands (Recommended)

This project includes a Makefile with commands to simplify the deployment process:

```bash
# Authenticate with Google Cloud
make gcloud-auth

# Deploy the application (includes authentication, building, pushing, and deploying)
make deploy

# Build the Docker image only
make build

# Push the Docker image to Container Registry only
make push

# Deploy to Cloud Run only
make gcloud-deploy

# Open logs in browser
make logs-browser

# Show all available commands
make help
```

### Manual Deployment Steps

If you prefer to deploy manually or understand the process:

1. **Authenticate with Google Cloud:**

   ```bash
   gcloud auth login
   gcloud config set project jira-work-logger
   ```

2. **Build the Docker image:**

   ```bash
   docker build --tag gcr.io/jira-work-logger/jira-work-logger:latest .
   ```

3. **Push the image to Google Container Registry:**

   ```bash
   docker push gcr.io/jira-work-logger/jira-work-logger
   ```

4. **Deploy to Cloud Run:**

   ```bash
   gcloud run deploy jira-work-logger \
     --image gcr.io/jira-work-logger/jira-work-logger \
     --platform managed \
     --region europe-southwest1 \
     --allow-unauthenticated \
     --timeout 300
   ```

5. **View the deployment:**

   After deployment, Cloud Run will provide a URL where your application is available.

## Usage

### First Time Setup
1. Click "Manage Credentials" to enter your Jira credentials:
   - Jira email address
   - API token (get it from [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens))
   - Choose whether to remember credentials

### Logging Work
1. Select time slots on the calendar by clicking and dragging
2. Enter the Jira issue key (e.g., "AI-152")
3. Click "Submit Work Logs" to sync with Jira
4. View confirmation and access the issue directly through provided links

### Managing Time Slots
- Resize: Drag the top or bottom edge of any unsubmitted time slot
- Delete: Click the "×" button on any unsubmitted time slot
- Clear: Use "Clear Unsubmitted" to remove all unsubmitted slots
- Developer Mode: Enable to access additional clearing options

### Customizing Calendar
- Set working hours using the start and end time inputs
- Select working days using the start and end day dropdowns
- Settings are automatically saved and persisted

## Security
- Credentials can be stored in browser storage (optional)
- API tokens are used instead of passwords
- Secure communication with Jira API
- No server-side credential storage

## Technical Details
- Frontend: HTML5, JavaScript, Bootstrap 5, FullCalendar 5
- Backend: Flask, Python
- Authentication: Jira API tokens
- Storage: Browser localStorage/sessionStorage
- Calendar: FullCalendar with time grid view

## Browser Support
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Notes
- Time slots are minimum 30 minutes
- All times are handled in the user's local timezone
- Submitted work logs cannot be modified through the interface
- Clear browser data to reset all settings and stored credentials