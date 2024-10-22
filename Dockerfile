# Need to clean this up - had to move to ubuntu:20.04 because
# weasyprint would not properly show SVG icons under 
# python:3.8-slim-buster. Using ubuntu increases the image size
# by 250 MB which is terrible. Need to get weasyprint working
# on python image
# Use Ubuntu as the base image due to WeasyPrint requirements

FROM ubuntu:20.04 AS builder
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for the build stage
RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-pip \
    gcc
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# App stage with only runtime dependencies
FROM ubuntu:20.04 AS app
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install necessary libraries and dependencies for runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    python3.8 \
    python3-pip \
    weasyprint=51-2 \
  && rm -rf /var/lib/apt/lists/*

# Copy dependencies from the builder stage
COPY --from=builder /usr/local /usr/local/
COPY . .

# Expose the default Cloud Run port
EXPOSE 8080

# Set up command to run the application
#CMD ["python3.8", "run.py"]

CMD ["python3.8", "-m", "http.server", "8080"]

