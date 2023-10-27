-- run in DB Browser

CREATE TABLE "order" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INT,
    "user_email" VARCHAR(200),
    "user_address" VARCHAR(200),
    "user_mobile" INT,
    "purchase_date" DATE,
    "ship_date" DATE,
    "status" INT
);

CREATE TABLE order_details (
    order_id INT,
    product_id INT,
    price NUMERIC,
    quantity INT,
    PRIMARY KEY (order_id, product_id)
)

