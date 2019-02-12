FROM nossas/bonde-dispatcher as pg-dispatcher-alpine

FROM python:alpine3.8

WORKDIR /usr/src/app

RUN apk add --no-cache --update build-base \
    postgresql-dev libressl-dev libgcc

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY --from=pg-dispatcher-alpine /usr/local/bin/pg-dispatcher /usr/local/bin/

CMD ["./run_dispatcher.sh"]
