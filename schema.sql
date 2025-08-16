CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

INSERT INTO products (name, price) VALUES
    ('Apple', 0.5),
    ('Banana', 0.3),
    ('Chocolate', 1.5);
