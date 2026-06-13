FROM python:3.14-alpine

COPY ./requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

ENV QBITTORRENT_SERVER=localhost
ENV QBITTORRENT_PORT=8080
ENV QBITTORRENT_USER=admin
ENV QBITTORRENT_PASS=adminadmin
ENV PORT_FORWARDED=tmp/gluetun/forwarded_port
ENV HTTP_S=http
ENV SLEEP_TIME_SEC=5

COPY ./check.py ./check.py
RUN chmod 770 ./check.py

CMD ["python3", "./check.py"]
