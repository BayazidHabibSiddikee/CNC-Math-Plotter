FROM python:3.11-slim

# Install system dependencies for Tkinter and OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    tk-dev \
    python3-tk \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy application files
COPY . .

# Pre-download the qwen2.5:0.5b model
RUN ollama pull qwen2.5:0.5b

# Expose necessary ports
# Telegram bot uses outgoing connections (no port needed)
# Ollama default port
EXPOSE 11434

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Create a script to start both Ollama and the bot
RUN echo '#!/bin/bash\n\
# Start Ollama server in background\n\
ollama serve &\n\
sleep 3\n\
# Start the CNC Controller bot\n\
python main_auto.py' > /app/start.sh && chmod +x /app/start.sh

# Default command
CMD ["/app/start.sh"]