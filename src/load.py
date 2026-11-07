import os
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")

connection_url = URL.create(
    "mssql+pyodbc",
    host=DB_SERVER,
    database=DB_NAME,
    query={
        "driver": DB_DRIVER,
        "Trusted_Connection": "yes"
    }
)

engine = create_engine(
    connection_url,
    fast_executemany=True
)

def load_data(transformed_tables):
    
    table_order = [
        "dim_user",
        "dim_category",
        "dim_product",
        "fact_cart",
        "fact_cart_item"
    ]
    
    try:
        with engine.begin() as connection:
            
            for table_name in table_order:
                
                df = transformed_tables[table_name]
                df.to_sql(
                    name=table_name,
                    con=connection,
                    schema="dbo",
                    if_exists="append",
                    index=False,
                    chunksize=1000
                )
                
                print(
                    f"{table_name}"
                    f"{len(df)} rows loaded successfully."
                )
                
            print(
                f"\nAll tables loaded successfully"
            )
            
    except Exception as e:
        print("error loading data", e)
        raise
    
    
def close_connection():
    engine.dispose()

                
                
        
