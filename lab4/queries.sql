SELECT logs.id, users.username, message FROM logs
LEFT JOIN users ON logs.user_id = users.id;

SELECT COUNT(id) AS orders_quantity, customer_id 
FROM orders GROUP BY customer_id HAVING COUNT(id) > 0;

SELECT COUNT(order_id), books.title FROM orders_books
RIGHT JOIN books ON orders_books.book_id = books.id
GROUP BY books.title ORDER BY COUNT(order_id) DESC;

SELECT * FROM books
JOIN publishers ON books.publisher_id = publishers.id;

SELECT * FROM books
JOIN suppliers ON books.supplier_id = suppliers.id;

SELECT * FROM orders
JOIN customers ON orders.customer_id = customers.id;

SELECT books.id, books.title, ARRAY_AGG(genres.name) 
FROM genres
JOIN genres_books ON genres.id = genres_books.genre_id
JOIN books ON books.id = genres_books.book_id
GROUP BY books.id, books.title;

SELECT * FROM books
JOIN genres_books ON genres_books.book_id = books.id
WHERE genre_id = 5; 

SELECT reviews.review_text, users.name, users.username 
FROM reviews
JOIN customers ON reviews.review_author_id = customers.id
JOIN users ON customers.user_id = users.id WHERE book_id = 1;

SELECT * FROM logs JOIN users ON logs.user_id = users.id
WHERE EXISTS (SELECT FROM customers WHERE user_id = users.id);

SELECT * FROM logs JOIN users ON logs.user_id = users.id
WHERE EXISTS (SELECT FROM employees WHERE user_id = users.id);

SELECT books.id, books.title, order_id FROM orders_books
JOIN books ON books.id = orders_books.book_id
WHERE order_id = 4;

SELECT books.id, books.title, ARRAY_AGG(authors.name)
FROM books 
LEFT JOIN authors_books ON books.id = authors_books.book_id
JOIN authors ON authors_books.author_id = authors.id
GROUP BY books.id;

SELECT books.*, ARRAY_AGG(authors.name)
FROM books 
LEFT JOIN authors_books ON books.id = authors_books.book_id
JOIN authors ON authors_books.author_id = authors.id
WHERE book_id = 21
GROUP BY books.id;

SELECT books.id, books.title,
CASE WHEN price IS NULL THEN 'Out of stock'
ELSE CAST(price AS VARCHAR) END
FROM books;


CREATE VIEW books_with_authors AS 
SELECT books.*, ARRAY_AGG(authors.name) AS authors_names
FROM books 
LEFT JOIN authors_books ON books.id = authors_books.book_id
JOIN authors ON authors_books.author_id = authors.id
GROUP BY books.id;

SELECT * FROM books_with_authors
WHERE book_id = 21;

SELECT * FROM books_with_authors;