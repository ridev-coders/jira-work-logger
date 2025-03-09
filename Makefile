# Configuration
PROJECT_NAME = jira-work-logger
GCP_PROJECT = jira-work-logger
GCP_REGION = europe-southwest1
IMAGE_NAME = gcr.io/$(GCP_PROJECT)/$(PROJECT_NAME)
TIMEOUT = 300

# Default goal
.DEFAULT_GOAL := help

.PHONY: deploy build push gcloud-deploy help logs logs-browser

# Main deployment command that runs everything
deploy: gcloud-auth build push gcloud-deploy
	@echo "🚀 Complete deployment finished successfully!"

# Check authentication status and configure project
gcloud-auth:
	@echo "🔐 Checking Google Cloud authentication..."
	@if ! gcloud auth list --format="get(account)" | grep -q "@"; then \
		echo "Not authenticated, logging in..."; \
		gcloud auth login; \
	else \
		echo "Already authenticated as $$(gcloud auth list --format='get(account)' | head -1)"; \
	fi
	@echo "Setting project to $(GCP_PROJECT)..."
	@gcloud config set project $(GCP_PROJECT)

# Build the Docker image
build:
	@echo "🏗️ Building Docker image..."
	docker build --tag $(IMAGE_NAME):latest .
	@echo "🧹 Cleaning up dangling images..."
	docker image prune -f --filter "dangling=true"
	
# Push to Google Container Registry
push:
	@echo "⬆️ Pushing to Google Container Registry..."
	docker push $(IMAGE_NAME)

# Deploy to Cloud Run
gcloud-deploy:
	@echo "🚀 Deploying to Cloud Run..."
	gcloud run deploy $(PROJECT_NAME) \
		--image $(IMAGE_NAME) \
		--platform managed \
		--region $(GCP_REGION) \
		--allow-unauthenticated \
		--timeout $(TIMEOUT)

# Show help
help:
	@echo "Available commands:"
	@echo "  make deploy         - Run complete deployment (auth, build, push, deploy)"
	@echo "  make build          - Build Docker image"
	@echo "  make push           - Push to Google Container Registry"
	@echo "  make gcloud-deploy  - Deploy to Cloud Run"
	@echo "  make gcloud-auth    - Authenticate with Google Cloud"
	@echo "  make help           - Show this help message"
	@echo "  make logs-browser   - Open logs in browser"

logs-browser:
	open "https://console.cloud.google.com/run/detail/$(GCP_REGION)/$(PROJECT_NAME)/logs?project=$(GCP_PROJECT)" 