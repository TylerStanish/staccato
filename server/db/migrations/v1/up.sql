begin;

create table auth_token (
    id serial primary key,
    token text unique not null
);


-- TODO add 'state' table to store state params for spotify auth

commit;
