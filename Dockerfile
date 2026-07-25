FROM python:3-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Copy all application files and directories
COPY index.html /app/
COPY main.py /app/
COPY css/ /app/css/
COPY js/ /app/js/
COPY assets/ /app/assets/

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]