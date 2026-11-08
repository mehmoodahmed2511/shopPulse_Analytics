
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

SELECT * FROM dim_product;

-- Products and categories
SELECT
    p.product_id,
    p.product_name,
    c.category
FROM dbo.dim_product sp
JOIN dbo.dim_category c
    ON p.category_id = c.category_id;



-- View 1 — Cart overview --
CREATE OR ALTER VIEW cart_overview AS

SELECT COUNT(cart_id) AS total_carts,
SUM(total_products) AS total_products,
SUM(total_quantity) AS total_items,
SUM(line_total) AS line_total,
SUM(line_total - discounted_total) AS total_discount,
SUM(discounted_total) AS discounted_total

FROM dbo.fact_cart;

SELECT * FROM dbo.cart_overview;


-- View 2 — Category analysis --
CREATE OR ALTER VIEW category_overview AS
SELECT 
c.category_id,
c. category,
COUNT(p.product_id) AS total_products,
SUM(p.stock) AS total_stock,
AVG(p.price) AS avg_price,
AVG(p.rating) AS avg_rating

FROM dim_category c LEFT JOIN dim_product p ON c.category_id = p.category_id GROUP BY c.category_id, c.category;

SELECT * FROM dbo.category_overview;


-- View 3 — Product performance --
CREATE OR ALTER VIEW product_performance AS
SELECT
p.product_id, 
p.product_name,
c.category,
SUM(ci.quantity) AS total_quantity,
SUM(ci.line_total) AS line_total,
SUM(ci.discounted_total) AS discounted_total,
SUM(ci.discount_percentage) AS discount_percentage
FROM dbo.fact_cart_item ci RIGHT JOIN dbo.dim_product p ON ci.product_id=p.product_id LEFT JOIN dim_category c ON p.category_id=c.category_id GROUP BY p.product_id, p.product_name, c.category;

SELECT * FROM dbo.product_performance;


-- View 4 — Customer cart details --
CREATE OR ALTER VIEW customer_cart_details AS
SELECT
u.user_id,
u.first_name,
u.last_name,
u.age,
u.gender,
u.city,
u.state,
u.country,
SUM(c.total_products) AS total_products,
SUM(c.total_quantity) AS total_quantity,
CAST(SUM(c.line_total) AS DECIMAL(20, 2)) AS line_total,
CAST(SUM(c.discounted_total) AS DECIMAL(20, 2)) AS discounted_total
FROM fact_cart c LEFT JOIN dim_user u ON u.user_id = c.user_id GROUP BY u.user_id, u.first_name, u.last_name, u.age, u.gender, u.city, u.state, u.country;

SELECT * FROM customer_cart_details;