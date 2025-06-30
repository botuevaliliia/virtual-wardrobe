import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from rembg import remove
from PIL import Image
import requests
from io import BytesIO
import os
import base64
from selenium.webdriver.common.by import By
import time

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




options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://us.supreme.com/collections/t-shirts")
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

items = soup.find_all("li", class_="sc-2s21k7-3")
products = []

for item in items:
    try:
        link_tag = item.find("a")
        title = item.find("span", {"aria-label": False}).text.strip()
        price = item.find("span", {"aria-label": "product price"}).text.strip()
        link = "https://us.supreme.com" + link_tag["href"]
        img_tag = item.find("img")
        image_url = "https:" + img_tag["src"] if img_tag and img_tag.get("src") else None

        products.append({
            "title": title,
            "price": price,
            "link": link,
            "image": image_url
        })
    except Exception as e:
        print("Error parsing item:", e)

df_supreme = pd.DataFrame(products)


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("https://www.stussy.com/collections/pants")
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

items = soup.find_all("li", class_="collection-grid__grid-item")
products = []

for item in items:
    try:
        product = item.find("div", class_="product-card")
        title = product.find("a", class_="product-card__title-link").text.strip()
        relative_link = product.find("a", class_="product-card__title-link")["href"]
        link = "https://www.stussy.com" + relative_link
        image_tag = product.find("div", class_="product-card__image--featured").find("img")
        image = "https:" + image_tag["src"] if image_tag else None
        price_tag = product.find("span", class_="product-card__price-sold-out")
        price = price_tag.text.strip() if price_tag else "Available"

        products.append({
            "title": title,
            "price": price,
            "link": link,
            "image": image
        })
    except Exception as e:
        print("Error parsing item:", e)

df_stussy = pd.DataFrame(products)


options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

url = "https://kangol.com/collections/top-sellers"
driver.get(url)
time.sleep(5) 

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

products = []
items = soup.find_all("li", class_="ns-product")
for item in items:
    try:
        title = item.find("a", class_="text-black no-underline ns-prod-link prodName").text.strip()
        link = item.find("a", class_="ns-prod-link")["href"]
        full_link = link if link.startswith("http") else f"https://kangol.com{link}"
        price = item.find("span", class_="text-black ns-price").text.strip()
        image = item.find("img")["src"]
        
        products.append({
            "title": title,
            "price": price,
            "link": full_link,
            "image": image
        })
    except Exception as e:
        print("Error parsing item:", e)

df_kangol = pd.DataFrame(products)


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://wearebraindead.com/collections/accessories"
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

products = []
items = soup.find_all("div", class_="_product-card")

for item in items:
    try:
        link_tag = item.find("a", href=True)
        link = "https://wearebraindead.com" + link_tag["href"]
        title = link_tag["aria-label"]
        image = "https:" + link_tag.find("img")["src"]
        price_tag = item.find("div", class_="_product__price")
        price = price_tag.text.strip().replace("\n", "") if price_tag else "N/A"

        products.append({
            "title": title,
            "price": price,
            "link": link,
            "image": image
        })
    except Exception as e:
        print("Error parsing item:", e)

df_acces = pd.DataFrame(products)


df = pd.concat([df_puma, df_nike])
df = df.reset_index(drop=True)
df['cloth'] = 'Shoes'
df_acces['company'] = 'BrainDead'
df_kangol['company'] = 'Kangol'
df_stussy['company'] = 'Stussy'
df_supreme['company'] = 'Supreme'
df_acces['cloth'] = 'Accessories'
df_kangol['cloth'] = 'Hat'
df_stussy['cloth'] = 'Pants'
df_supreme['cloth'] = 'Tees'
df_new = pd.concat([df_acces, df_kangol, df_stussy, df_supreme])


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

removed_images = []
for url in df_new.image:
    response = requests.get(url)
    input_image = Image.open(BytesIO(response.content)).convert("RGBA")
    output_image = remove(input_image)
    img_b64 = image_to_base64(output_image)
    removed_images.append(img_b64)
df_new['images_upd'] = removed_images

df_combined = pd.concat([df, df_new])
df_combined = df_combined.reset_index(drop=True)

df_combined[df_combined.cloth=='Shoes'].to_json('shoe_images.json', orient='records', indent=2)
df_combined[df_combined.cloth=='Hat'].to_json('hat_images.json', orient='records', indent=2)
df_combined[df_combined.cloth=='Tees'].to_json('tee_images.json', orient='records', indent=2)
df_combined[df_combined.cloth=='Pants'].to_json('pants_images.json', orient='records', indent=2)
df_combined[df_combined.cloth=='Accessories'].to_json('acces_images.json', orient='records', indent=2)

df.to_json('shoe_images.json', orient='records', indent=2)

