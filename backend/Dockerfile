
# Use the official Python 3.10.4 image as the base image
FROM python:3.10.4

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8080

# Start the backend server using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
