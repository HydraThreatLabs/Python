import requests
from bs4 import BeautifulSoup

req = requests.get("http://hackthissite.org", verify=False)
html_page = BeautifulSoup(req.text, 'html.parser')
for line in html_page.find_all('script'):
    try:
        link = line.get("src")
        if link and link.endswith(".js"):
         print(link)
    except:
        print("unexcepeted error")