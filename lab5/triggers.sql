------------------------------------------------------------

-- recount order sum (if not commited)
-- after insert/update/delete on orders_books
CREATE OR REPLACE FUNCTION orders_update_sum_on_add_remove_book()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
    BEGIN
        IF TG_OP = 'UPDATE' OR TG_OP = 'INSERT' THEN
            IF (SELECT is_commited FROM orders 
            WHERE orders.id = NEW.order_id) IS TRUE THEN
                RAISE EXCEPTION 'Can''t modify commited order.';
            ELSE
                CALL update_order_sum(NEW.order_id);
                RETURN NEW;
            END IF;
        ELSIF TG_OP = 'DELETE' THEN
            IF (SELECT is_commited FROM orders 
            WHERE orders.id = OLD.order_id) IS TRUE THEN
                RAISE EXCEPTION 'Can''t modify commited order.';
            ELSE
                CALL update_order_sum(OLD.order_id);
                RETURN OLD;
            END IF;
        END IF;
    END;
$$;

CREATE OR REPLACE TRIGGER orders_update_sum_on_add_remove_book
AFTER INSERT OR UPDATE OR DELETE ON orders_books 
FOR EACH ROW EXECUTE FUNCTION orders_update_sum_on_add_remove_book();

------------------------------------------------------------



------------------------------------------------------------

-- recount order sum (if not commited) 
-- after update on book price
CREATE OR REPLACE FUNCTION orders_update_sum_on_book_price_changed()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
    DECLARE 
        t_row orders%ROWTYPE;
    BEGIN
        FOR t_row IN SELECT * FROM orders 
        WHERE orders.is_commited = FALSE
        AND EXISTS (SELECT * FROM orders_books 
        WHERE orders_books.order_id = orders.id 
        AND orders_books.book_id = NEW.id) LOOP
            CALL update_order_sum(t_row.id);
        END LOOP;
        RETURN NEW;
    END;
$$;

CREATE OR REPLACE TRIGGER orders_update_sum_on_book_price_changed
AFTER UPDATE OF price ON books 
FOR EACH ROW EXECUTE FUNCTION orders_update_sum_on_book_price_changed();

------------------------------------------------------------



------------------------------------------------------------

-- set user status to inactive instead of delete
-- users.is_active=false instead of delete on users 
CREATE OR REPLACE FUNCTION delete_user()
RETURNS TRIGGER 
LANGUAGE PLPGSQL 
AS $$
    BEGIN
        UPDATE users SET is_active = FALSE 
        WHERE id = OLD.id;
        RETURN NULL; -- PREVENT DELETION
    END;
$$;

CREATE OR REPLACE TRIGGER delete_user
BEFORE DELETE ON users 
FOR EACH ROW EXECUTE FUNCTION delete_user();

------------------------------------------------------------



------------------------------------------------------------

-- set creation_time and delivery_date for new order 
-- (now(), now() + x days)
CREATE OR REPLACE FUNCTION orders_set_time()
RETURNS TRIGGER 
LANGUAGE plpgsql
AS $$
    BEGIN
        IF NEW.is_commited = TRUE THEN
            NEW.creation_date := now();
            NEW.delivery_date := now()::date + INTERVAL '3 DAYS';
        END IF;
        RETURN NEW;
    END;
$$;

CREATE OR REPLACE TRIGGER orders_set_time
BEFORE UPDATE OF is_commited OR INSERT ON orders
FOR EACH ROW EXECUTE FUNCTION orders_set_time();

------------------------------------------------------------



------------------------------------------------------------

-- logs (after insert/update/delete on users)
CREATE OR REPLACE FUNCTION logging_users()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
    BEGIN
        IF TG_OP = 'UPDATE' THEN
            INSERT INTO logs (user_id, message, time) 
            VALUES (NEW.id, 'User updated', now());
            RETURN NEW;
        ELSIF TG_OP = 'DELETE' THEN
            INSERT INTO logs (user_id, message, time)
            VALUES (OLD.id, format('User ''%s'' deleted', OLD.username), now());
            RETURN NEW;
        ELSIF TG_OP = 'INSERT' THEN
            INSERT INTO logs (user_id, message, time)
            VALUES (NEW.id, 'User inserted', now());
            RETURN NEW;
        END IF;
    END; 
$$;

CREATE OR REPLACE TRIGGER logging_users
AFTER UPDATE OR DELETE OR INSERT ON users
FOR EACH ROW EXECUTE FUNCTION logging_users();

------------------------------------------------------------