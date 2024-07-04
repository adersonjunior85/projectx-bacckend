FROM python:3.12.2-slim-bullseye

ENV POETRY_VERSION=1.7.1

WORKDIR /app
COPY . /app/

RUN apt update
RUN pip install --upgrade pip
RUN pip install poetry==$POETRY_VERSION
RUN poetry install --no-root

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "main:get_app", "--host", "0.0.0.0", "--port", "8080"]
