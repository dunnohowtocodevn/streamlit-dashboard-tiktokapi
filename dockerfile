# Use official Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install additional dependencies for testing and code quality
RUN pip install pytest flake8

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8501 for Streamlit
EXPOSE 8501

# Command to run tests (optional) and then start the Streamlit app
CMD ["sh", "-c", "pytest tests/ && streamlit run main/main.py"]

