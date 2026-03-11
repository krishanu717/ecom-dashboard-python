import os
from flask import Flask, render_template, jsonify, request
from analytics.analytics import (
    get_kpi_metrics,
    monthly_sales,
    top_products,
    category_sales,
    top_cities,
    revenue_growth,
    top_states
)

app = Flask(__name__)

# In-memory API Cache Dictionary
api_cache = {}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/kpi')
def api_kpi():
    range_filter = request.args.get("range", "all")
    cache_key = f'/api/kpi?range={range_filter}'
    if cache_key in api_cache:
        return jsonify(api_cache[cache_key])
    
    try:
        data = get_kpi_metrics(range_filter)
        api_cache[cache_key] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/monthly-sales')
def api_monthly_sales():
    range_filter = request.args.get("range", "all")
    cache_key = f'/api/monthly-sales?range={range_filter}'
    if cache_key in api_cache:
        return jsonify(api_cache[cache_key])
        
    try:
        data = monthly_sales(range_filter)
        api_cache[cache_key] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/top-products')
def api_top_products():
    range_filter = request.args.get("range", "all")
    cache_key = f'/api/top-products?range={range_filter}'
    if cache_key in api_cache:
        return jsonify(api_cache[cache_key])
        
    try:
        data = top_products(range_filter)
        api_cache[cache_key] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/category-sales')
def api_category_sales():
    range_filter = request.args.get("range", "all")
    cache_key = f'/api/category-sales?range={range_filter}'
    if cache_key in api_cache:
        return jsonify(api_cache[cache_key])
        
    try:
        data = category_sales(range_filter)
        api_cache[cache_key] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/top-cities')
def api_top_cities():
    range_filter = request.args.get("range", "all")
    cache_key = f'/api/top-cities?range={range_filter}'
    if cache_key in api_cache:
        return jsonify(api_cache[cache_key])
        
    try:
        data = top_cities(range_filter)
        api_cache[cache_key] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/revenue-growth')
def api_revenue_growth():
    range_filter = request.args.get("range", "all")
    cache_key = f'/api/revenue-growth?range={range_filter}'
    if cache_key in api_cache:
        return jsonify(api_cache[cache_key])
        
    try:
        data = revenue_growth(range_filter)
        api_cache[cache_key] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/top-states')
def api_top_states():
    range_filter = request.args.get("range", "all")
    cache_key = f'/api/top-states?range={range_filter}'
    if cache_key in api_cache:
        return jsonify(api_cache[cache_key])
        
    try:
        data = top_states(range_filter)
        api_cache[cache_key] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
