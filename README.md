# marketplace-scraper

Automated webscraper written in Python to parse through marketplace listings with the Selenium testing tool and Google Chrome webdriver. It finds listings of items that are free or that match a predefined set of keywords and sends an email containing all relevant listings obtained from the search. Compatible with ARM processors such as raspberry pi.

It is currently running in a container on a raspberry pi that runs the script every 12 hours via a cronjob

## How to run locally

Ensure python and pip are installed.

Create a python virtual environment

In project root folder run:
```bash
python -m venv venv
```

Activate the environment (linux):
```bash
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```


## How to run in container
Ensure you have Docker installed on your system. Clone the repo onto your system. Create a .env file with the variables specified in the docker-compose.yaml file and modify the volume mapping paths in the docker-compose file to suit your system. Run the following command to start a container in detached mode:

```bash
docker compose up -d
```

The volume mapping in the docker compose file allows for modifying the list of keywords without having to rebuild the image.


## Dependencies
selenium\
python-dotenv\
yagmail\
Jinja2

## TODO
### Internal
[] Error handling (send email if error)\
[] Add config file with env for dev mode (i.e ignore last scraped listing check)\
[] Store cookies for subsequent scrapes
### Dev
[] Automate message to seller\
[] Web UI to add/remove keywords via list with slider for price | Button to run manually and test manually (without saving latest scrape)

## Debugging
EoL sequence for crontab should be LF!!!!!!!!!!!!!!!!!!