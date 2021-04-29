from python:3.9.4-slim


# create and set work dir
RUN mkdir /app
WORKDIR /app

# prepare environment [copy dependencies files, install all dependencies]
COPY requirements.txt Pipfile Pipfile.lock .
RUN pip install pipenv
RUN pipenv install --system --deploy

# copy all project
COPY . .

# set command for running
CMD ["python", "discord_weather_bot/__main__.py"]