------------------------------------------------------------

-- create new user
CREATE OR REPLACE PROCEDURE create_user(
	username_p varchar,
	password_p varchar,
	email_p varchar,
	name_p varchar,
	phone_number_p varchar, 
    role_id_p INTEGER
)
LANGUAGE plpgsql
AS $$
    BEGIN
        -- check if username exists
        IF EXISTS (SELECT FROM users WHERE users.username=username_p) THEN
            RAISE EXCEPTION 'Username already exists.';
        ELSE
            -- insert new user
            INSERT INTO users (username, password, email, name, phone_number, is_active, role_id)
            VALUES (username_p, password_p, email_p, name_p, phone_number_p, TRUE, role_id_p);
        END IF;
    END;
$$;

------------------------------------------------------------



------------------------------------------------------------

-- add book to order
-- (update quantity or insert orders_books row)
CREATE OR REPLACE PROCEDURE add_book_to_order(
    order_id_p INTEGER, 
    book_id_p INTEGER
)
LANGUAGE plpgsql
AS $$
    DECLARE 
        reserved INTEGER;
        total INTEGER;
    BEGIN
        SELECT COALESCE(SUM(quantity), 0) INTO reserved 
        FROM orders_books 
        WHERE order_id = order_id_p 
        AND book_id = book_id_p;
        SELECT quantity INTO total FROM books WHERE id = book_id_p;
        IF total > reserved THEN
            INSERT INTO orders_books (order_id, book_id, quantity)
            VALUES (order_id_p, book_id_p, 1)
            ON CONFLICT ON CONSTRAINT orders_books_pk DO 
            UPDATE SET quantity = orders_books.quantity + 1 
            WHERE orders_books.order_id = order_id_p 
            AND orders_books.book_id = book_id_p;
        ELSE
            RAISE EXCEPTION 'Out of stock.';
        END IF;
    END;
$$;

------------------------------------------------------------



------------------------------------------------------------

-- remove book from order
-- (update quantity or delete orders_books row)
CREATE OR REPLACE PROCEDURE remove_book_from_order(
    order_id_p INTEGER, 
    book_id_p INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE 
    qt INTEGER;
BEGIN
    -- check if row exists
    SELECT quantity INTO qt FROM orders_books 
    WHERE order_id = order_id_p AND book_id = book_id_p;
    IF qt IS NOT NULL THEN
        IF qt > 1 THEN
            -- if quantity more than 1 then decrement
            UPDATE orders_books SET quantity = quantity - 1 
            WHERE order_id = order_id_p AND book_id = book_id_p;
        ELSIF qt = 1 THEN
            -- if quantity = 1 delete row
            DELETE FROM orders_books WHERE order_id = order_id_p 
            AND book_id = book_id_p;
        END IF;
    END IF;
END;
$$;

-- call remove_book_from_order(4, 6);
 
-- SELECT books.id, books.title, order_id, orders_books.quantity 
-- FROM orders_books
-- JOIN books ON books.id = orders_books.book_id
-- WHERE order_id = 4;

-- call remove_book_from_order(4, 7);
 
-- SELECT books.id, books.title, order_id, orders_books.quantity 
-- FROM orders_books
-- JOIN books ON books.id = orders_books.book_id
-- WHERE order_id = 4;

------------------------------------------------------------



------------------------------------------------------------

-- commit order (check if all fields 
-- are correct and order is not empty 
-- raise error if necessary)

CREATE OR REPLACE PROCEDURE commit_order(id_p integer)
LANGUAGE plpgsql
AS $$
DECLARE
    order_row orders%ROWTYPE;
    items_count INTEGER;
BEGIN
    SELECT orders.* INTO order_row
    FROM orders WHERE orders.id = id_p;
    -- check if already commited
    IF order_row.is_commited IS TRUE THEN
        RETURN;
    -- if not commited
    ELSE
        -- check address filled
        IF order_row.delivery_address = '' IS TRUE 
        OR order_row.delivery_address IS NULL THEN
            RAISE EXCEPTION 'Address is empty.';
            RETURN;
        END IF;
        -- check not empty (orders_books rows exist)
        SELECT SUM(quantity) INTO items_count 
        FROM orders_books 
        WHERE orders_books.order_id = id_p;
        IF items_count <= 0 OR items_count IS NULL THEN
            RAISE EXCEPTION 'Order is empty.';
            RETURN;
        END IF;
        UPDATE orders SET is_commited = TRUE WHERE id = id_p;
    END IF;
END;
$$;

------------------------------------------------------------



------------------------------------------------------------

CREATE OR REPLACE PROCEDURE delete_order(id_p INTEGER)
LANGUAGE PLPGSQL
AS $$
BEGIN
    DELETE FROM orders WHERE id = id_p;
END;
$$;

------------------------------------------------------------



------------------------------------------------------------

-- update order sum
CREATE OR REPLACE PROCEDURE update_order_sum(
    IN order_id_p INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE 
    new_total_sum decimal;
BEGIN
    SELECT SUM(orders_books.quantity * books.price) INTO new_total_sum
    FROM orders_books LEFT JOIN books
    ON orders_books.book_id = books.id
    WHERE orders_books.order_id = order_id_p;
    UPDATE orders SET sum_total = new_total_sum
    WHERE orders.id = order_id_p;
END;
$$;

------------------------------------------------------------



------------------------------------------------------------

-- login
CREATE OR REPLACE FUNCTION login_user(
    username_p varchar,
    password_p varchar
)
RETURNS users
LANGUAGE plpgsql
AS $$
DECLARE
    user_ users%ROWTYPE;
BEGIN
    SELECT * INTO user_ FROM users WHERE 
    users.username = username_p AND users.password = password_p;
    RETURN user_;
END;
$$;

------------------------------------------------------------



------------------------------------------------------------

CREATE OR REPLACE PROCEDURE add_review(
    review_author_id_p INTEGER, 
    book_id_p INTEGER,
    review_text_P varchar
)
LANGUAGE plpGsql
AS $$
    BEGIN
        INSERT INTO reviews (review_author_id, book_id, review_text)
        VALUEs (review_author_id_p, book_id_p, review_text_p);
    END;
$$;

------------------------------------------------------------



------------------------------------------------------------

CREATE OR REPLACE PROCEDURE update_user_info(
    id_p INTEGER,
	email_p varchar DEFAULT NULL,
	name_p varchar DEFAULT NULL,
	phone_number_p varchar DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
    BEGIN
        UPDATE users 
        SET phone_number = COALESCE(phone_number_p, 
                                    user_to_update.phone_number),
        name = COALESCE(name_p, user_to_update.name),
        email = COALESCE(email_p, user_to_update.email)        
        FROM (SELECT name, phone_number, email 
        FROM users WHERE id = id_p) AS user_to_update
        WHERE id = id_p;
    END;
$$;

------------------------------------------------------------

------------------------------------------------------------

CREATE OR REPLACE PROCEDURE update_user_role(
    user_id INTEGER, 
    new_role_id INTEGER
)
LANGUAGE PLPGSQL
AS $$
BEGIN
    UPDATE users SET role_id = new_role_id WHERE id = user_id;
END;
$$;

------------------------------------------------------------

