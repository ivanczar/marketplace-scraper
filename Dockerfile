FROM selenium/standalone-chrome:latest

RUN pip3 install twilio

COPY . /home/pi/Docker/Scraper

CMD ["python3", "/home/pi/Docker/Scraper/scraper.py"]


