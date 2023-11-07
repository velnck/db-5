CREATE TABLE IF NOT EXISTS users
(
	id serial PRIMARY KEY,
	username varchar(100) NOT NULL UNIQUE,
	password varchar(100) NOT NULL,
	email varchar(256) NOT NULL,
	name varchar(256),
	phone_number varchar NOT NULL
);


CREATE TABLE IF NOT EXISTS customers
(
	id serial PRIMARY KEY,
	user_id serial NOT NULL UNIQUE,
	CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS employees
(
	id serial PRIMARY KEY,
	user_id serial NOT NULL UNIQUE,
	CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS logs
(
	id serial PRIMARY KEY,
	user_id serial,
	message varchar(500) NOT NULL,
	CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS publishers
(
	id serial PRIMARY KEY,
	name varchar(256) NOT NULL UNIQUE,
	address varchar
);


CREATE TABLE IF NOT EXISTS suppliers
(
	id serial PRIMARY KEY,
	address varchar,
	phone varchar,
	email varchar(256),
	name varchar(256) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS genres
(
	id serial PRIMARY KEY,
	name varchar(256) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS authors
(
	id serial PRIMARY KEY,
	name varchar(256) NOT NULL
);


CREATE TABLE IF NOT EXISTS books
(
	id serial PRIMARY KEY,
	isbn varchar(13) NOT NULL UNIQUE,
	title varchar NOT NULL,
	publisher_id serial,
	price decimal CHECK (price > 0),
	supplier_id serial,
	CONSTRAINT fk_publisher 
		FOREIGN KEY(publisher_id) 
			REFERENCES publishers(id) ON DELETE SET NULL,
	CONSTRAINT fk_supplier 
		FOREIGN KEY(supplier_id) 
			REFERENCES suppliers(id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS orders
(
	id serial PRIMARY KEY,
	delivery_address varchar NOT NULL,
	creation_date timestamp,
	delivery_date date NOT NULL,
	customer_id serial,
	sum_total decimal CHECK (sum_total > 0),
	CONSTRAINT fk_customer 
		FOREIGN KEY(customer_id) 
			REFERENCES customers(id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS reviews
(
	id serial PRIMARY KEY,
	review_author_id serial NOT NULL,
	book_id serial NOT NULL,
	review_text varchar,
	CONSTRAINT fk_review_author
		FOREIGN KEY(review_author_id)
			REFERENCES customers(id) ON DELETE CASCADE,
	CONSTRAINT fk_book
		FOREIGN KEY(book_id)
			REFERENCES books(id)
);


CREATE TABLE IF NOT EXISTS authors_books
(
	author_id serial REFERENCES authors(id) ON DELETE CASCADE,
	book_id serial REFERENCES books(id) ON DELETE CASCADE,
	CONSTRAINT authors_books_pk PRIMARY KEY(author_id, book_id)
);


CREATE TABLE IF NOT EXISTS genres_books
(
	genre_id serial REFERENCES genres(id) ON DELETE CASCADE,
	book_id serial REFERENCES books(id) ON DELETE CASCADE,
	CONSTRAINT genres_books_pk PRIMARY KEY(genre_id, book_id)
);


CREATE TABLE IF NOT EXISTS orders_books
(
	order_id serial REFERENCES orders(id) ON DELETE CASCADE,
	book_id serial REFERENCES books(id) ON DELETE CASCADE,
	CONSTRAINT orders_books_pk PRIMARY KEY(order_id, book_id)
);