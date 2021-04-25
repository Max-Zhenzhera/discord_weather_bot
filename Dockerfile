from python:3.9.4-slim


COPY . /app
WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "discord_weather_bot/__main__.py"]