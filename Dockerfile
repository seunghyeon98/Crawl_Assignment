# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt-get update \
    && apt-get install -y gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install any dependencies needed for your script
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run on container start
CMD ["python", "run_crawling.py"]