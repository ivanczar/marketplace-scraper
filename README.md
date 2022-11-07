# MarketplaceScraper
Automated webscraper written in Python to parse through marketplace listings with the Selenium testing tool to find items that are free or that match a set of keywords. The program then sends an SMS via the Twilio API containing all relevant info obtained from the search.
It is hosted on a raspberry pi within a docker container that runs the program twice a day. 
