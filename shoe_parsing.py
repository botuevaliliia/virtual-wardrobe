import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://us.puma.com/us/en/women/shoes/lifestyle"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

product_list = soup.find("ul", {"id": "product-list-items"})
products = product_list.find_all("li", {"data-test-id": "product-list-item"})

results = []
for item in products:
    try:
        link_tag = item.find("a", {"data-test-id": "product-list-item-link"})
        link = "https://us.puma.com" + link_tag["href"]
        title = link_tag.get("aria-label", "").strip()
        image = link_tag.find("img")["src"]
        price = item.find("span", {"data-test-id": "price"}).text.strip()

        results.append({"title": title, "price": price, "link": link, "image": image})
    except Exception as e:
        continue

df_puma = pd.DataFrame(results)
df_puma['company'] = 'Puma'


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://www.nike.com/w/womens-lifestyle-shoes-13jrmz5e1x6zy7ok"
driver.get(url)

soup = BeautifulSoup(driver.page_source, "html.parser")
cards = soup.find_all("div", class_="product-card")

results = []
for card in cards:
    title = card.find("div", class_="product-card__title").text.strip()
    price = card.find("div", class_="product-price").text.strip()
    image = card.find("img", class_="product-card__hero-image")
    img_url = image['src'] if image else "No image"
    link_tag = card.find("a", {"data-testid": "product-card__link-overlay"})
    partial_link = link_tag["href"] if link_tag else ""
    link = partial_link if partial_link.startswith("http") else f"https://www.nike.com{partial_link}"
    
    
    results.append({
            "title": title,
            "price": price,
            "link": link,
            "image": img_url
        })

driver.quit()
df_nike = pd.DataFrame(results)
df_nike['company'] = 'Nike'

df = pd.concat([df_puma, df_nike])
df = df.reset_index(drop=True)


from rembg import remove
from PIL import Image
import requests
from io import BytesIO
import os
import base64

def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

removed_images = []
for url in df.image:
    response = requests.get(url)
    input_image = Image.open(BytesIO(response.content)).convert("RGBA")
    output_image = remove(input_image)
    img_b64 = image_to_base64(output_image)
    removed_images.append(img_b64)

df['images_upd'] = removed_images


df.to_json('shoe_images.json', orient='records', indent=2)

