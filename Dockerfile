FROM python:3.12-slim

# Install system dependencies for Tkinter and Xvfb (for headless GUI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    xvfb \
    curl \
    ca-certificates \
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

# Expose Ollama default port
EXPOSE 11434

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
# Default serial port inside container (user should map this)
ENV CNC_SERIAL_PORT=/dev/ttyUSB0

# Create a script to start Ollama, Xvfb, and the bot
RUN echo '#!/bin/bash\n\
# Start Xvfb for headless Tkinter support\n\
Xvfb :99 -screen 0 1024x768x16 &\n\
\n\
# Start Ollama server in background\n\
ollama serve &\n\
sleep 5\n\
\n\
# Ensure model is available\n\
ollama pull qwen2.5:0.5b\n\
\n\
# Start the CNC Controller bot\n\
python main_auto.py' > /app/start.sh && chmod +x /app/start.sh

# Default command
CMD ["/app/start.sh"]