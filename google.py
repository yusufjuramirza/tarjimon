import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import logging

RETRY_DELAY = 1  # adjust this as necessary
RETRY_ATTEMPTS = 10  # adjust this as necessary


def chunk(s: str) -> list[str]:
    completions = []
    while len(s) > 5000:
        cut_index = 0
        for i in range(5000, -1, -1):
            if s[i] in [' ', '\n', '\t', '\r']:
                cut_index = i
                break
        completions.append(s[:cut_index])
        s = s[cut_index:]
    completions.append(s)
    return completions


def translate(q: str) -> str:
    qs = chunk(q)  # splitting the string into a list of characters

    i = 0
    while i < len(qs):
        retry_delay = RETRY_DELAY
        attempts = 0

        while True:
            attempts += 1
            try:
                resp = requests.get(f"https://translate.google.com/m?sl=en&tl=uz&q={quote(qs[i])}")
            except Exception as e:
                logging.error(f"Can't do request: {e}")
                return " ".join(qs)
            if resp.status_code != 200:
                logging.error(f"Bad status: {resp.status_code}")
                if attempts < RETRY_ATTEMPTS:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    return " ".join(qs)

            soup = BeautifulSoup(resp.text, 'html.parser')
            result_container = soup.find('div', {'class': 'result-container'})

            if result_container is None:
                logging.error("Not found")
                return " ".join(qs)

            qs[i] = result_container.text

            break  # break the while loop if the request is successful and result is found
        i += 1
    return " ".join(qs)