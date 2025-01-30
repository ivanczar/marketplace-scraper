from . import run_scraper

if __name__ == "__main__":
    for data in run_scraper():
        # TODO: find a fix for this. Simulates Flask consuming
        # the stream (we need this to be able to also execute from cli)
        print(data)
