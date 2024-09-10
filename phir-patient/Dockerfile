FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y gcc python3-dev

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-dev

# Copy application files
COPY . .

# Run the application
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
