# Container Image
FROM ubuntu:latest

# Set Up Container
RUN apt-get update -y && apt install python3 python3-pip git -y

# Create master-of-jokes Directory
RUN mkdir master-of-jokes
WORKDIR /master-of-jokes

# Copy .whl From repository
COPY ./dist/moj-1.0.0-py2.py3-none-any.whl ./

# Install Project Dependencies
RUN pip install --no-cache-dir --break-system-packages ./moj-1.0.0-py2.py3-none-any.whl

# Starts Project
RUN flask --app moj init-db && flask --app moj run --host=0.0.0.0
