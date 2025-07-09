import requests
from bs4 import BeautifulSoup

def get_live_data():
    url = "https://kwgvip5.com/"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    spans = soup.select('span')
    multipliers = []
    for span in spans:
        text = span.text.replace('x', '').strip()
        try:
            value = float(text)
            multipliers.append(value)
        except:
            continue
    return multipliers[-10:]  # Return last 10 valid multipliers
