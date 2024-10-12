FROM python:3.11-slim

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1 

ENV HOME=/home/lorax
ENV APP_HOME=/home/lorax/trees

# create a directory for the app
RUN mkdir -p $APP_HOME

# Create an app user with a memorable GUID
RUN addgroup --gid 2012 treemen 
RUN adduser --system --ingroup treemen lorax

# Set the working directory in the container
WORKDIR $APP_HOME

# Update the package list
RUN apt update && apt upgrade -y

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements_docker.txt $APP_HOME
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir --upgrade -r requirements_docker.txt

# Get project files
COPY ./app $APP_HOME
COPY ./utils/model_state.py $APP_HOME

# Chown all the files to the app user
RUN chown -R lorax:treemen $APP_HOME

# Switch the user
USER lorax
