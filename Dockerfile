FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Expose port 8080 for Cloud Run
EXPOSE 8080
# Set environment variable
ENV PORT=8080
# Run the application
CMD ["python", "app.py"]