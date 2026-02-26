# 1. Base Image
# We use the official Python 3.11 slim image based on Debian Linux.
# 'slim' strips out GUI and other unnecessary packages to reduce the attack surface and image size.
FROM python:3.13-slim

# 2. System Dependencies
# Some Python packages (like certain pandas/numpy dependencies) require C compilers to build.
# We install them, and then immediately clean up the apt cache to keep the image small.
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Working Directory
# This sets the execution context inside the container. All subsequent commands run from here.
WORKDIR /app

# 4. Dependency Installation
# We copy ONLY the requirements file first. 
# Docker caches layers. If we copy the whole app first, any change to your python code 
# would invalidate the cache and force Docker to redownload all pip packages.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Application Code
# Now we copy the rest of your project (the app folder, model_training folder, etc.) into the container.
COPY . .

# 6. Network Configuration
# This documents that the container process will listen on port 8000.
EXPOSE 8000

# 7. Execution Command
# This is the command that runs when the container starts.
# We bind Uvicorn to 0.0.0.0 so it accepts connections from outside the container's internal network.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Run the docker build using the command `docker build -t fraud-detection-api .` the -t gives the resulting file a tag
# Run the docker file `docker run -d -p 8000:8000 --name running-fraud-api fraud-detection-api` 