# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir pytest pytest-html tstl coverage

# Command to run tests and generate reports
CMD ["bash", "-c", "pytest --html=unit_test_report.html --self-contained-html && tstl inventory.py.tstl.py --test-time 10 && coverage run -m pytest && coverage html"]
