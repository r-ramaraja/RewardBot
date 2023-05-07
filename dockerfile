# set base image
FROM python:3.8-slim-bullseye

# set the working directory in the container
WORKDIR /code

# copy the content of the local src directory to the working directory
COPY . .

# install dependencies
RUN pip install -r requirements.txt

# command to run on container start
CMD [ "gunicorn", "app:flask_app" ]
