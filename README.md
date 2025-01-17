# sale-products-extractor
Product Scraper
This project uses Selenium and BeautifulSoup to scrape product information from a specific webpage. The script automatically scrolls through the page to load all content, extracts relevant product details, and saves the data in a structured JSON format. It is particularly designed to scrape promotions and sale items, including product names, prices, sale statuses, links, and images.

Features
Automatically scrolls the webpage to load all products.
Extracts detailed product information including:
Name
Original price
Discounted price
Sale status
Product link
Product image URL
Saves the extracted data in a well-formatted JSON file.
Can be easily modified to scrape other websites by adjusting the URL and element selectors.
Requirements
Python 3.x
Selenium
BeautifulSoup4
WebDriver Manager
Setup
Install the required dependencies using pip:
bash
Copiar
Editar
pip install selenium beautifulsoup4 webdriver-manager
Download the appropriate ChromeDriver version using webdriver-manager (this is handled automatically by the script).

Run the script with the desired URL to start scraping.

bash
Copiar
Editar
python product_scraper.py
The product data will be saved in a folder called ProductsOnSale, in a file named all_products.json.

Customization
You can adjust the script to scrape other types of products or websites by modifying the url and changing the HTML element selectors in the parse_products function.

This README provides a concise overview of the project and how to use it. Feel free to modify it further based on additional details or customizations.
