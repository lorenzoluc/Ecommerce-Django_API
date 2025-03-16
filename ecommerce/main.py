from api_client import get_products

products = get_products()

if products:
    print("Product:", products)