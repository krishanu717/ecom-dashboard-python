import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error

# Global cache variables
_cached_df = None
_cached_kpi = {}
_cached_monthly_sales = {}
_cached_top_products = {}
_cached_category_sales = {}
_cached_top_cities = {}
_cached_top_states = {}
_cached_revenue_growth = {}

def get_connection():
    """Establish and return database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ecommerce_dashboard'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
    return None

def load_sales_data():
    """Load sales data from the database into a pandas DataFrame."""
    global _cached_df
    if _cached_df is not None:
        return _cached_df

    connection = get_connection()
    if not connection:
        return pd.DataFrame()

    query = """
        SELECT
            o.order_id,
            o.order_date,
            p.product_name,
            p.category,
            oi.quantity,
            oi.amount,
            l.city,
            l.state
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN locations l ON o.location_id = l.location_id
    """
    try:
        df = pd.read_sql(query, connection)
        if not df.empty and 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'])
            _cached_df = df
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
    finally:
        if connection.is_connected():
            connection.close()

def apply_date_filter(df, range_filter):
    if df.empty or 'order_date' not in df.columns:
        return df

    today = df['order_date'].max()
    
    if range_filter == "30d":
        df = df[df["order_date"] >= (today - pd.Timedelta(days=30))]
    elif range_filter == "6m":
        df = df[df["order_date"] >= (today - pd.DateOffset(months=6))]
        
    return df

def get_kpi_metrics(range_filter="all"):
    """Calculate and return KPI metrics."""
    global _cached_kpi
    if range_filter in _cached_kpi:
        return _cached_kpi[range_filter]

    try:
        df = load_sales_data()
        df = apply_date_filter(df, range_filter)
        
        if df.empty:
            return {"total_revenue": 0, "total_orders": 0, "total_products": 0, "total_cities": 0}

        total_revenue = float(df['amount'].sum()) if 'amount' in df.columns else 0.0
        total_orders = int(df['order_id'].nunique()) if 'order_id' in df.columns else 0
        total_products = int(df['product_name'].nunique()) if 'product_name' in df.columns else 0
        total_cities = int(df['city'].nunique()) if 'city' in df.columns else 0

        res = {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "total_products": total_products,
            "total_cities": total_cities
        }
        _cached_kpi[range_filter] = res
        return res
    except Exception as e:
        print(f"Error calculating KPI metrics: {e}")
        return {"total_revenue": 0, "total_orders": 0, "total_products": 0, "total_cities": 0}

def monthly_sales(range_filter="all"):
    """Calculate and return monthly sales trend."""
    global _cached_monthly_sales
    if range_filter in _cached_monthly_sales:
        return _cached_monthly_sales[range_filter]

    try:
        df = load_sales_data()
        df = apply_date_filter(df, range_filter)
        
        if df.empty or 'order_date' not in df.columns or 'amount' not in df.columns:
            return {"labels": [], "data": []}

        df['month'] = df['order_date'].dt.to_period('M').astype(str)
        monthly_df = df.groupby('month')['amount'].sum().reset_index()
        monthly_df = monthly_df.sort_values('month')

        res = {
            "labels": monthly_df['month'].tolist(),
            "data": [float(x) for x in monthly_df['amount'].tolist()]
        }
        _cached_monthly_sales[range_filter] = res
        return res
    except Exception as e:
        print(f"Error calculating monthly sales: {e}")
        return {"labels": [], "data": []}

def top_products(range_filter="all"):
    """Calculate and return top 10 selling products based on quantity."""
    global _cached_top_products
    if range_filter in _cached_top_products:
        return _cached_top_products[range_filter]

    try:
        df = load_sales_data()
        df = apply_date_filter(df, range_filter)
        
        if df.empty or 'product_name' not in df.columns or 'quantity' not in df.columns:
            return {"labels": [], "data": []}

        top_prod_df = df.groupby('product_name')['quantity'].sum().reset_index()
        top_prod_df = top_prod_df.sort_values(by='quantity', ascending=False).head(10)

        res = {
            "labels": top_prod_df['product_name'].tolist(),
            "data": [int(x) for x in top_prod_df['quantity'].tolist()]
        }
        _cached_top_products[range_filter] = res
        return res
    except Exception as e:
        print(f"Error calculating top products: {e}")
        return {"labels": [], "data": []}

def category_sales(range_filter="all"):
    """Calculate and return sales revenue broken down by category."""
    global _cached_category_sales
    if range_filter in _cached_category_sales:
        return _cached_category_sales[range_filter]

    try:
        df = load_sales_data()
        df = apply_date_filter(df, range_filter)
        
        if df.empty or 'category' not in df.columns or 'amount' not in df.columns:
            return {"labels": [], "data": []}

        cat_df = df.groupby('category')['amount'].sum().reset_index()
        cat_df = cat_df.sort_values(by='amount', ascending=False).head(10)

        res = {
            "labels": cat_df['category'].tolist(),
            "data": [float(x) for x in cat_df['amount'].tolist()]
        }
        _cached_category_sales[range_filter] = res
        return res
    except Exception as e:
        print(f"Error calculating category sales: {e}")
        return {"labels": [], "data": []}

def top_cities(range_filter="all"):
    """Calculate and return top 10 cities by revenue."""
    global _cached_top_cities
    if range_filter in _cached_top_cities:
        return _cached_top_cities[range_filter]

    try:
        df = load_sales_data()
        df = apply_date_filter(df, range_filter)
        
        if df.empty or 'city' not in df.columns or 'amount' not in df.columns:
            return {"labels": [], "data": []}

        city_df = df.groupby('city')['amount'].sum().reset_index()
        city_df = city_df.sort_values(by='amount', ascending=False).head(10)

        res = {
            "labels": city_df['city'].tolist(),
            "data": [float(x) for x in city_df['amount'].tolist()]
        }
        _cached_top_cities[range_filter] = res
        return res
    except Exception as e:
        print(f"Error calculating top cities: {e}")
        return {"labels": [], "data": []}

def revenue_growth(range_filter="all"):
    """Calculate and return month-over-month revenue growth percentage."""
    global _cached_revenue_growth
    if range_filter in _cached_revenue_growth:
        return _cached_revenue_growth[range_filter]

    try:
        df = load_sales_data()
        df = apply_date_filter(df, range_filter)
        
        if df.empty or 'order_date' not in df.columns or 'amount' not in df.columns:
            return {"growth_percent": 0.0}

        df['month'] = df['order_date'].dt.to_period('M')
        monthly_revenue = df.groupby('month')['amount'].sum().sort_index()

        if len(monthly_revenue) <= 1:
            return {"growth_percent": 0.0}

        growth = monthly_revenue.pct_change() * 100
        latest_growth = float(growth.iloc[-1])

        if pd.isna(latest_growth):
            return {"growth_percent": 0.0}

        res = {"growth_percent": round(latest_growth, 2)}
        _cached_revenue_growth[range_filter] = res
        return res
    except Exception as e:
        print(f"Error calculating revenue growth: {e}")
        return {"growth_percent": 0.0}

def top_states(range_filter="all"):
    """Calculate and return top 10 states by revenue."""
    global _cached_top_states
    if range_filter in _cached_top_states:
        return _cached_top_states[range_filter]

    try:
        df = load_sales_data()
        df = apply_date_filter(df, range_filter)
        
        if df.empty or 'state' not in df.columns or 'amount' not in df.columns:
            return {"labels": [], "data": []}

        state_df = df.groupby('state')['amount'].sum().reset_index()
        state_df = state_df.sort_values(by='amount', ascending=False).head(10)

        res = {
            "labels": state_df['state'].tolist(),
            "data": [float(x) for x in state_df['amount'].tolist()]
        }
        _cached_top_states[range_filter] = res
        return res
    except Exception as e:
        print(f"Error calculating top states: {e}")
        return {"labels": [], "data": []}
