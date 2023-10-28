CREATE DATABASE restaurant_chatbot;
USE restaurant_chatbot;

CREATE TABLE Restaurants (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_name VARCHAR(255) NOT NULL
);

CREATE TABLE FoodItems (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT,
    item_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);

INSERT INTO Restaurants (restaurant_name) VALUES
('Arcadian Cafe'),
('Veera 5'),
('Monal Lahore restaurant'),
('Pablos restaurant'),
('Cafe Aylanto'),
('Andaaz Restaurant');

select * from FoodItems;
DROP TABLE reservations;

-- Arcadian Cafe
INSERT INTO FoodItems (restaurant_id, item_name, price) VALUES
(1, 'black pepper asian', 1500),
(1, 'garlic butter steak', 1800),
(1, 'crispy battered fish', 1400),
(1, 'apple mint', 600),
(1, 'bread pudding', 900);

-- Veera 5
INSERT INTO FoodItems (restaurant_id, item_name, price) VALUES
(2, 'chicken chowmein', 1200),
(2, 'Thai chili paste chicken', 1400),
(2, 'crispy battered fish', 1300),
(2, 'beef with broccoli', 1500),
(2, 'lime fish', 1600),
(2, 'prawns in garlic sauce', 1900);

-- Monal Lahore restaurant
INSERT INTO FoodItems (restaurant_id, item_name, price) VALUES
(3, 'chicken gola kabab', 2000),
(3, 'Moroccan chicken', 2200),
(3, 'Chinese fried rice', 1800),
(3, 'mutton karahi', 2300),
(3, 'gulab jamun', 800);

-- Pablos restaurant
INSERT INTO FoodItems (restaurant_id, item_name, price) VALUES
(4, 'fajita pasta', 1700),
(4, 'crispy chicken wrap', 1400),
(4, 'garlic mayo fries', 800),
(4, 'pink pasta', 1900),
(4, 'molten lava wrap', 1600);

-- Cafe Aylanto
INSERT INTO FoodItems (restaurant_id, item_name, price) VALUES
(5, 'oven baked fish', 2200),
(5, 'kalamata chicken', 1900),
(5, 'spicy lamb chops', 2400),
(5, 'mexican burger', 1500),
(5, 'fudge cake', 1100);

-- Andaaz Restaurant
INSERT INTO FoodItems (restaurant_id, item_name, price) VALUES
(6, 'bhuna gosht', 1800),
(6, 'chanp bhuna', 2000),
(6, 'murgh tikka masala', 2200),
(6, 'lassi', 500),
(6, 'nimbu soda', 400);

CREATE TABLE orders (
  order_id INT NOT NULL,
  restraurant_name VARCHAR(255),
  item_id INT NOT NULL,
  food_item_name VARCHAR(255),
  quantity INT DEFAULT NULL,
  total_price DECIMAL(10,2) DEFAULT NULL,
  c_name VARCHAR(255),
  c_address VARCHAR(255),
  PRIMARY KEY (order_id, item_id),
  KEY orders_ibfk_1 (item_id),
  CONSTRAINT orders_ibfk_1 FOREIGN KEY (item_id) REFERENCES FoodItems (item_id)
);

CREATE TABLE Timings (
    timing_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT,
    opening_time TIME,
    closing_time TIME,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);


CREATE TABLE Reservations (
    reservation_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT,
    restaurant_name VARCHAR(255),
    reservation_time TIME,
    reservation_date DATE,
    number_of_people INT,
    customer_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);





select * from orders;
