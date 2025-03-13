# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables

# Prevent Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# disables buffering on stdout. Useful for seeing logging messages in
# Docker logs, but it comes at a performance cost
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /

# Install Poetry
RUN pip install --no-cache-dir poetry

# Add Poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
    libmpc-dev \
    libgmp-dev \
    libmpfr-dev

# Copy the entire project into the container
COPY . .

# Install dependencies
RUN poetry install

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "python", "-m", "fastapi"]
