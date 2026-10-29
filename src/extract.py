import pandas as pd
import requests

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

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
    
    return cart_df

extracted_products = extract_products()
extracted_users = extract_users()
extracted_carts = extract_carts()


def transform_users(extracted_users):
    users = pd.json_normalize(
        extracted_users.to_dict(orient="records")
    )
    print(f"Users Data:\n{users.head()}")
    
    dim_user = users[
        [
            "id",
        "firstName",
        "lastName",
        "age",
        "gender",
        "email",
        "phone",
        "address.city",
        "address.state",
        "address.country",
        "company.department"
        ]
    ].copy()
    
    dim_user = dim_user.rename(columns={
        "id":"user_id",
        "firstName":"first_name",
        "lastName":"last_name",
        "address.city":"city",
        "address.state":"state",
        "address.country":"country",
        "company.department":"department"
    })
    
    dim_user = dim_user.drop_duplicates(subset = ["user_id"])
    
    return dim_user


def transform_products(product_df):
    products = product_df.copy()
    
    dim_category = pd.DataFrame({
        "category" : sorted(products["category"].dropna().unique())
    })
    
    dim_category = dim_category.insert(
        range(1, len(dim_category) + 1)
    )