ShopPulse Analytics | End-to-End Data Engineering Project

The Business Problem
E-commerce businesses need a unified view of their product catalog, customer information, product categories, inventory, and shopping cart activity to support better business decisions.

However, when this information comes from different API resources and nested JSON structures, organizing it into a consistent, analysis-ready format can be challenging.
That's the problem I'm addressing with ShopPulse Analytics, an end-to-end data engineering and analytics project.

What I'm Building
I'm developing an ETL pipeline that:
- Extracts: Retrieves product, user, and cart data from the DummyJSON API.
- Transforms: Uses Python and Pandas to clean, structure, and transform raw JSON data into relational datasets.
- Loads: Stores the transformed data in PostgreSQL using a relational database schema with primary and foreign key relationships.
- Validates: Checks data consistency, duplicate records, missing values, and table relationships.

Current Progress
I've completed the initial ETL workflow, created five relational tables in PostgreSQL, loaded the extracted data, and verified that the database relationships are working.
The next step is to develop SQL analytics queries and build an interactive Power BI dashboard to explore product performance, category-level trends, and shopping cart patterns.
This project is helping me strengthen my practical understanding of data engineering concepts while connecting them with business intelligence.

Tech Stack: Python | Pandas | REST APIs | PostgreSQL | SQL | Power BI
I'm also planning to extend the pipeline with Apache Airflow and Docker as the project progresses.
