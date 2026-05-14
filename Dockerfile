# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY  . /app

# Copy mqtt_connector from the parent folder to the /app folder -- handled by git action
COPY mqtt_connector /app/mqtt_connector

# Install pip requirements
RUN python -m pip install -r requirements.txt

# Add the mqtt_connector folder to the PYTHONPATH
ENV PYTHONPATH=/app/mqtt_connector/:$PYTHONPATH

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

RUN mkdir -p "logs"

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["python", "main.py"]
CMD ["--configfile", "configs/config-broker-evaluation.yml"]

# Run mqtt_client.py when the container launches
# ENTRYPOINT ["python", "./subscriber.py"]
# CMD ["--logfile","./testLogFile.log"]
