# Use the latest stable Python base image
FROM python:3.11-slim AS build

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Use the latest stable Python base image for the final image
FROM python:3.11-slim

# # Set the working directory in the container
# WORKDIR /app

# Copy the installed dependencies from the build stage
COPY --from=build /usr/local/ /usr/local/

# Copy the application code
COPY app ./server/app

WORKDIR /server

# Set the environment variables
ENV ENVIRONMENT=production

# Expose the port the app runs on
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
