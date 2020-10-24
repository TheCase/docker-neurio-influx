FROM alpine:3.12

RUN apk add --update py-pip
RUN pip install --upgrade pip
RUN pip install neurio influxdb

COPY *.py /

ENV NEURIOAPIKEY xxx
ENV NEURIOSECRET xxx

ENV INFLUXHOST localhost
ENV INFLUXPORT 8086
ENV INFLUXUSER root
ENV INFLUXPASS root
ENV INFLUXDB   neurio

# time between API hits in seconds
ENV POLL_INTERVAL 60

CMD [ "python3", "neurio-influx.py" ]
