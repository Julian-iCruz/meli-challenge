# Oficial Image for Python
FROM python:3.11-buster

# Disable the output buffer
# Errors will be displayed inmediately instead of being buffered. 
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Defined the app directory
WORKDIR /usr/src/app

# Copy local files to docker container in app directory
COPY . .

# Install the necessary app packages 
RUN python -m pip install -r requirements.txt