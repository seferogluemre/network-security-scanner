import requests
from bs4 import BeautifulSoup

url = "https://seferogluemre.vercel.app/"
response=requests.get(url)

soup=BeautifulSoup(response.text,"html.parser")

headlines=soup.find_all('h2')

print("Scraping Script Started....")

for h in headlines[:10]:
    print("-",h.text.strip())