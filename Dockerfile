# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Intall any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app when the container launches
CMD ["python", "manage.py", "runserver"]

# Set proxy server
#ENV http_proxy 0.0.0.0:5000
#ENV https+proxy 0.0.0.0:5000
