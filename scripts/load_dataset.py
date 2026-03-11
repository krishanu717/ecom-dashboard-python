import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
import sys

def native_type(val):
    if pd.isna(val):
        return None
    if isinstance(val, (np.int64, np.int32)):
        return int(val)
    if isinstance(val, (np.float64, np.float32)):
        return float(val)
    return val

def main():
    csv_path = r"C:\Users\mkris\Downloads\ecomm\dataset\Amazon Sale Report.csv"
    
    # Step 1: Load dataset
    print("Loading dataset")
    try:
        df = pd.read_csv(csv_path, low_memory=False)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        sys.exit(1)

    # Step 2: Data Cleaning
    print("Cleaning dataset")
    try:
        df.rename(columns=lambda x: str(x).strip(), inplace=True)
        
        # remove rows where Amount is null
        if 'Amount' in df.columns:
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            df = df.dropna(subset=['Amount'])
            
        # remove rows where Qty <= 0
        if 'Qty' in df.columns:
            df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(0).astype(int)
            df = df[df['Qty'] > 0]
            
        # remove rows where Status = Cancelled
        if 'Status' in df.columns:
            df = df[df['Status'].astype(str).str.strip().str.lower() != 'cancelled']
            
        # Drop duplicates
        df = df.drop_duplicates()
        
        # convert Date column to datetime format
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.dropna(subset=['Date'])
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
            
        print(f"Number of rows after cleaning: {len(df)}")
        
        # String truncations referencing schema constraints
        string_cols_50 = ['Order ID', 'Status', 'Fulfilment', 'Sales Channel', 'SKU']
        for col in string_cols_50:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str[:50]
                
        if 'Style' in df.columns:
            df['Style'] = df['Style'].fillna('Unknown').astype(str).str.strip().str[:200]
            
        if 'Category' in df.columns:
            df['Category'] = df['Category'].fillna('Unknown').astype(str).str.strip().str[:100]
            
        if 'Size' in df.columns:
            df['Size'] = df['Size'].fillna('Unknown').astype(str).str.strip().str[:20]
            
        city_state_country = ['ship-city', 'ship-state', 'ship-country']
        for col in city_state_country:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown').astype(str).str.strip().str[:100]
                
    except Exception as e:
        print(f"Error during data cleaning: {e}")
        sys.exit(1)

    # Database operations
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ecommerce_dashboard'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            chunk_size = 5000
            
            # Step 3: Insert Products
            print("Inserting products")
            products_df = df[['SKU', 'Style', 'Category', 'Size']].drop_duplicates(subset=['SKU'])
            products_data = [tuple(native_type(x) for x in row) for row in products_df.to_numpy()]
            
            insert_prod_query = """
                INSERT IGNORE INTO products (sku, product_name, category, size)
                VALUES (%s, %s, %s, %s)
            """
            for i in range(0, len(products_data), chunk_size):
                cursor.executemany(insert_prod_query, products_data[i:i+chunk_size])
            connection.commit()
            
            # Fetch product mapping
            cursor.execute("SELECT sku, product_id FROM products")
            product_map = {row[0]: row[1] for row in cursor.fetchall()}
            df['product_id'] = df['SKU'].map(product_map)
            
            # Step 4: Insert Locations
            print("Inserting locations")
            locations_df = df[['ship-city', 'ship-state', 'ship-country']].drop_duplicates()
            locations_data = [tuple(native_type(x) for x in row) for row in locations_df.to_numpy()]
            
            insert_loc_query = """
                INSERT IGNORE INTO locations (city, state, country)
                VALUES (%s, %s, %s)
            """
            for i in range(0, len(locations_data), chunk_size):
                cursor.executemany(insert_loc_query, locations_data[i:i+chunk_size])
            connection.commit()
            
            # Fetch location mapping
            cursor.execute("SELECT city, state, country, location_id FROM locations")
            location_map = {(row[0], row[1], row[2]): row[3] for row in cursor.fetchall()}
            df['location_id'] = pd.Series(list(zip(df['ship-city'], df['ship-state'], df['ship-country'])), index=df.index).map(location_map)
            
            # Step 5: Insert Orders
            print("Inserting orders")
            orders_cols = ['Order ID', 'Date', 'Status', 'Fulfilment', 'Sales Channel', 'location_id']
            orders_df = df[orders_cols].drop_duplicates(subset=['Order ID'])
            orders_data = [tuple(native_type(x) for x in row) for row in orders_df.to_numpy()]
            
            insert_order_query = """
                INSERT IGNORE INTO orders (order_id, order_date, status, fulfilment, sales_channel, location_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            for i in range(0, len(orders_data), chunk_size):
                cursor.executemany(insert_order_query, orders_data[i:i+chunk_size])
            connection.commit()
            
            # Step 6: Insert Order Items
            print("Inserting order items")
            order_items_df = df[['Order ID', 'product_id', 'Qty', 'Amount']].copy()
            order_items_df = order_items_df.dropna(subset=['product_id'])
            order_items_data = [tuple(native_type(x) for x in row) for row in order_items_df.to_numpy()]
            
            insert_order_items_query = """
                INSERT INTO order_items (order_id, product_id, quantity, amount)
                VALUES (%s, %s, %s, %s)
            """
            for i in range(0, len(order_items_data), chunk_size):
                cursor.executemany(insert_order_items_query, order_items_data[i:i+chunk_size])
            connection.commit()
            
            print("Dataset import completed successfully")
            
    except Error as e:
        print(f"Database error during SQL insertion: {e}")
    except Exception as e:
        print(f"Error during SQL operations: {e}")
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()
