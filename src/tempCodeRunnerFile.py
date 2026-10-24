import pandas as pd
import requests

base_url = "https://dummyjson.com"

def extract_products():
    url = f"{base_url}/products"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    product_df = pd.DataFrame(data["products"])
    
    print(f"Products Data:\n{product_df.info()}")
    
    return product_df


def extract_users():
    url = f"{base_url}/users"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    user_df = pd.DataFrame(data["users"])
    
    print(f"Users Data:\n{user_df}")
    
    return user_df


def extract_carts():
    url = f"{base_url}/carts"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    cart_df = pd.DataFrame(data["carts"])
    
    print(f"Carts Data\n{cart_df}")

extract_products()
extract_users()
extract_carts()

