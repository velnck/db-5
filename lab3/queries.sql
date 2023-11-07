SELECT * FROM books 
ORDER BY title LIMIT 5 OFFSET 10;


SELECT * FROM genres
ORDER BY name;


SELECT COUNT(id) AS reviews_quantity, review_author_id FROM reviews
GROUP BY review_author_id;


SELECT COUNT(id) FROM orders
WHERE customer_id = 1;


SELECT * FROM authors  ORDER BY name DESC;


SELECT id, title, price FROM books
WHERE price BETWEEN 15.00 AND 20.00 ORDER BY price;


SELECT title, publisher_id, supplier_id FROM books
WHERE publisher_id = 1 AND supplier_id = 3;


SELECT customer_id, delivery_address, creation_date::DATE FROM orders
WHERE delivery_address LIKE '%ул. Брестская%';


SELECT logs.id, users.username, message 
FROM logs JOIN users 
ON logs.user_id = users.id;


SELECT COUNT(id) AS orders_quantity, customer_id 
FROM orders
GROUP BY customer_id
HAVING COUNT(id) > 0;


SELECT books.title, genre_id FROM genres_books
JOIN books ON genres_books.book_id = books.id
WHERE genre_id IN(2, 3);


UPDATE books
SET price = price + 5
WHERE publisher_id = 3;

