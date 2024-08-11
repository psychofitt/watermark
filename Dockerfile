# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
ENV IMGBB_API_KEY=${IMGBB_API_KEY}

# Run the bot
CMD ["python", "bot.py"]
