DROP DATABASE IF EXISTS ecommerce_dashboard;
CREATE DATABASE ecommerce_dashboard;
USE ecommerce_dashboard;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50),
    product_name VARCHAR(200),
    category VARCHAR(100),
    size VARCHAR(20),
    INDEX idx_category (category)
);

CREATE TABLE locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    INDEX idx_city (city)
);

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date DATE,
    status VARCHAR(50),
    fulfilment VARCHAR(50),
    sales_channel VARCHAR(50),
    location_id INT,
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    INDEX idx_order_date (order_date)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(50),
    product_id INT,
    quantity INT,
    amount DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
