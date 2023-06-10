FROM python:3.8

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

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


# COPY cronjob /etc/cron.d/crontab
# RUN chmod 0644 /etc/cron.d/crontab
# RUN /usr/bin/crontab /etc/cron.d/crontab
# CMD ["cron", "-f"]

# COPY ./cronjob /etc/cron.d/container_cronjob
# COPY ./script.sh /script.sh
# RUN chmod +x /script.sh

# CMD [“/bin/bash”, “-c”, “/script.sh && chmod 644 /etc/cron.d/container_cronjob && cron && tail -f /var/log/cron.log”]
# CMD ["python", "./scraper.py"]