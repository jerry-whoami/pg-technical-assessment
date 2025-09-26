DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS deliveries CASCADE;
DROP TABLE IF EXISTS restaurants CASCADE;
DROP TABLE IF EXISTS delivery_persons CASCADE;

CREATE TABLE delivery_persons (
    delivery_person_id INT PRIMARY KEY,
    name VARCHAR,
    region VARCHAR,
    hired_date DATE,
    is_active BOOLEAN
);

CREATE TABLE restaurants (
    restaurant_id VARCHAR PRIMARY KEY,
    area VARCHAR,
    name VARCHAR,
    cuisine_type VARCHAR,
    avg_preparation_time_min FLOAT
);

CREATE TABLE deliveries (
    delivery_id VARCHAR PRIMARY KEY,
    delivery_person_id INT REFERENCES delivery_persons(delivery_person_id),
    restaurant_area VARCHAR,
    customer_area VARCHAR,
    delivery_distance_km FLOAT,
    delivery_time_min INT,
    order_placed_at TIMESTAMP,
    weather_condition VARCHAR,
    traffic_condition VARCHAR,
    delivery_rating FLOAT
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    delivery_id VARCHAR REFERENCES deliveries(delivery_id),
    restaurant_id VARCHAR REFERENCES restaurants(restaurant_id),
    customer_id VARCHAR,
    order_value FLOAT,
    items_count INT
);
