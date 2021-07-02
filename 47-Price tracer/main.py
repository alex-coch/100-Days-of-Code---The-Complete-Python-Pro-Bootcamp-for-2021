import requests
import lxml
from bs4 import BeautifulSoup
import smtplib

url = "https://www.amazon.com/Duo-Evo-Plus-esterilizadora-vaporizador/dp/B07W55DDFB/ref=sr_1_4?qid=1597660904"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(url, headers=header)

# soup = BeautifulSoup(response.content, "lxml")
soup = BeautifulSoup(response.content, "html.parser")
# print(soup.prettify())

try:
    price = soup.find(id="priceblock_ourprice").get_text()
    price_without_currency = price.split("$")[1]
    price_as_float = float(price_without_currency)
    print(price_as_float)
except:
    print("Price is not found")

title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 200

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

try:
    with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
        connection.sendmail(
            from_addr=YOUR_EMAIL,
            to_addrs=YOUR_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}"
        )
except:
    pass