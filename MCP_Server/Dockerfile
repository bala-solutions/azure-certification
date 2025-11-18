# Use official Python slim image
FROM python:3.10-slim

# Container working directory
WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app
COPY . .

# Expose HTTP port
EXPOSE 80

# Run MCP server in Streamable HTTP mode
CMD ["uvicorn", "mcp_server:app", "--host", "0.0.0.0", "--port", "80"]