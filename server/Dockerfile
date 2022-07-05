FROM python:3.8 as builder

WORKDIR /tmp

ENV POETRY_VERSION=1.1.13

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install poetry==$POETRY_VERSION

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.8

WORKDIR /app

COPY --from=builder /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]