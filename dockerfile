# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir requests python-dotenv python-telegram-bot apscheduler schedule

# Make sure you have all necessary files in the directory (e.g., autorization.py, database.py, send_message.py, and any JSON files).
# If some dependencies require system packages, you may need to install them, for example:
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Expose any necessary port if you need to access it externally
EXPOSE 8000

# Set environment variables for Docker
# ENV TELEGRAM_TOKEN=<your_telegram_token>
# ENV TELEGRAM_USERNAME=<your_telegram_username>
# ENV CHAT_ID=<your_chat_id>

ENV BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
ENV username = os.getenv('TELEGRAM_USERNAME')
ENV chat_id = os.getenv('CHAT_ID')

# Run the Python script
CMD ["python", "app.py"]
