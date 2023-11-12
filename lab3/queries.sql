SELECT * FROM books 
ORDER BY title LIMIT 5 OFFSET 10;


SELECT * FROM books ORDER BY price;


SELECT * FROM books 
JOIN authors_books ON authors_books.book_id = books.id
WHERE author_id = 4 
AND price BETWEEN 17 AND 20;


SELECT * FROM genres ORDER BY name;


SELECT * FROM books
WHERE publisher_id = 1;


SELECT title, publisher_id, supplier_id FROM books
WHERE publisher_id = 1 AND supplier_id = 3;


SELECT COUNT(id) FROM orders
WHERE customer_id = 1;


SELECT * FROM authors  ORDER BY name;


SELECT id, title, price FROM books
WHERE price BETWEEN 15.00 AND 20.00 ORDER BY price;


SELECT * FROM books
WHERE title ILIKE '%история%';


SELECT customer_id, delivery_address, creation_date::DATE FROM orders
WHERE delivery_address LIKE '%ул. Брестская%';


UPDATE books SET price = price + 5
WHERE publisher_id = 3;