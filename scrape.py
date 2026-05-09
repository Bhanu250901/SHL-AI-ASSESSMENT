import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

data = []

for a in soup.find_all("a", href=True):

    text = a.get_text(strip=True)
    link = a["href"]

    if text and "/products/" in link:

        if not link.startswith("http"):
            link = "https://www.shl.com" + link

        data.append({
            "name": text,
            "url": link
        })

df = pd.DataFrame(data)

df.drop_duplicates(inplace=True)

df.to_csv("shl_catalog.csv", index=False)

print(df.head())
print("Catalog saved")