from dotenv import load_dotenv
import agentql
#from agentql.sync_api import ScrollDirection
import csv

load_dotenv()

PRODUCTS = """
{
    results{
        products[]{
            product_name
            product_price
            num_reviews
            rating
        }
    }
}
"""
NEXT_PAGE_BTN ="""
{
    next_page_button_enabled
    next_page_button_disabled
}
"""
session = agentql.start_session("https://www.amazon.in/iphone/s?k=iphone")

session.driver.scroll_to_bottom()

pagination = session.query(NEXT_PAGE_BTN)
print("get pagination")
print(pagination.next_page_button_enabled)


with open("products.csv", "a",newline="") as file:
    fieldnames = ["product_name","product_price","num_reviews","rating"]
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
    
    print(f"enabled button : {pagination.to_data()['next_page_button_enabled']}")
    print(f"disabled button : {pagination.to_data()['next_page_button_disabled']}")
    
    while(
        pagination.to_data()['next_page_button_enabled'] and
        pagination.to_data()['next_page_button_disabled'] is None
    ):
        products = session.query(PRODUCTS)
        print("scraped product data")
        print(products.to_data())
        
        for product in products.to_data()['results']['products']:
            print(f"product: {product}")
            writer.writerow(product)
        print("data written to csv")
        