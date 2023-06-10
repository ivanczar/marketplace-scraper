# MarketplaceScraper

Automated webscraper written in Python to parse through marketplace listings with the Selenium testing tool and Google Chrome webdriver. It finds listings of items that are free or that match a predefined set of keywords and sends an email containing all relevant listings obtained from the search.

It is currently running in a container on a raspberry pi that runs the script every 12 hours via a cronjob

## ARM64
To run on an ARM processor (such as a raspberry pi), refer to the "ARM64" branch. Google Chrome doesnt support ARM processors so we need to use Chromium-driver instead.
