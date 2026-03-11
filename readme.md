# Ecommerce Sales Analytics Dashboard

A full-stack **data analytics dashboard** that analyzes ecommerce sales data using **Python, MySQL, Pandas, Flask, and Chart.js**.
The system processes large sales datasets, performs analytics, and displays business insights through an interactive web dashboard.

---

## Project Overview

This project demonstrates how modern data analytics systems are built using:

* **Data ingestion**
* **Data cleaning**
* **Database modeling**
* **Backend analytics APIs**
* **Frontend visualization dashboards**

The dashboard provides key business insights such as revenue trends, top products, geographic sales distribution, and category performance.

---

## Key Features

### Data Processing

* Load ecommerce dataset from CSV
* Clean data using **Pandas**
* Remove invalid or cancelled orders
* Convert and normalize data formats

### Database System

* Structured relational database using **MySQL**
* Optimized schema for analytics queries
* Indexed tables for faster performance

### Backend API

* Built using **Flask**
* REST APIs for analytics data
* Cached analytics to reduce computation time

### Interactive Dashboard

* Built using **HTML, CSS, Bootstrap**
* Data visualization with **Chart.js**
* Neo-Brutalism UI design style

### Analytics Insights

The dashboard provides:

* Total Revenue
* Total Orders
* Total Products
* Total Cities
* Monthly Revenue Trend
* Top Selling Products
* Sales by Category
* Top Cities by Revenue
* Top States by Revenue
* Revenue Growth Indicator

### User Interaction

* Date filters:

  * Last 30 Days
  * Last 6 Months
  * All Time
* Dynamic charts that update without page reload
* Dark mode toggle

---

## Project Architecture

```
CSV Dataset
    ↓
Data Cleaning (Pandas)
    ↓
MySQL Database
    ↓
Flask Backend API
    ↓
Analytics Engine (Pandas)
    ↓
Chart.js Dashboard
```

---

## Tech Stack

### Backend

* Python 3.13
* Flask

### Data Analytics

* Pandas
* NumPy

### Database

* MySQL
* XAMPP (phpMyAdmin)

### Visualization

* Chart.js
* Matplotlib
* Seaborn

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Design Style

* Neo-Brutalism UI

---

## Project Folder Structure

```
ecommerce-analytics-dashboard
│
├── app.py
├── config.py
├── requirements.txt
│
├── analytics
│   └── analytics.py
│
├── database
│   └── schema.sql
│
├── dataset
│   └── Amazon Sale Report.csv
│
├── scripts
│   └── load_dataset.py
│
├── static
│   ├── css
│   │   └── style.css
│   ├── js
│   │   └── dashboard.js
│   └── charts
│
├── templates
│   └── dashboard.html
│
└── utils
    └── db.py
```

---

## Database Schema

The system uses a relational schema optimized for analytics.

Tables include:

* **orders**
* **products**
* **locations**
* **order_items**

This structure enables efficient queries for:

* revenue aggregation
* product analytics
* geographic insights

---

## Installation Guide

### 1. Clone the Repository

```
git clone https://github.com/yourusername/ecommerce-analytics-dashboard.git
cd ecommerce-analytics-dashboard
```

---

### 2. Install Python Dependencies

```
pip install -r requirements.txt
```

---

### 3. Start MySQL (XAMPP)

Start the following services:

* Apache
* MySQL

Open phpMyAdmin:

```
http://localhost/phpmyadmin
```

---

### 4. Create Database

Run the schema file:

```
database/schema.sql
```

This creates the required tables.

---

### 5. Import Dataset

Run the data loader:

```
python scripts/load_dataset.py
```

This will:

* load the CSV dataset
* clean the data
* insert records into MySQL

---

### 6. Run the Flask Server

```
python app.py
```

Open the dashboard in your browser:

```
http://127.0.0.1:5000
```

---

## Dashboard Preview

The dashboard provides:

* KPI summary cards
* revenue growth indicators
* interactive charts
* geographic sales analysis

Charts include:

* Monthly Sales Trend
* Top Products
* Sales by Category
* Top Cities
* Top States

---

## Performance Optimization

To improve dashboard speed:

* Pandas data caching
* API response caching
* Indexed database queries
* Parallel chart loading

These optimizations reduce dashboard reload time significantly.

---

## Dataset

The dataset used in this project is based on an **Amazon ecommerce sales report**.

Fields include:

* Order ID
* Order Date
* Product SKU
* Product Category
* Quantity Sold
* Revenue
* City
* State
* Country

---

## Future Improvements

Potential enhancements:

* AI sales prediction
* Customer segmentation
* Profit analysis
* Time-series forecasting
* Deployment on cloud platform

---

## Author

Krish

Master of Computer Applications (MCA)
Full-Stack & Data Analytics Developer

---

## License

This project is intended for academic and educational purposes.

Co-authored-by: @isthatpratham <premdebnath08@gmail.com>

