# Use an official Python image
FROM python:3.11-slim

# Set environment variables to prevent Python from buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl gcc libpq-dev && \ 
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the rest of the application code
COPY . .

# Install dependencies tanpa virtualenv
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-cache

# Expose the port the app runs on
EXPOSE 8081

# Command to run the application
CMD ["python", "main.py", "serve"]
