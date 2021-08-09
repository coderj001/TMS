FROM python:3.8.3-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

COPY requirements.txt requirements.txt

# install dependencies
RUN \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# copy entrypoint.sh
COPY ./entrypoint.sh .

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
