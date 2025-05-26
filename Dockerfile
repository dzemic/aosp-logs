FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set environment port for Cloud Run
ENV PORT=8080

# Start the server
CMD ["python", "main.py"]

