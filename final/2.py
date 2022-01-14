import requests
from bs4 import BeautifulSoup

response = requests.get("https://iot.cpe.ku.ac.th/daq/task2/data/26")
soup = BeautifulSoup(response.text, "html.parser")

athlete_name = [s.text.strip() for s in soup.select("td:nth-of-type(2)")]

country = [s.text.strip() for s in soup.select("td:nth-of-type(3)")]

sport = [s.text.strip() for s in soup.select("td:nth-of-type(1)")]

gold = [int(s.text.replace(",","")) for s in soup.select("td:nth-of-type(4)")]

silver = [int(s.text.replace(",","")) for s in soup.select("td:nth-of-type(5)")]

bronze = [int(s.text.replace(",","")) for s in soup.select("td:nth-of-type(6)")]

for at,coun,spo,go,sil,bro in zip(athlete_name,country,sport,gold,silver,bronze):
    print(f"{at} : {coun} : {spo} : {go} : {sil} : {bro}")
  