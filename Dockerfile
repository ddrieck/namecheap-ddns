FROM frolvlad/alpine-python3

WORKDIR /opt/namecheap-ddns
COPY . .

RUN pip install -r requirements.txt

COPY ddns-cron /etc/crontabs/ddns-cron
RUN chmod 0644 /etc/crontabs/ddns-cron
RUN crontab /etc/crontabs/ddns-cron

CMD ["crond", "-f"]