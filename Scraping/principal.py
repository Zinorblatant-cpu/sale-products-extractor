from bs4 import BeautifulSoup
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


# Function to automatically scroll the webpage to load all content
def auto_scroll(driver):
    total_height = 0  # Tracks the total height scrolled
    distance = 100  # Scroll distance per step
    scroll_pause_time = 0.1  # Pause time between scrolls

    while True:
        # Execute JavaScript to scroll the page
        driver.execute_script(f"window.scrollBy(0, {distance});")
        total_height += distance
        time.sleep(scroll_pause_time)
        # Get the total height of the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Stop scrolling if the bottom of the page is reached
        if total_height >= scroll_height - driver.execute_script("return window.innerHeight;"):
            break


# Function to extract product information from the webpage
def parse_products(driver):
    all_products = []  # List to store all product data
    html_content = driver.page_source  # Get the HTML content of the current page
    soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML using BeautifulSoup

    # Find all promotion sections
    promotions = soup.find_all('div', class_='vtex-search-result-3-x-gallery')
    for promotion in promotions:
        # Find all product items within each promotion section
        products = promotion.find_all('div', class_='vtex-search-result-3-x-galleryItem')
        for product in products:
            # Extract product details
            name_tag = product.find('span', class_='vtex-product-summary-2-x-productBrand')
            name = name_tag.text.strip() if name_tag else "Name not found"
            original_price_tag = product.find('span', class_='vtex-product-price-1-x-listPriceValue strike')
            original_price = original_price_tag.text.strip() if original_price_tag else "This product is not on sale"
            on_sale_tag = product.find('div', class_='vtex-store-components-3-x-discountInsideContainer t-mini white absolute right-0 pv2 ph3 bg-emphasis z-1')
            on_sale = on_sale_tag.text.strip() if on_sale_tag else "On sale not found"
            price_tag = product.find('p', class_='cea-cea-store-theme-2-x-spotPriceShelf__price')
            price = price_tag.text.strip() if price_tag else "Price not found"
            link_tag = product.find('a', href=True)
            link = link_tag['href'] if link_tag else "Link not found"
            img_tag = product.find('img')
            img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'Img not found'

            # Store the product data in a dictionary
            product_data = {
                'name': name,
                'original_price': original_price,
                'On Sale': on_sale,
                'price': price,
                'link': link,
                'img': img_url
            }
            all_products.append(product_data)  # Add the product data to the list
    return all_products


if __name__ == '__main__':
    # Initialize the Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # URL of the webpage to scrape
    url = 'https://www.cea.com.br/ofertas/liquida/vestidos'
    driver.get(url)  # Open the URL in the browser

    # Scroll through the page to load all products
    auto_scroll(driver)

    # Extract product data from the page
    products = parse_products(driver)

    # Close the browser
    driver.quit()

    # Create a directory to save the JSON file
    output_dir = "ProductsOnSale"
    os.makedirs(output_dir, exist_ok=True)

    # Save all product data to a single JSON file
    output_file = os.path.join(output_dir, 'all_products.json')
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(products, json_file, ensure_ascii=False, indent=4)

    # Print confirmation message
    print(f"All products saved to {output_file}")
