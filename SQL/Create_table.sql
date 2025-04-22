create table if not exists sales (
            id serial primary key,
            doc_id varchar(30),
            item varchar,
            category varchar(50),
            amount int,
            price numeric,
            discount numeric
        )