FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install \
    net-tools telnet openssl vim procps \
    libgomp1 \
    --no-install-recommends --no-upgrade --yes \
    && apt-get clean


RUN pip install poetry

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry export -f requirements.txt --without-hashes >> requirements.txt

# python path for all python services
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PATH="${PATH}:/root/.local/bin"

RUN pip install -r requirements.txt -U

COPY some_api /app/some_api

CMD ["python3", "some_api/app.py"]

