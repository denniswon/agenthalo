FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11-dev python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

RUN python3 --version

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
    libmpfr-dev \
    libhdf5-dev \
    wget \
    tar

# Copy the entire project into the container
COPY . .

# Install dependencies
RUN poetry install

COPY script.sh /script.sh
RUN chmod +x /script.sh

# Expose the port the app runs on
EXPOSE 8000

ARG BUILD_ENV=remote
ENV BUILD_ENV=${BUILD_ENV}

RUN echo "Running in ${BUILD_ENV} mode"

# Command to run the application
CMD ["/script.sh"]
