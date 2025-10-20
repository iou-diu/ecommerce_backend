# Use a specific version of the python image for consistency
FROM python:3.11-slim-bullseye

# Set environment variables to prevent bytecode generation and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    cargo \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Run the collectstatic command during build
RUN python manage.py collectstatic --noinput

# Apply database migrations during container startup
CMD ["sh", "-c", "python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
