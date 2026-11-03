import pandas as pd
import requests

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

base_url = "https://dummyjson.com"

# extracting products from API
def extract_products():
    url = f"{base_url}/products"
    response = requests.get(url, params={"limit":0}, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    product_df = pd.DataFrame(data["products"])
    
    print(f"Products Data:\n{product_df}")
    
    return product_df

#extracting users from API
def extract_users():
    url = f"{base_url}/users"
    response = requests.get(url, params={"limit":0}, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    user_df = pd.DataFrame(data["users"])
    
    print(f"Users Data:\n{user_df}")
    
    return user_df

# extracting carts from API
def extract_carts():
    url = f"{base_url}/carts"
    response = requests.get(url, params={"limit":0}, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    cart_df = pd.DataFrame(data["carts"])
    
    print(f"Carts Data\n{cart_df}")
    
    return cart_df

extracted_products = extract_products()
extracted_users = extract_users()
extracted_carts = extract_carts()


# transforming data for USER, PRODUCT, CATEGORY, CART, and CART_ITEM table to put in database:

# transforming users data 
def transform_users(user_df):
    users = pd.json_normalize(
        user_df.to_dict(orient="records")
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

# transforming products and categories data
def transform_products(product_df):
    products = product_df.copy()
    
    dim_category = pd.DataFrame({
        "category" : sorted(products["category"].dropna().unique())
    })
    
    dim_category.insert(
        0, "category_id",
        range(1, len(dim_category) + 1)
    )
    
    products = products.merge(
        dim_category,
        on = "category",
        how = "left",
        validate = "many_to_one"
    )
    
    dim_product = products[
        [
            "id",
            "title",
            "category_id",
            "category",
            "price",
            "discountPercentage",
            "rating",
            "stock",
            "brand",
            "sku",
            "availabilityStatus",
        ]
    ].copy()
    
    dim_product = dim_product.rename(columns={
        "id":"product_id",
        "title":"product_name",
        "discountPercentage":"discount_percentage",
        "availabilityStatus":"availability_status"
    })
    
    dim_product = dim_product.drop_duplicates(subset=["product_id"])
    
    return dim_product, dim_category

# transforming carts and cart_items data
def transform_carts(cart_df):
    fact_cart = pd.DataFrame({
        "cart_id" : cart_df["id"],
        "user_id" : cart_df["userId"],
        "total_products" : cart_df["totalProducts"],
        "total_quantity" : cart_df["totalQuantity"],
        "line_total" : cart_df["total"],
        "discounted_total" : cart_df["discountedTotal"]
    })
    
    cart_records = cart_df.to_dict(orient = "records")
    
    item_records = []
    
    for cart in cart_records: 
        for item in cart["products"]:
            item_records.append({
                "cart_id" : cart["id"],
                "product_id" : item["id"],
                "unit_price" : item["price"],
                "quantity" : item["quantity"],
                "line_total" : item["total"],
                "discounted_total" : item["discountedTotal"],
                "discount_percentage" : item["discountPercentage"]
            })
            
    fact_cart_item = pd.DataFrame(item_records)
            
    return fact_cart, fact_cart_item
    
dim_user = transform_users(extracted_users)
dim_product, dim_category = transform_products(extracted_products)
fact_cart, fact_cart_item  = transform_carts(extracted_carts) 
        
# storing tables in a single variable to access them easily
transformed_tables = {
    "dim_user" : dim_user,
    "dim_product" : dim_product,
    "dim_category" : dim_category,
    "fact_cart" : fact_cart,
    "fact_cart_item" : fact_cart_item
}
# checking transformation results
for table_name, df in transformed_tables.items():
    print(f"\n---{table_name}---")
    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())
    print("Missing values:", df.isnull().sum())
    print("Duplicated Rows:", df.duplicated().sum())
    print(df.head(3))    
    
    
print("Product columns:", dim_product.columns.tolist())
print("Cart item columns:", fact_cart_item.columns.tolist())
    
print(f"cart users missing from dim_user:", (~fact_cart["user_id"].isin(dim_user["user_id"])).sum())
print(f"cart products missing from dim_product:", (~fact_cart_item["product_id"].isin(dim_product["product_id"])).sum())

print(extracted_carts.columns.to_list())

# checking primary keys uniqueness
print(f"Duplicated User IDs:", dim_user["user_id"].duplicated().sum())
print(f"Duplicated Product IDs:", dim_product["product_id"].duplicated().sum())
print(f"Duplicated category IDs:", dim_category["category_id"].duplicated().sum())
print(f"Duplicated Cart IDs:", fact_cart["cart_id"].duplicated().sum())
print(f"Duplicated Cart Item IDs:", fact_cart_item.duplicated(subset = ["cart_id", "product_id"]).sum())

# checking all foreign keys have matching parents records
print("Invalid Product Categories:", (~dim_product["category_id"].isin(dim_category["category_id"])).sum())
print("Invalid Cart references:", (~fact_cart["cart_id"].isin(fact_cart_item["cart_id"])).sum())

# cheking if the user_id exists in carts, then we will use it as a Foreign Key
print(extracted_carts.columns.tolist())