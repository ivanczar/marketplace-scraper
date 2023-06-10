FROM python:3.8

RUN apt-get update --allow-releaseinfo-change

RUN apt-get install chromium-driver -y

# Set display port as an environment variable
ENV DISPLAY=:99

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install cron -y

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]
