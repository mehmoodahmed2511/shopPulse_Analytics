CREATE DATABASE shoppulse_db;

USE shoppulse_db;

CREATE TABLE dim_user (
user_id INTEGER PRIMARY KEY,
first_name VARCHAR(100),
last_name VARCHAR (100),
age INTEGER,
gender VARCHAR (30),
email VARCHAR(100),
phone VARCHAR(30),
city VARCHAR(100),
state VARCHAR(30),
country VARCHAR(30),
department VARCHAR(100)
);

CREATE TABLE dim_category (
category_id INTEGER PRIMARY KEY,
category VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE dim_product(
product_id INTEGER PRIMARY KEY,
product_name VARCHAR(255),
category_id INTEGER,
price NUMERIC(12,2),
discount_percentage NUMERIC(6,2),
rating NUMERIC(4,2),
stock INTEGER,
brand VARCHAR(150),
sku VARCHAR(100),
availability_status VARCHAR(100),

CONSTRAINT fk_product_category
FOREIGN KEY (category_id) REFERENCES dim_category(category_id)
);

CREATE TABLE fact_cart(
cart_id INTEGER PRIMARY KEY,
user_id INTEGER,
total_products INTEGER,
total_quantity INTEGER,
line_total NUMERIC(12,2),
discounted_total NUMERIC(12,2),

CONSTRAINT fk_cart_user
FOREIGN KEY (user_id) REFERENCES dim_user(user_id)
);

CREATE TABLE fact_cart_item(
cart_id INTEGER NOT NULL,
product_id INTEGER NOT NULL,
unit_price NUMERIC(12,2),
quantity INTEGER,
line_total NUMERIC(12,2),
discounted_total NUMERIC(12,2),
discount_percentage NUMERIC(6,2),

CONSTRAINT pk_cart_item
PRIMARY KEY(cart_id, product_id),

CONSTRAINT fk_cart_item_cart
FOREIGN KEY (cart_id) REFERENCES fact_cart(cart_id),

CONSTRAINT fk_cart_item_product
FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);











